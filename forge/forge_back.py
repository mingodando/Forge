import json
import os

from backend.config import Config
from backend.directory_setup import Directory
from backend.leveling import get_level_info
from currency.currency import Currency

CATEGORY_MATERIAL = {
    "social": "Wood",
    "work": "Stone",
    "study": "Clay",
    "exercise": "Iron",
}

MATERIAL_DROP_TIER = {
    "easy": 1,
    "medium": 2,
    "hard": 3,
}

GEAR_CATALOG = {
    "iron_shortsword": {
        "name": "Iron Shortsword",
        "slot": "main_hand",
        "slot_label": "Main Hand",
        "path": "B",
        "tag": "Damage",
        "icon": "\U0001F5E1",
        "bonus_type": "xp_gain",
        "bonus_value": 8,
        "bonus_label": "+8% XP gain",
        "material": "Iron",
        "material_cost": 6,
        "coin_cost": 60,
        "unlock_level": 0,
    },
    "clay_etched_band": {
        "name": "Clay-Etched Band",
        "slot": "off_hand",
        "slot_label": "Off Hand",
        "path": "A",
        "tag": "Tank",
        "icon": "\U0001F6E1",
        "bonus_type": "shield_charge",
        "bonus_value": 1,
        "bonus_label": "+1 streak shield charge",
        "material": "Clay",
        "material_cost": 4,
        "coin_cost": 45,
        "unlock_level": 0,
    },
    "iron_chestplate": {
        "name": "Iron Chestplate",
        "slot": "chest",
        "slot_label": "Chest",
        "path": "B",
        "tag": "Damage",
        "icon": "\U0001F9BA",
        "bonus_type": "xp_gain",
        "bonus_value": 5,
        "bonus_label": "+5% XP gain",
        "material": "Iron",
        "material_cost": 8,
        "coin_cost": 80,
        "unlock_level": 0,
    },
    "reinforced_shield": {
        "name": "Reinforced Shield",
        "slot": "off_hand",
        "slot_label": "Off Hand",
        "path": "A",
        "tag": "Tank",
        "icon": "\U0001F6E1",
        "bonus_type": "missed_day_protection",
        "bonus_value": 2,
        "bonus_label": "+2 missed-day protection",
        "material": "Iron",
        "material_cost": 10,
        "coin_cost": 150,
        "unlock_level": 20,
    },
}

GEAR_SLOTS = ["main_hand", "off_hand", "chest"]

_forgeback_instance = None


def get_forgeback():
    global _forgeback_instance
    if _forgeback_instance is None:
        _forgeback_instance = ForgeBack()
    return _forgeback_instance


class ForgeBack:
    def __init__(self):
        self.config = Config()
        self.directory = Directory()
        self.currency = Currency()

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

    #--- XP / Level ---#
    def get_xp(self):
        return self.read_save().get("xp", 0)

    #--- Materials ---#
    def get_materials(self):
        data = self.read_save()
        materials = data.get("materials", {})
        return {material: materials.get(material, 0) for material in ("Wood", "Stone", "Clay", "Iron")}

    def add_material_for_category(self, category, difficulty):
        material = CATEGORY_MATERIAL.get(category.lower())
        if material is None:
            return
        amount = MATERIAL_DROP_TIER.get(difficulty.lower(), 0)
        if amount <= 0:
            return

        data = self.read_save()
        materials = data.setdefault("materials", {})
        materials[material] = materials.get(material, 0) + amount
        self.write_save(data)

    def spend_materials(self, material, amount):
        data = self.read_save()
        materials = data.setdefault("materials", {})
        if materials.get(material, 0) < amount:
            return False
        materials[material] -= amount
        self.write_save(data)
        return True

    #--- Gear inventory ---#
    def get_gear_state(self):
        data = self.read_save()
        gear = data.get("gear", {})
        smelted = gear.get("smelted", [])
        equipped = gear.get("equipped", {})
        return smelted, equipped

    def is_smelted(self, item_id):
        smelted, _ = self.get_gear_state()
        return item_id in smelted

    def get_equipped_item_id(self, slot):
        _, equipped = self.get_gear_state()
        return equipped.get(slot)

    def is_locked(self, item_id):
        item = GEAR_CATALOG[item_id]
        level = get_level_info(self.get_xp())["level"]
        return level < item["unlock_level"]

    def can_smelt(self, item_id):
        item = GEAR_CATALOG[item_id]
        level = get_level_info(self.get_xp())["level"]
        if level < item["unlock_level"]:
            return False, f"Unlocks at Level {item['unlock_level']} — {item['unlock_level'] - level} levels to go"

        if self.is_smelted(item_id):
            return False, "Already smelted"

        materials = self.get_materials()
        have = materials.get(item["material"], 0)
        need = item["material_cost"]
        if have < need:
            category_hint = next((c for c, m in CATEGORY_MATERIAL.items() if m == item["material"]), None)
            hint = f" — {category_hint.capitalize()} quests drop it" if category_hint else ""
            return False, f"Need {need - have} more {item['material']}{hint}"

        if self.currency.get_currencies() < item["coin_cost"]:
            return False, "Not enough coins"

        return True, ""

    def smelt(self, item_id):
        ok, _ = self.can_smelt(item_id)
        if not ok:
            return False

        item = GEAR_CATALOG[item_id]
        if not self.spend_materials(item["material"], item["material_cost"]):
            return False
        self.currency.currency_change(-item["coin_cost"])

        data = self.read_save()
        gear = data.setdefault("gear", {"smelted": [], "equipped": {}})
        smelted = gear.setdefault("smelted", [])
        if item_id not in smelted:
            smelted.append(item_id)
        self.write_save(data)
        return True

    def equip(self, item_id):
        item = GEAR_CATALOG[item_id]
        if not self.is_smelted(item_id):
            return False

        slot = item["slot"]
        current = self.get_equipped_item_id(slot)
        if current == item_id:
            return True
        if current is not None:
            self.unequip(slot)

        data = self.read_save()
        gear = data.setdefault("gear", {"smelted": [], "equipped": {}})
        gear.setdefault("equipped", {})[slot] = item_id
        self.write_save(data)

        if item["bonus_type"] == "shield_charge":
            data = self.read_save()
            data["shield_charges"] = data.get("shield_charges", 1) + item["bonus_value"]
            self.write_save(data)

        return True

    def unequip(self, slot):
        item_id = self.get_equipped_item_id(slot)
        if item_id is None:
            return False
        item = GEAR_CATALOG[item_id]

        data = self.read_save()
        gear = data.setdefault("gear", {"smelted": [], "equipped": {}})
        gear.setdefault("equipped", {}).pop(slot, None)
        self.write_save(data)

        if item["bonus_type"] == "shield_charge":
            data = self.read_save()
            data["shield_charges"] = max(0, data.get("shield_charges", 1) - item["bonus_value"])
            self.write_save(data)

        return True

    #--- Aggregate bonuses ---#
    def get_equipped_items(self):
        _, equipped = self.get_gear_state()
        return [GEAR_CATALOG[item_id] for item_id in equipped.values() if item_id in GEAR_CATALOG]

    def get_gear_bonus_percent(self):
        return sum(item["bonus_value"] for item in self.get_equipped_items() if item["bonus_type"] == "xp_gain")

    def get_equipped_count(self):
        return len(self.get_equipped_items())

    def get_xp_multiplier(self):
        return 1 + self.get_gear_bonus_percent() / 100

    def get_missed_day_protection(self):
        return sum(item["bonus_value"] for item in self.get_equipped_items() if item["bonus_type"] == "missed_day_protection")
