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
        self.focus_frame = ctk.CTkFrame(self.setup.content_frame, width=500, height=500, fg_color="red")
        self.focus_frame.grid(row=0, column=0, sticky="nw")

        self.focus_frame.tkraise()