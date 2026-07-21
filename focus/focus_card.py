import customtkinter as ctk
from tkinter import Canvas

from backend.config import Config
from pages.home_page import get_home

class FocusCard:
    def __init__(self):
        self.config = Config()
        self.config.main()
        self.home_page = get_home()

        self.canvas = None
        self.zero_label = None
        self.focus_label = None

    def main(self):
        pass
    def create_ring(self):
        self.canvas = Canvas(self.home_page.focus_frame, width=150, height=150, bg=self.config.nav_tab_color, highlightthickness=0, )
        self.canvas.grid(row=0, column=0, rowspan=5, padx=20, pady=20, sticky="nsew")

        self.canvas.create_oval(10, 10, 140, 140, outline=self.config.well_color, width=8, fill="")

        self.canvas.create_arc(10, 10, 140, 140, start=90, extent=270, outline=self.config.faint_text, width=8, style="arc")

    def create_onboard(self):
        self.zero_label = ctk.CTkLabel(self.home_page.focus_frame, width=160, height=10, text="ZERO-FRICTION START", font=self.config.timer_font, text_color=self.config.ember_light, fg_color=self.config.nav_tab_color)
        self.zero_label.grid(row=0, column=1, pady=(15,0), sticky="new")

        self.focus_label = ctk.CTkLabel(self.home_page.focus_frame, width=160, height=30, text="Focus Session", font=self.config.levelup_font, text_color=self.config.primary_text)
        self.focus_label.grid(row=1, column=1, sticky="n")

