import json
import os
import re
from datetime import datetime

import customtkinter as ctk

from tkinter import messagebox
from backend.config import Config
from currency.currency import Currency
from backend.directory_setup import Directory



class QuestBack:
    def __init__(self):
        self.config = Config()
        self.currency = Currency()
        self.directory = Directory()

    def main(self):
        pass

    def update_quest_folder(self):
        current_directory = self.directory.quest_file()

        files = sorted(
            os.listdir(current_directory),
            key=lambda fname: int(os.path.splitext(fname)[0].removeprefix("data_")),
        )

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

    def create_quest_frontend(self):
        pass