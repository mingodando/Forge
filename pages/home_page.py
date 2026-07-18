import customtkinter as ctk

from backend.config import Config
from backend.start_setup import Setup

class Home:
    def __init__(self, setup):
        self.config = Config()
        self.config.main()
        self.setup = setup

        #--- Widgets ---#
        self.level_label = None

        #--- Frames ---#
        self.focus_frame = None

    def main(self):
        self.focus_frame = ctk.CTkFrame(self.setup.content_frame, width=1050, height=150, fg_color=self.config.home_color, corner_radius=30)
        self.focus_frame.grid(row=0, column=0, padx=35, sticky="nsew")

        self.focus_frame.tkraise()