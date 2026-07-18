import customtkinter as ctk
from PIL import Image
import os

from config import Config
from start_setup import Setup
from home_page import Home

class App:
    def __init__(self):
        #--- Main Window Activation ---#
        self.root = ctk.CTk()

        #--- OS Directory ---#
        self.current_directory = None

        #--- Other File Activation ---#
        self.setup = Setup()
        self.config = Config()
        self.home_page = Home()
        self.home_page.main()
        self.config.main()

        #--- Topbar Widgets ---#
        self.topbar_currency_display = None
        self.topbar_level_display = None
        self.xp_level_display = None

        #--- Navbar Widgets ---#
        self.title_home_button = None
        self.home_button = None
        self.quest_button = None

        #--- Images ---#
        self.forge_raw_image = None
        self.forge_button_image = None
        self.home_raw_image = None
        self.home_button_image = None
        self.quest_raw_image = None
        self.quest_button_image = None

#----- Starting Functions -----#
    def main(self):
        self.root.title("Forge")
        self.root.geometry("1280x720")

        self.setup.create_home_page(self.root)
        self.setup.navbar.columnconfigure(0, weight=1)
        self.setup_navbar()
        self.setup_topbar()

        self.root.mainloop()

    def setup_app(self):
        self.setup.setup_files()

    def setup_topbar_images(self):
        pass

    def setup_topbar(self):
        self.setup.topbar.columnconfigure(0, weight=1)
        self.setup.topbar.rowconfigure(1, weight=1)

        self.topbar_currency_display = ctk.CTkLabel(self.setup.topbar, height=40, width=150, text=f"Currency = ",
                                             font=self.config.body_font, fg_color=self.config.topbar_bg_color,
                                             bg_color=self.config.topbar_color, corner_radius=10)
        self.topbar_currency_display.grid(row=0, column=0, padx=10, pady=30, sticky="ens")

        self.topbar_level_display = ctk.CTkLabel(self.setup.topbar, height=40, width=100, text=f"Lv. ",
                                               font=self.config.body_font, fg_color=self.config.topbar_bg_color,
                                               bg_color=self.config.topbar_color, corner_radius=10)
        self.topbar_level_display.grid(row=0, column=1, padx=10, pady=30, sticky="ens")

        self.xp_level_display = ctk.CTkLabel(self.setup.topbar, height=40, width=150, text=f" XP",
                                             font=self.config.body_font, fg_color=self.config.topbar_bg_color,
                                             bg_color=self.config.topbar_color, corner_radius=10)
        self.xp_level_display.grid(row=0, column=2, padx=10, pady=30, sticky="ens")

    def setup_navbar_images(self):
        self.current_directory = self.setup.setup_directory()
        self.forge_raw_image = Image.open(rf"{self.current_directory}\images\forge_logo.jpg")
        self.home_raw_image = Image.open(rf"{self.current_directory}\images\home_logo.jpg")
        self.quest_raw_image = Image.open(rf"{self.current_directory}\images\quest_logo.jpg")

        return self.forge_raw_image

    def setup_navbar(self):
        self.setup_navbar_images()

        self.forge_button_image = ctk.CTkImage(light_image = self.forge_raw_image,
                                              dark_image = self.forge_raw_image)

        self.home_button_image = ctk.CTkImage(light_image = self.home_raw_image,
                                              dark_image = self.home_raw_image)

        self.quest_button_image = ctk.CTkImage(light_image = self.quest_raw_image,)

        self.title_home_button = ctk.CTkButton(self.setup.navbar, height=60, width=60, text="",
                                               command=lambda: self.setup.on_click_home(), image=self.forge_button_image,
                                               fg_color=self.config.navbar_color, hover_color=self.config.hover_color)
        self.title_home_button.grid(row=0, column=0, pady=10)

        self.home_button = ctk.CTkButton(self.setup.navbar, height=60, width=60, text="Home", font=self.config.title_font,
                                         text_color=self.config.gold_accent_color, image=self.home_button_image,
                                         fg_color=self.config.navbar_color, hover_color=self.config.hover_color,
                                         command=lambda: self.home_page.setup_home_page())
        self.home_button.grid(row=1, column=0, pady=10)

        self.quest_button = ctk.CTkButton(self.setup.navbar, height=60, width=60, text="Quest", font=self.config.title_font,
                                          text_color=self.config.gold_accent_color, image=self.quest_button_image,
                                          fg_color=self.config.navbar_color, hover_color=self.config.hover_color)
        self.quest_button.grid(row=2, column=0, pady=10)

if __name__ == "__main__":
    app = App()
    current_directory = app.setup_app()
    app.main()