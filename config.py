class Config:
    def __init__(self):
        self.bg_color = None
        self.navbar_color = None
        self.card_color = None
        self.topbar_color = None
        self.gold_accent_color = None
        self.text_color = None
        self.hover_color = None

        self.card_font = None

    def main(self):
        #--- Color ---#
        self.bg_color = "#1a1a1a"
        self.navbar_color = "#111111"
        self.card_color = "#222222"
        self.topbar_color = "#161616"
        self.gold_accent_color = "#c8a96e"
        self.text_color = "e0e0e0"
        self.hover_color = "2a2a2a"

        #--- Font ---#
        self.card_font = ("Segoe UI", 13, "bold")