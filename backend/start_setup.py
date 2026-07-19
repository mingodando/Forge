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
        self.file_path = None

        self.root = None
        self.topbar = None
        self.navbar = None
        self.content_frame = None

#----- Starting Functions -----#
    def create_home_page(self, root):
        self.root = root
        self.topbar = ctk.CTkFrame(self.root, width=1120, height=120, bg_color=self.config.window_color, fg_color=self.config.window_color)
        self.topbar.grid(row=0, column=1, sticky="n")
        self.topbar.grid_propagate(False)
        self.navbar = ctk.CTkFrame(self.root, width=160, height=800, bg_color=self.config.sidebar_color, fg_color=self.config.sidebar_color)
        self.navbar.grid(row=0, column=0, rowspan=2, sticky="ns")
        self.navbar.grid_propagate(False)
        self.content_frame = ctk.CTkFrame(self.root, width=1120, height=680, bg_color=self.config.window_color, fg_color=self.config.window_color)
        self.content_frame.grid(row=1, column=1, sticky="nw")
        self.content_frame.grid_propagate(False)

    def on_click_home(self):
        self.content_frame.tkraise()

    def setup_files(self):
        current_directory = self.directory.backend_directory()
        data = [
            "level",
            "xp",
            "coins",
            "materials",
            "gear",
            "streaks",
            "history"
        ]

        self.data_file_name = "../save.json"

        self.file_path = os.path.join(current_directory, self.data_file_name)

        if not os.path.exists(self.file_path):
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            print(f"Successfully created the file: {self.data_file_name}")
        else:
            print(f"File already exists")