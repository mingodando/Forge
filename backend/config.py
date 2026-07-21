import customtkinter as ctk
import os
import ctypes

# 1. Register the font file dynamically at runtime
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT_PATH = os.path.join(PROJECT_ROOT, "font", "SpaceGrotesk-Regular.ttf")

if os.path.exists(FONT_PATH):
    ctypes.windll.gdi32.AddFontResourceW(FONT_PATH)
else:
    print(f"Warning: Font file not found at {FONT_PATH}")


class Config:
    def __init__(self):
        #--- Font ---#
        self.heading_font = None
        self.label_font = None
        self.body_font = None

        #--- Surface Color ---#
        self.bg = None
        self.nav = None
        self.card = None
        self.card_hi = None

        #--- Accent Color ---#
        self.gold = None
        self.ember = None

        #--- Text Color ---#
        self.text = None
        self.muted = None

        #--- Feedback Color ---#
        self.green = None
        self.red = None

    def main(self):
        #--- Font ---#
        self.heading_font = ctk.CTkFont("Space Grotesk", 22, "bold")
        self.label_font = ctk.CTkFont("Space Grotesk", 15, "bold")
        self.body_font = ctk.CTkFont("Space Grotesk", 13, "bold")

        #--- Surface Color ---#
        self.bg = "#14100c"
        self.nav = "#0c0906"
        self.card = "#20170d"
        self.card_hi = "#181209"

        #--- Accent Color ---#
        self.gold = "#f2b45f"
        self.ember = "#f2903c"

        #--- Text Color ---#
        self.text = "#f0e9e0"
        self.muted = "#9a8f82"

        #--- Feedback Color ---#
        self.green = "#86c98b"
        self.red = "#e0817f"