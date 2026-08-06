import customtkinter as ctk

from backend.config import Config
from backend.start_setup import get_setup
from pages.habit_page import get_habit
from habit.habit_back import get_habitback

_habitfront_instance = None

def get_habitfront():
    global _habitfront_instance
    if _habitfront_instance is None:
        _habitfront_instance = HabitFront()
    return _habitfront_instance

class HabitFront:
    def __init__(self):
        self.config = Config()
        self.config.main()
        self.setup = get_setup()
        self.habit_page = get_habit()
        self.habit_back = get_habitback()

        self.title_label = None
        self.subtitle_label = None
        self.new_habit_button = None

    def main(self):
        pass

    def setup_topbar(self):
        self.title_label = ctk.CTkLabel(self.habit_page.topbar_frame, text="Habits", font=ctk.CTkFont("Space Grotesk", 28, "bold"), text_color=self.config.text)
        self.title_label.grid(row=0, column=0, padx=20, pady=(15, 0), sticky="w")

        self.subtitle_label = ctk.CTkLabel(self.habit_page.topbar_frame,
                                text="Daily repeatables · streaks reset at midnight", font=self.config.body_font, text_color=self.config.muted)
        self.subtitle_label.grid(row=1, column=0, padx=20, pady=(0, 15), sticky="w")

        self.new_habit_button = ctk.CTkButton(self.habit_page.topbar_frame, text="+ New habit", font=self.config.button_font,
                                              fg_color=self.config.ember, hover_color=self.config.gold,
                                              text_color=self.config.nav, corner_radius=20, command=lambda: self.habit_back.create_habit())
        self.new_habit_button.grid(row=0, column=1, rowspan=2, padx=(0, 30), pady=15, sticky="e")

        self.habit_page.topbar_frame.grid_columnconfigure(1, weight=1)