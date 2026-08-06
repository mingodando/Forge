import os
import json
import customtkinter as ctk
from tkinter import messagebox

from backend.config import Config
from backend.start_setup import get_setup
from backend.directory_setup import Directory
from pages.habit_page import get_habit
from habit.habit_front import get_habitfront

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
        self.habit_front = get_habitfront()

    def main(self):
        pass

    def create_habit(self):
        self.popup = ctk.CTkToplevel(self.habit_page.frame)
        self.popup.title("Create New Habit")

    def get_max_habits(self):
        path = os.path.join(self.directory.main(), "save.json")

        with open(path, "r") as f:
            data = json.load(f)

        return data["max_habits"]