import customtkinter as ctk

class Config:
    def __init__(self):
        self.background_color = None
        self.navbar_color = None
        self.topbar_color = None
        self.gold_accent_color = None
        self.text_color = None
        self.hover_color = None
        self.card_inner_color = None
        self.border_color = None
        self.muted_text_color = None
        self.topbar_bg_color = None

        self.title_font = None
        self.stats_font = None
        self.card_header = None
        self.body_font = None
        self.label_font = None
        self.small_font = None
        self.brand_font = None

    def main(self):
        #--- Color ---#
        self.background_color = "#1a1a1a"
        self.navbar_color = "#111111"
        self.card_inner_color = "#222222"
        self.topbar_color = "#1e1e1e"
        self.topbar_bg_color = "#2a2a2a"
        self.gold_accent_color = "#c8a96e"
        self.text_color = "e0e0e0"
        self.hover_color = "#2a2a2a"
        self.border_color = "#2a2a2a"
        self.muted_text_color = "#555555"

        #--- Font ---#
        self.title_font = ctk.CTkFont("Segoe UI", 22, "bold")

        self.stats_font = ctk.CTkFont("Segoe UI", 26, "bold")

        self.card_header = ctk.CTkFont("Segoe UI", 15, "bold")

        self.body_font = ctk.CTkFont("Segoe UI", 13)

        self.label_font = ctk.CTkFont("Segoe UI", 11)

        self.small_font = ctk.CTkFont("Segoe UI", 12)

        self.brand_font  = ctk.CTkFont("Segoe UI", 19)