import customtkinter as ctk
import os
import json
from tkinter import simpledialog

from backend.config import Config
from backend.directory_setup import Directory

class Setup:
    def __init__(self):
        self.config = Config()
        self.directory = Directory()
        self.config.main()

        self.current_directory = None
        self.data_file_name = None
        self.data_path = None
        self.focus_path = None
        self.focus_file_name = None

        self.root = None
        self.topbar = None
        self.navbar = None
        self.content_frame = None

#----- Starting Functions -----#
    def create_home_page(self, root):
        self.root = root
        self.topbar = ctk.CTkFrame(self.root, width=1120, height=120, bg_color=self.config.bg, fg_color=self.config.bg)
        self.topbar.grid(row=0, column=1, sticky="n")
        self.topbar.grid_propagate(False)
        self.navbar = ctk.CTkFrame(self.root, width=160, height=900, bg_color=self.config.nav, fg_color=self.config.nav)
        self.navbar.grid(row=0, column=0, rowspan=2, sticky="ns")
        self.navbar.grid_propagate(False)
        self.content_frame = ctk.CTkFrame(self.root, width=1120, height=780, bg_color=self.config.bg, fg_color=self.config.bg)
        self.content_frame.grid(row=1, column=1, sticky="nw")
        self.content_frame.grid_propagate(False)

    def on_click_home(self):
        self.content_frame.tkraise()

    def get_user_name(self):
        self.username = simpledialog.askstring("Username", "Please enter your username")

        with open(os.path.join(self.directory.main(), "save.json"), "r", encoding="utf-8") as f:
            data = json.load(f)

        data["username"] = self.username

        with open(os.path.join(self.directory.main(), "save.json"), "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)


    def check_user_name(self):
        with open(os.path.join(self.directory.main(), "save.json"), "r", encoding="utf-8") as f:
            data = json.load(f)
            if data["username"] == "":
                self.get_user_name()
            else:
                pass

    def migrate_save_data(self, defaults):
        with open(self.data_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        changed = False
        for key, default_value in defaults.items():
            if key not in data:
                data[key] = default_value
                changed = True

        if not isinstance(data.get("materials"), dict):
            data["materials"] = dict(defaults["materials"])
            changed = True

        if not isinstance(data.get("gear"), dict) or "smelted" not in data.get("gear", {}):
            data["gear"] = dict(defaults["gear"])
            changed = True

        if changed:
            with open(self.data_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)

    def setup_files(self):
        data = {
            "username": "",
            "level": 0,
            "xp": 0,
            "max_quests": 5,
            "max_habits": 3,
            "materials": {"Wood": 0, "Stone": 0, "Clay": 0, "Iron": 0},
            "gear": {"smelted": [], "equipped": {}},
            "shield_charges": 1,
            "streaks": 0,
            "history": []
        }

        self.data_file_name = "save.json"
        self.data_path = os.path.join(self.directory.main(), self.data_file_name)

        if not os.path.exists(self.data_path):
            with open(self.data_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            print(f"Successfully created the file: {self.data_path}")
        else:
            self.migrate_save_data(data)
            print(f"File already exists")

        self.focus_file_name = "focus.txt"
        self.focus_path = self.directory.focus_file()

        if not os.path.exists(self.focus_path):
            with open(self.focus_path, "w", encoding="utf-8") as f:
                pass
            print(f"Successfully created the file: {self.focus_path}")
        else:
            print(f"File already exists")

        # quest_file()/habit_file() create their own subfolders on demand.
        self.directory.quest_file()
        self.directory.habit_file()

_setup_instance = None

def get_setup():
    global _setup_instance
    if _setup_instance is None:
        _setup_instance = Setup()
    return _setup_instance