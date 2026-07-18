import customtkinter as ctk
import os
import json

from config import Config

class Setup:
    def __init__(self):
        self.config = Config()
        self.config.main()

        self.current_directory = None
        self.data_file_name = None
        self.file_path = None

        self.root = None
        self.topbar = None
        self.navbar = None
        self.content_frame = None

        self.weights(self.topbar, self.content_frame, self.navbar)

#----- Starting Functions -----#
    def create_home_page(self, root):
        self.root = root
        self.topbar = ctk.CTkFrame(self.root, width=1160, height=100)
        self.topbar.grid(row=0, column=1, sticky="n")
        self.topbar.configure(fg_color=self.config.topbar_color)
        self.topbar.grid_propagate(False)
        self.navbar = ctk.CTkFrame(self.root, width=120, height=720)
        self.navbar.grid(row=0, column=0, rowspan=2, sticky="ns")
        self.navbar.configure(fg_color=self.config.navbar_color)
        self.navbar.grid_propagate(False)
        self.content_frame = ctk.CTkFrame(self.root, width=1160, height=620)
        self.content_frame.grid(row=1, column=1, sticky="se")
        self.content_frame.configure(fg_color=self.config.background_color)

    def weights(self, topbar, content_frame, navbar):
        #--- Topbar ---#
        pass

    def on_click_home(self):
        self.content_frame.tkraise()

    def setup_directory(self):
        self.current_directory = os.getcwd()
        return self.current_directory

    def setup_files(self):
        current_directory = self.setup_directory()
        data = [
            "level",
            "xp",
            "coins",
            "materials",
            "gear",
            "streaks",
            "history"
        ]

        self.data_file_name = "save.json"

        self.file_path = os.path.join(current_directory, self.data_file_name)

        if not os.path.exists(self.file_path):
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            print(f"Successfully created the file: {self.data_file_name}")
        else:
            print(f"File already exists")