import customtkinter as ctk
from tkinter import Canvas
from PIL import Image, ImageDraw, ImageFilter, ImageTk

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
        self.ring_image = None
        self.perk_label = None

    def main(self):
        pass
    def create_ring(self):
        self.canvas = Canvas(self.home_page.focus_frame, width=150, height=150, bg=self.config.nav_tab_color, highlightthickness=0)
        self.canvas.grid(row=0, column=0, rowspan=5, padx=20, pady=20, sticky="nsew")

        self.ring_image = self.render_glow_ring()
        self.canvas.create_image(75, 75, image=self.ring_image)

        self.canvas.create_text(75, 63, text="25:00", fill=self.config.primary_text, font=self.config.levelup_font)
        self.canvas.create_text(75, 88, text="READY", fill=self.config.muted_text, font=self.config.page_font)

    @staticmethod
    def render_glow_ring():
        scale = 4
        size = 150 * scale
        center = size // 2
        img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        halo_radius = 62 * scale
        draw.ellipse((center - halo_radius, center - halo_radius, center + halo_radius, center + halo_radius), fill="#3d2c1c")
        img = img.filter(ImageFilter.GaussianBlur(radius=3 * scale))

        disc_radius = 40 * scale
        draw = ImageDraw.Draw(img)
        draw.ellipse((center - disc_radius, center - disc_radius, center + disc_radius, center + disc_radius), fill="#161009")
        img = img.filter(ImageFilter.GaussianBlur(radius=0.5 * scale))

        img = img.resize((150, 150), Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(img)

    def create_onboard(self):
        self.zero_label = ctk.CTkLabel(self.home_page.focus_frame, width=160, height=10, text="ZERO-FRICTION START",
                                       font=self.config.timer_font, text_color=self.config.ember_light, fg_color=self.config.nav_tab_color)
        self.zero_label.grid(row=0, column=1, pady=(15,0), sticky="new")

        self.focus_label = ctk.CTkLabel(self.home_page.focus_frame, width=160, height=30, text="Focus Session",
                                        font=self.config.levelup_font, text_color=self.config.primary_text)
        self.focus_label.grid(row=1, column=1, sticky="n")

        self.perk_label = ctk.CTkLabel(self.home_page.focus_frame, width=160, height=30, text="One tap and the forge fires. "
        "Finish a session and it auto-rolls XP,\n coins & materials — the fastest way to make studying pay.",
                                       font=self.config.page_font, text_color=self.config.primary_text)
        self.perk_label.grid(row=2, column=1, sticky="n")