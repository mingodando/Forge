import json
import os

from backend.config import Config
from backend.directory_setup import Directory
from currency.currency import Currency
from forge.forge_back import get_forgeback, GEAR_CATALOG
from habit.habit_back import get_habitback

SHOP_CATALOG = {
    "extra_quest_slot": {
        "name": "Extra quest slot",
        "description": "Raise your quest cap from {current} to {next}. Applies immediately.",
        "icon": "\U0001F4CB",
        "cost": 150,
    },
    "streak_revival": {
        "name": "Streak revival",
        "description": "Restore one broken streak to its previous count. Choose after buying.",
        "icon": "\U0001F525",
        "cost": 200,
    },
    "shield_refresh": {
        "name": "Shield refresh",
        "description": "Refill all shield charges on your equipped Off-Hand gear.",
        "icon": "\U0001F6E1",
        "cost": 90,
    },
    "ember_skin": {
        "name": "Ember skin — Main Hand",
        "description": "Cosmetic finish for your equipped weapon. Pure style, no stats.",
        "icon": "\U0001F3A8",
        "cost": 120,
    },
}

_shopback_instance = None


def get_shopback():
    global _shopback_instance
    if _shopback_instance is None:
        _shopback_instance = ShopBack()
    return _shopback_instance


class ShopBack:
    def __init__(self):
        self.config = Config()
        self.directory = Directory()
        self.currency = Currency()
        self.forge_back = get_forgeback()
        self.habit_back = get_habitback()

    def main(self):
        pass

    def save_path(self):
        return os.path.join(self.directory.main(), "save.json")

    def read_save(self):
        with open(self.save_path(), "r") as f:
            return json.load(f)

    def write_save(self, data):
        with open(self.save_path(), "w") as f:
            json.dump(data, f, indent=4)

    #--- Availability checks ---#
    def can_afford(self, item_id):
        return self.currency.get_currencies() >= SHOP_CATALOG[item_id]["cost"]

    def get_off_hand_item(self):
        item_id = self.forge_back.get_equipped_item_id("off_hand")
        if item_id is None:
            return None
        return GEAR_CATALOG[item_id]

    def get_revivable_habits(self):
        habits = self.habit_back.load_habits()
        return [h for h in habits if h.get("streak", 0) == 0 and h.get("previous_streak", 0) > 0]

    def has_ember_skin(self):
        return "ember_skin" in self.read_save().get("cosmetics", [])

    def can_buy(self, item_id):
        if not self.can_afford(item_id):
            return False, "Not enough coins"

        if item_id == "shield_refresh" and self.get_off_hand_item() is None:
            return False, "No Off-Hand gear equipped — smelt one first"

        if item_id == "ember_skin" and self.has_ember_skin():
            return False, "Owned"

        return True, ""

    #--- Purchases ---#
    def buy_extra_quest_slot(self):
        data = self.read_save()
        data["max_quests"] = data.get("max_quests", 5) + 1
        self.write_save(data)
        self.currency.currency_change(-SHOP_CATALOG["extra_quest_slot"]["cost"])
        return data["max_quests"]

    def buy_shield_refresh(self):
        off_hand = self.get_off_hand_item()
        if off_hand is None or off_hand["bonus_type"] != "shield_charge":
            return False
        max_charges = 1 + off_hand["bonus_value"]
        data = self.read_save()
        data["shield_charges"] = max_charges
        self.write_save(data)
        self.currency.currency_change(-SHOP_CATALOG["shield_refresh"]["cost"])
        return True

    def buy_ember_skin(self):
        data = self.read_save()
        cosmetics = data.setdefault("cosmetics", [])
        if "ember_skin" in cosmetics:
            return False
        cosmetics.append("ember_skin")
        self.write_save(data)
        self.currency.currency_change(-SHOP_CATALOG["ember_skin"]["cost"])
        return True

    def buy_streak_revival(self, file_name):
        current_directory = self.directory.habit_file()
        path = os.path.join(current_directory, file_name)
        if not os.path.exists(path):
            return False
        with open(path, "r") as f:
            habit_data = json.load(f)

        if habit_data.get("streak", 0) != 0 or habit_data.get("previous_streak", 0) <= 0:
            return False

        habit_data["streak"] = habit_data["previous_streak"]
        habit_data["previous_streak"] = 0
        with open(path, "w") as f:
            json.dump(habit_data, f, indent=4)

        self.currency.currency_change(-SHOP_CATALOG["streak_revival"]["cost"])
        return True
