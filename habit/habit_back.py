import os
import json
import re
import customtkinter as ctk
from tkinter import messagebox

from backend.config import Config
from backend.start_setup import get_setup
from backend.directory_setup import Directory
from pages.habit_page import get_habit

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
        self.setup = get_setup()
        self.habit_page = get_habit()

    def main(self):
        pass

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

    def create_habit(self):
        self.popup = ctk.CTkToplevel(self.habit_page.frame)
        self.popup.title("Create New Habit")

    def get_max_habits(self):
        path = os.path.join(self.directory.main(), "save.json")

        with open(path, "r") as f:
            data = json.load(f)

        return data["max_habits"]

    def file_largest_num(self):
        current_directory = self.directory.habit_file()
        numbers = [int(re.sub(r"^\D+", "", os.path.splitext(fname)[0])) for fname in os.listdir(current_directory)]
        largest_number = max(numbers, default=0)

        return largest_number
    def create_habit_file(self, name, category, difficulty):
        current_directory = self.directory.habit_file()
        os.makedirs(current_directory, exist_ok=True)

        target_num = self.file_largest_num()

        file_name = f"habit_{target_num}.json"

        habit_data = {
            "name": name,
            "category": category,
            "difficulty": difficulty,
            "checked": False,
        }

        with open(os.path.join(current_directory, file_name), "w") as f:
            json.dump(habit_data, f, indent=4)
            messagebox.showinfo("Habit Created", f"Habit '{name}' created successfully!")

    def delete_habit(self, file_name):
        current_directory = self.directory.habit_file()
        path = os.path.join(current_directory, file_name)
        if os.path.exists(path):
            os.remove(path)
        self.update_habit_folder()
