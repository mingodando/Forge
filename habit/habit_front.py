import customtkinter as ctk
from tkinter import messagebox

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
        self.setup = get_setup()
        self.habit_page = get_habit()
        self.habit_back = get_habitback()
        self.slots_used = 0
        self.max_slots = self.habit_back.get_max_habits()

        self.title_label = None
        self.subtitle_label = None
        self.slots_frame = None
        self.slots_count_label = None
        self.slots_text_label = None
        self.new_habit_button = None

    def main(self):
        pass

    def setup_topbar(self):
        self.title_label = ctk.CTkLabel(self.habit_page.topbar_frame, text="Habtis", font=ctk.CTkFont("Space Grotesk", 28, "bold"), text_color=self.config.text)
        self.title_label.grid(row=0, column=0, padx=20, pady=(15, 0), sticky="w")

        self.subtitle_label = ctk.CTkLabel(self.habit_page.topbar_frame,
                                text="Daily Repeatables. Finish before midnight, or streaks will be gone. ")
        self.subtitle_label.grid(row=1, column=0, padx=20, pady=(0, 15), sticky="w")

        self.slots_frame = ctk.CTkFrame(self.habit_page.topbar_frame, fg_color=self.config.bg)
        self.slots_frame.grid(row=0, column=1, rowspan=2, padx=(20, 2), pady=15, sticky="e")

        self.slots_count_label = ctk.CTkLabel(self.slots_frame, text=f"{self.slots_used} / {self.max_slots}", font=self.config.body_font, text_color=self.config.gold)
        self.slots_count_label.grid(row=0, column=0, sticky="e")

        self.slots_text_label = ctk.CTkLabel(self.slots_frame, text=" slots used", font=self.config.body_font, text_color=self.config.muted)
        self.slots_text_label.grid(row=0, column=1, padx=(0,4), sticky="e")


        self.new_habit_button = ctk.CTkButton(self.habit_page.topbar_frame, text="+ New Habit", font=self.config.button_font,
                                    fg_color=self.config.ember, hover_color=self.config.gold,
                                    text_color=self.config.nav, corner_radius=20, command=lambda: self.habit_back.create_new_habit())