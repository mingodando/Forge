import customtkinter as ctk
from tkinter import Canvas

from backend.config import Config

class FocusCard:
    def __init__(self):
        self.config = Config()

    def main(self):
        pass
    def create_ring(self, focus_frame):
        self.canvas = Canvas(focus_frame, width=150, height=150, bg=self.config.nav_tab_color, highlightthickness=0)
        self.canvas.grid(row=0, column=0)

        self.canvas.create_oval(10, 10, 140, 140, outline=self.config.disabled_text, width=8, fill="")

        self.canvas.create_arc(10, 10, 140, 140, start=90, extent=270, outline=self.config.faint_text, width=8, style="arc")