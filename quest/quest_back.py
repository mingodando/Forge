import json
import os
import re
from datetime import datetime

import customtkinter as ctk

from tkinter import messagebox
from backend.config import Config
from currency.currency import Currency
from backend.directory_setup import Directory
from pages.quest_page import TIER_LEVEL

XP_MULTIPLIER = 6


class QuestBack:
    def __init__(self):
        self.config = Config()
        self.currency = Currency()
        self.directory = Directory()

        self.slots_used = None

    def main(self):
        pass

    def update_quest_folder(self):
        current_directory = self.directory.quest_file()

        files = sorted(
            os.listdir(current_directory),
            key=lambda fname: int(os.path.splitext(fname)[0].removeprefix("data_")), )

        for index, fname in enumerate(files, start=1):
            old_path = os.path.join(current_directory, fname)
            new_path = os.path.join(current_directory, f"data_{index}.json")
            if old_path != new_path:
                os.rename(old_path, new_path)

    def file_largest_num(self):
        current_directory = self.directory.quest_file()
        numbers = [int(re.sub(r"^\D+", "", os.path.splitext(fname)[0])) for fname in os.listdir(current_directory)]
        largest_number = max(numbers, default=0)

        return largest_number

    def create_quest_file(self, name, category, difficulty):
        self.update_quest_folder()
        current_directory = self.directory.quest_file()
        os.makedirs(current_directory, exist_ok=True)

        target_num = self.file_largest_num() + 1

        file_name = f"data_{target_num}.json"

        quest_data = {
            "name": name,
            "category": category,
            "difficulty": difficulty,
            "created_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "completed": False,
        }

        with open(os.path.join(current_directory, file_name), "w") as f:
            json.dump(quest_data, f, indent=4)
            messagebox.showinfo("Quest Created", "Your quest has been created successfully!")

    def timed_delete_quest(self):
        current_directory = self.directory.quest_file()
        current_time = datetime.now()

        for fname in os.listdir(current_directory):
            file_path = os.path.join(current_directory, fname)

            with open(file_path, "r") as f:
                quest_data = json.load(f)

            created_date = datetime.strptime(quest_data["created_date"], "%Y-%m-%d %H:%M:%S")

            if created_date.date() < current_time.date():
                os.remove(file_path)

        self.update_quest_folder()

    def load_quests(self):
        self.timed_delete_quest()
        current_directory = self.directory.quest_file()
        os.makedirs(current_directory, exist_ok=True)

        files = sorted(
            os.listdir(current_directory),
            key=lambda fname: int(os.path.splitext(fname)[0].removeprefix("data_")),
        )

        quests = []
        for fname in files:
            with open(os.path.join(current_directory, fname), "r") as f:
                quest_data = json.load(f)
            quest_data["file_name"] = fname
            quests.append(quest_data)

        return quests

    @staticmethod
    def calculate_rewards(difficulty):
        coins = TIER_LEVEL[difficulty.lower()]
        xp = coins * XP_MULTIPLIER
        return coins, xp

    def get_max_quests(self):
        path = os.path.join(self.directory.main(), "save.json")
        with open(path, "r") as f:
            data = json.load(f)
        return data.get("max_quests", 5)

    def add_xp(self, amount):
        path = os.path.join(self.directory.main(), "save.json")
        with open(path, "r") as f:
            data = json.load(f)

        data["xp"] = data.get("xp", 0) + amount

        with open(path, "w") as f:
            json.dump(data, f, indent=4)

    def complete_quest(self, file_name):
        current_directory = self.directory.quest_file()
        path = os.path.join(current_directory, file_name)

        with open(path, "r") as f:
            quest_data = json.load(f)

        if quest_data.get("completed"):
            return 0, 0

        coins, xp = self.calculate_rewards(quest_data["difficulty"])
        self.currency.currency_change(coins)
        self.add_xp(xp)

        quest_data["completed"] = True
        with open(path, "w") as f:
            json.dump(quest_data, f, indent=4)

        return coins, xp

    def delete_quest(self, file_name):
        current_directory = self.directory.quest_file()
        path = os.path.join(current_directory, file_name)
        if os.path.exists(path):
            os.remove(path)
        self.update_quest_folder()

    def get_num_quests(self):
        quests = self.load_quests()
        self.slots_used = len([quest for quest in quests if not quest.get("completed", False)])
        return self.slots_used

    def quest_display(self):
        line = f"{self.get_num_quests()} quests left today. Streak safe until midnight!"
        return line