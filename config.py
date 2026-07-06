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

        self.body_font = None
        self.card_color = None
        self.card_font = None
        self.body_color = None
        self.stat_font = None
        self.badge_text = None

    def main(self):
        #--- Color ---#
        self.background_color = "#1a1a1a"
        self.navbar_color = "#111111"
        self.card_inner_color = "#1a1a1a"
        self.topbar_color = "#1e1e1e"
        self.topbar_bg_color = "#2a2a2a"
        self.gold_accent_color = "#c8a96e"
        self.text_color = "e0e0e0"
        self.hover_color = "#2a2a2a"
        self.border_color = "#2a2a2a"
        self.muted_text_color = "#555555"

        #--- Font ---#
        self.card_font = ("Segoe UI", 13, "bold")
        self.card_color = "#222222"

        self.body_font = ("Segoe UI", 13)
        self.body_color = "#e0e0e0"

        self.stat_font = ("Segoe UI", 22, "bold")

        self.badge_text = ("Segoe UI", 11)