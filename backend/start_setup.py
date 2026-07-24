import customtkinter as ctk
import os
import json

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
        self.navbar = ctk.CTkFrame(self.root, width=160, height=800, bg_color=self.config.nav, fg_color=self.config.nav)
        self.navbar.grid(row=0, column=0, rowspan=2, sticky="ns")
        self.navbar.grid_propagate(False)
        self.content_frame = ctk.CTkFrame(self.root, width=1120, height=680, bg_color=self.config.bg, fg_color=self.config.bg)
        self.content_frame.grid(row=1, column=1, sticky="nw")
        self.content_frame.grid_propagate(False)

    def on_click_home(self):
        self.content_frame.tkraise()

    def setup_files(self):
        current_directory = self.directory.backend_directory()
        data = [
            "level",
            "xp",
            "materials",
            "gear",
            "streaks",
            "history"
        ]

        self.data_file_name = "../save.json"

        self.data_path = os.path.join(current_directory, self.data_file_name)

        if not os.path.exists(self.data_path):
            with open(self.data_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            print(f"Successfully created the file: {self.data_file_name}")
        else:
            print(f"File already exists")

        self.focus_file_name = "focus.txt"
        self.focus_path = self.directory.focus_file()

        if not os.path.exists(self.focus_path):
            with open(self.focus_path, "w", encoding="utf-8") as f:
                pass
            print(f"Successfully created the file: {self.focus_file_name}")
        else:
            print(f"File already exists")

_setup_instance = None

def get_setup():
    global _setup_instance
    if _setup_instance is None:
        _setup_instance = Setup()
    return _setup_instance