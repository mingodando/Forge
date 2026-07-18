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
        self.levelup_font = None
        self.timer_font = None
        self.page_font = None
        self.section_font = None
        self.big_stat_font = None
        self.focused_today_font = None
        self.hero_sub_font = None
        self.popup_font = None
        self.brand_font = None
        self.card_font = None
        self.body_font = None
        self.small_font = None
        self.eyebrow_font = None

        #--- Color ---#
        self.background_color = None
        self.window_color = None
        self.sidebar_color = None
        self.card_color = None
        self.well_color = None
        self.nav_tab_color = None
        self.navhover_color = None
        self.amber = None
        self.ember_orange = None
        self.ember_light = None
        self.amber_muted = None
        self.home_color = None

        #--- Text Color ---#
        self.primary_text = None
        self.muted_text = None
        self.faint_text = None
        self.disabled_text = None

        #--- Progress Color ---#
        self.start_color = None
        self.mid_color = None
        self.end_color = None

        #--- Feedback Color ---#
        self.success_color = None
        self.toast_color = None
        self.warning_color = None
        self.bright_color = None


    def main(self):
        #--- FONT ---#
        self.levelup_font = ctk.CTkFont("Space Grotesk", 22, "bold")
        self.timer_font = ctk.CTkFont("Space Grotesk", 15, "bold")
        self.page_font = ctk.CTkFont("Space Grotesk", 13, "bold")
        self.section_font = ctk.CTkFont("Space Grotesk", 13,  "bold")
        self.big_stat_font = ctk.CTkFont("Space Grotesk", 14, "bold")
        self.focused_today_font = ctk.CTkFont("Space Grotesk", 13, "bold")
        self.hero_sub_font = ctk.CTkFont("Space Grotesk", 12,  "bold")
        self.popup_font = ctk.CTkFont("Space Grotesk", 12,  "bold")
        self.brand_font = ctk.CTkFont("Space Grotesk", 12,  "bold")
        self.card_font = ctk.CTkFont("Space Grotesk", 10,  "bold")
        self.body_font = ctk.CTkFont("Space Grotesk", 9)
        self.small_font = ctk.CTkFont("Space Grotesk", 10,  "bold")
        self.eyebrow_font = ctk.CTkFont("Space Grotesk", 10)

        #--- Color ---#
        self.background_color = "#0a0705"
        self.window_color = "#14100c"
        self.sidebar_color = "#0c0906"
        self.card_color = "#1a130c"
        self.well_color ="#0f0b07"
        self.nav_tab_color = "#20180f"
        self.navhover_color = "#181209"

        self.amber = "#f2b45f"
        self.home_color = "#20170D"
        self.ember_orange = "#e0763c"
        self.ember_light = "#f2903c"
        self.amber_muted = "#c99a5f"
        #--- Text Color ---#
        self.primary_text = "#f0e9e0"
        self.muted_text = "#9a8f82"
        self.faint_text = "#5a4a38"
        self.disabled_text = "#6a5c48"

        #--- Progress Color ---#
        self.start_color = "#7a3016"
        self.mid_color = "#e0763c"
        self.end_color = "#f2b45f"

        #--- Feedback Color ---#
        self.success_color = "#86c98b"
        self.toast_color = "#182a18"
        self.warning_color = "#e0817f"
        self.bright_color = "#ff8a80"