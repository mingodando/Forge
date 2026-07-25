import customtkinter as ctk

from backend.config import Config
from backend.start_setup import get_setup

_habit_instance = None

def get_habit():
    global _habit_instance
    if _habit_instance is None:
        _habit_instance = Habit()
    return _habit_instance

class Habit:
    def __init__(self):
        self.config = Config()
        self.config.main()
        self.setup = get_setup()

        self.frame = None

    def main(self):
        self.frame = ctk.CTkFrame(self.setup.content_frame, width=1120, height=680, fg_color=self.config.bg, corner_radius=0)
        self.frame.grid(row=0, column=0, sticky="nsew")
        self.frame.grid_propagate(False)

        placeholder = ctk.CTkLabel(self.frame, text="Habits", font=self.config.heading_font, text_color=self.config.text)
        placeholder.grid(row=0, column=0, padx=35, pady=35, sticky="nw")