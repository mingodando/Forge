import json
import os
import re
import customtkinter as ctk
from tkinter import messagebox

from backend.config import Config
from backend.start_setup import get_setup
from backend.directory_setup import Directory

_quest_instance = None

def get_quest():
    global _quest_instance
    if _quest_instance is None:
        _quest_instance = Quest()
    return _quest_instance

class Quest:
    def __init__(self):
        self.config = Config()
        self.directory = Directory()
        self.config.main()
        self.setup = get_setup()

        self.frame = None
        self.topbar_frame = None

    def main(self):
        self.frame = ctk.CTkFrame(self.setup.content_frame, width=1120, height=680, fg_color=self.config.bg, corner_radius=0)
        self.frame.grid(row=0, column=0, sticky="nsew")
        self.frame.grid_propagate(False)

        self.topbar_frame = ctk.CTkFrame(self.setup.topbar, width=1120, height=680, fg_color=self.config.bg)
        self.topbar_frame.grid(row=0, column=0, sticky="nsew")

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
        }

        with open(os.path.join(current_directory, file_name), "w") as f:
            json.dump(quest_data, f, indent=4)
            messagebox.showinfo("Quest Created", "Your quest has been created successfully!")
