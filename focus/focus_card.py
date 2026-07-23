import customtkinter as ctk
from tkinter import Canvas
from PIL import Image, ImageDraw, ImageFilter, ImageTk

from backend.config import Config
from pages.home_page import get_home

RING_SIZE = 180
HALO_FRACTION = 62 / 150
DISC_FRACTION = 40 / 150
SESSION_MINUTES = 25

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
        self.time_text = None
        self.status_text = None
        self.remaining_seconds = SESSION_MINUTES * 60
        self.timer_job = None

    def main(self):
        pass

    def create_ring(self):
        size = RING_SIZE
        center = size // 2

        self.canvas = Canvas(self.home_page.focus_frame, width=size, height=size, bg=self.config.card, highlightthickness=0)
        self.canvas.grid(row=0, column=0, rowspan=5, padx=20, pady=10, sticky="nsew")

        self.ring_image = self.render_glow_ring(size)
        self.canvas.create_image(center, center, image=self.ring_image)

        self.time_text = self.canvas.create_text(center, center - 12, text="25:00", fill=self.config.text, font=self.config.heading_font)
        self.status_text = self.canvas.create_text(center, center + 13, text="READY", fill=self.config.muted, font=self.config.body_font)

    @classmethod
    def render_glow_ring(cls, size):
        scale = 4
        px = size * scale
        center = px // 2
        img = Image.new("RGBA", (px, px), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        halo_radius = int(px * HALO_FRACTION)
        draw.ellipse((center - halo_radius, center - halo_radius, center + halo_radius, center + halo_radius), fill="#3d2c1c")
        img = img.filter(ImageFilter.GaussianBlur(radius=3 * scale))

        disc_radius = int(px * DISC_FRACTION)
        draw = ImageDraw.Draw(img)
        draw.ellipse((center - disc_radius, center - disc_radius, center + disc_radius, center + disc_radius), fill="#161009")
        img = img.filter(ImageFilter.GaussianBlur(radius=0.5 * scale))

        img = img.resize((size, size), Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(img)

    def create_onboard(self):
        self.zero_label = ctk.CTkLabel(self.home_page.focus_frame, width=160, height=10, text="ZERO-FRICTION START",
                                       font=self.config.label_font, text_color=self.config.ember, fg_color=self.config.card)
        self.zero_label.grid(row=0, column=1, pady=(15,0), sticky="nw")

        self.focus_label = ctk.CTkLabel(self.home_page.focus_frame, width=160, height=30, text="Focus Session",
                                        font=self.config.heading_font, text_color=self.config.text)
        self.focus_label.grid(row=1, column=1, sticky="nw")

        self.perk_label = ctk.CTkLabel(self.home_page.focus_frame, width=160, height=30, text="One tap and the forge fires. "
        "Finish a session and it auto-rolls XP,\n coins & materials — the fastest way to make studying pay.",
                                       font=self.config.body_font, text_color=self.config.text)
        self.perk_label.grid(row=2, column=1, sticky="n")

        self.start_button = ctk.CTkButton(self.home_page.focus_frame, text="▶  Start 25 min", font=self.config.button_font,
                                          fg_color=self.config.ember, hover_color="#d97a2e", text_color="#1a1006",
                                          corner_radius=12, width=160, height=40, command=self.start_focus_session)
        self.start_button.grid(row=3, column=1, pady=(10, 0), sticky="nw")

    def start_focus_session(self):
        self.canvas.itemconfig(self.status_text, text="FOCUSING")
        self.start_button.configure(text="⏸  Pause", command=self.pause_focus_session)
        self.tick()

    def pause_focus_session(self):
        self.canvas.itemconfig(self.status_text, text="PAUSED")
        self.start_button.configure(text="▶  Resume", command=self.start_focus_session)
        if self.timer_job is not None:
            self.canvas.after_cancel(self.timer_job)
            self.timer_job = None

    def tick(self):
        minutes, seconds = divmod(self.remaining_seconds, 60)
        self.canvas.itemconfig(self.time_text, text=f"{minutes:02d}:{seconds:02d}")

        if self.remaining_seconds <= 0:
            self.finish_focus_session()
            return

        self.remaining_seconds -= 1
        self.timer_job = self.canvas.after(1000, self.tick)

    def finish_focus_session(self):
        self.canvas.itemconfig(self.status_text, text="DONE")
        self.start_button.configure(text="▶  Start 25 min", command=self.start_focus_session)
        self.remaining_seconds = SESSION_MINUTES * 60
        self.timer_job = None