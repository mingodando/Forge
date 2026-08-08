import os
import json
import re
from datetime import date
from tkinter import messagebox

from backend.config import Config
from currency.currency import Currency
from backend.directory_setup import Directory
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
            "shielded": False,
        }

        with open(os.path.join(current_directory, file_name), "w") as f:
            json.dump(habit_data, f, indent=4)
            messagebox.showinfo("Habit Created", f"Habit '{name}' created successfully!")

    @staticmethod
    def reset_daily(data):
        today = date.today()
        streak_date_str = data.get("streak_date")
        streak_date = date.fromisoformat(streak_date_str) if streak_date_str else today

        if streak_date >= today:
            data["streak_date"] = data.get("streak_date", today.isoformat())
            return data

        gap = (today - streak_date).days
        missed_days = gap - 1 if data.get("checked") else gap

        if missed_days > 0:
            if missed_days == 1 and data.get("shielded"):
                data["shielded"] = False
            else:
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

        if data.get("checked"):
            return 0, 0

        coins, xp = self.calculate_rewards(data["difficulty"])
        self.currency.currency_change(coins)
        self.add_xp(xp)

        data["checked"] = True
        data["streak"] = data.get("streak", 0) + 1
        data["streak_date"] = date.today().isoformat()

        with open(path, "w") as f:
            json.dump(data, f, indent=4)

        return coins, xp

    def delete_habit(self, file_name):
        current_directory = self.directory.habit_file()
        path = os.path.join(current_directory, file_name)
        if os.path.exists(path):
            os.remove(path)
        self.update_habit_folder()
