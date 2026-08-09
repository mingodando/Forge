import os
import json
import re
from datetime import date
from tkinter import messagebox

from backend.config import Config
from currency.currency import Currency
from backend.directory_setup import Directory
from forge.forge_back import get_forgeback
from pages.quest_page import TIER_LEVEL
from quest.quest_back import XP_MULTIPLIER

_habitback_instance = None


def get_habitback():
    global _habitback_instance
    if _habitback_instance is None:
        _habitback_instance = HabitBack()
    return _habitback_instance

class HabitBack:
    def __init__(self):
        self.config = Config()
        self.directory = Directory()
        self.currency = Currency()
        self.forge_back = get_forgeback()

    def main(self):
        pass

    @staticmethod
    def calculate_rewards(difficulty):
        coins = TIER_LEVEL[difficulty.lower()]
        xp = coins * XP_MULTIPLIER
        return coins, xp

    def add_xp(self, amount):
        path = os.path.join(self.directory.main(), "save.json")
        with open(path, "r") as f:
            data = json.load(f)

        data["xp"] = data.get("xp", 0) + amount

        with open(path, "w") as f:
            json.dump(data, f, indent=4)

    def get_max_habits(self):
        path = os.path.join(self.directory.main(), "save.json")

        with open(path, "r") as f:
            data = json.load(f)

        return data["max_habits"]

    def get_shield_charges(self):
        path = os.path.join(self.directory.main(), "save.json")
        with open(path, "r") as f:
            data = json.load(f)
        return data.get("shield_charges", 1)

    def set_shield_charges(self, amount):
        path = os.path.join(self.directory.main(), "save.json")
        with open(path, "r") as f:
            data = json.load(f)
        data["shield_charges"] = amount
        with open(path, "w") as f:
            json.dump(data, f, indent=4)

    def toggle_shield(self, file_name):
        current_directory = self.directory.habit_file()
        path = os.path.join(current_directory, file_name)

        with open(path, "r") as f:
            data = json.load(f)

        if data.get("shielded", False):
            data["shielded"] = False
            self.set_shield_charges(self.get_shield_charges() + 1)
        else:
            charges = self.get_shield_charges()
            if charges <= 0:
                return False
            self.set_shield_charges(charges - 1)
            data["shielded"] = True

        with open(path, "w") as f:
            json.dump(data, f, indent=4)

        return True

    def update_habit_folder(self):
        current_directory = self.directory.habit_file()

        files = sorted(
            os.listdir(current_directory),
            key=lambda fname: int(os.path.splitext(fname)[0].removeprefix("habit_")))

        for index, fname in enumerate(files, start=1):
            old_path = os.path.join(current_directory, fname)
            new_path = os.path.join(current_directory, f"habit_{index}.json")
            if old_path != new_path:
                os.rename(old_path, new_path)

    def file_largest_num(self):
        current_directory = self.directory.habit_file()
        numbers = [int(re.sub(r"^\D+", "", os.path.splitext(fname)[0])) for fname in os.listdir(current_directory)]
        largest_number = max(numbers, default=0)

        return largest_number

    def create_habit_file(self, name, category, difficulty):
        self.update_habit_folder()
        current_directory = self.directory.habit_file()
        os.makedirs(current_directory, exist_ok=True)

        target_num = self.file_largest_num() + 1

        file_name = f"habit_{target_num}.json"

        habit_data = {
            "name": name,
            "category": category,
            "difficulty": difficulty,
            "checked": False,
            "streak": 0,
            "streak_date": date.today().isoformat(),
            "last_completed_date": None,
            "shielded": False,
        }

        with open(os.path.join(current_directory, file_name), "w") as f:
            json.dump(habit_data, f, indent=4)
            messagebox.showinfo("Habit Created", f"Habit '{name}' created successfully!")

    def reset_daily(self, data):
        today = date.today()
        streak_date_str = data.get("streak_date")
        streak_date = date.fromisoformat(streak_date_str) if streak_date_str else today

        if streak_date >= today:
            data["streak_date"] = data.get("streak_date", today.isoformat())
            return data

        gap = (today - streak_date).days
        missed_days = gap - 1 if data.get("last_completed_date") == streak_date_str else gap

        if missed_days > 0:
            protection = self.forge_back.get_missed_day_protection()
            if missed_days == 1 and data.get("shielded"):
                data["shielded"] = False
            elif missed_days <= protection:
                pass
            else:
                if data.get("streak", 0) > 0:
                    data["previous_streak"] = data["streak"]
                data["streak"] = 0

        data["checked"] = False
        data["streak_date"] = today.isoformat()
        return data

    def load_habits(self):
        current_directory = self.directory.habit_file()
        os.makedirs(current_directory, exist_ok=True)

        files = sorted(
            os.listdir(current_directory),
            key=lambda fname: int(os.path.splitext(fname)[0].removeprefix("habit_")),
        )

        habits = []
        for fname in files:
            path = os.path.join(current_directory, fname)
            with open(path, "r") as f:
                habit_data = json.load(f)

            updated = self.reset_daily(dict(habit_data))
            if updated != habit_data:
                with open(path, "w") as f:
                    json.dump(updated, f, indent=4)

            updated["file_name"] = fname
            habits.append(updated)

        return habits

    def complete_habit(self, file_name):
        current_directory = self.directory.habit_file()
        path = os.path.join(current_directory, file_name)

        with open(path, "r") as f:
            data = json.load(f)

        today = date.today().isoformat()
        if data.get("checked") or data.get("last_completed_date") == today:
            if not data.get("checked") and data.get("last_completed_date") == today:
                # Someone hand-edited "checked" back to false after already completing
                # today; heal the file instead of leaving it in a re-clickable state.
                data["checked"] = True
                with open(path, "w") as f:
                    json.dump(data, f, indent=4)
            return 0, 0

        coins, xp = self.calculate_rewards(data["difficulty"])
        xp = round(xp * self.forge_back.get_xp_multiplier())
        self.currency.currency_change(coins)
        self.add_xp(xp)
        self.forge_back.add_material_for_category(data["category"], data["difficulty"])

        data["checked"] = True
        data["streak"] = data.get("streak", 0) + 1
        data["streak_date"] = today
        data["last_completed_date"] = today

        with open(path, "w") as f:
            json.dump(data, f, indent=4)

        return coins, xp

    def get_best_streak(self):
        habits = self.load_habits()
        if not habits:
            return None, 0
        best = max(habits, key=lambda habit: habit.get("streak", 0))
        return best["name"], best.get("streak", 0)

    def get_num_habits_left(self):
        habits = self.load_habits()
        self.habits_left = len([habit for habit in habits if not habit.get("checked", False)])
        return self.habits_left

    def habit_display(self):
        line = f"{self.get_num_habits_left()} habits left today. Streak safe until midnight!"
        return line

    def delete_habit(self, file_name):
        current_directory = self.directory.habit_file()
        path = os.path.join(current_directory, file_name)
        if os.path.exists(path):
            os.remove(path)
        self.update_habit_folder()
