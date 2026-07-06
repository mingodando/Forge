import customtkinter as ctk
from PIL import Image
import os

from config import Config
from setup import Setup

class App:
    def __init__(self):
        #--- Main Window Activation ---#
        self.root = None

        #--- OS Directory ---#
        self.current_directory = None

        #--- Other File Activation ---#
        self.setup = Setup()
        self.config = Config()
        self.config.main()

        #--- Topbar Widgets ---#
        self.currency_display = None

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
        self.root = ctk.CTk()
        self.root.title("Forge")
        self.root.geometry("1280x720")

        self.setup.create_home_page(self.root)
        self.setup.navbar.columnconfigure(0, weight=1)
        self.setup_navbar()
        self.setup_topbar()

        self.root.mainloop()

    def setup_topbar_images(self):
        pass

    def setup_topbar(self):
        self.setup.topbar.columnconfigure(0, weight=2)

        self.currency_display = ctk.CTkLabel(self.setup.topbar, height=50, width=150, text=f"Currency = ",
                                             font=self.config.card_font, fg_color=self.config.topbar_bg_color,
                                             bg_color=self.config.topbar_color, corner_radius=10)
        self.currency_display.grid(row=0, column=0, padx=10, pady=24, sticky="ens")

    def setup_navbar_images(self):
        self.current_directory = os.getcwd()

        self.forge_raw_image = Image.open(rf"{current_directory}\images\forge_logo.jpg")
        self.home_raw_image = Image.open(rf"{current_directory}\images\home_logo.jpg")
        self.quest_raw_image = Image.open(rf"{current_directory}\images\quest_logo.jpg")

        return self.forge_raw_image
    def setup_navbar(self):
        self.setup_navbar_images()

        self.forge_button_image = ctk.CTkImage(light_image = self.forge_raw_image,
                                              dark_image = self.forge_raw_image)

        self.home_button_image = ctk.CTkImage(light_image = self.home_raw_image,
                                              dark_image = self.home_raw_image)

        self.quest_button_image = ctk.CTkImage(light_image = self.quest_raw_image,)

        self.title_home_button = ctk.CTkButton(self.setup.navbar, height=60, width=60, text="",
                                               image=self.forge_button_image, command=lambda: self.setup.on_click_home(),
                                               fg_color=self.config.card_color, hover_color=self.config.hover_color)
        self.title_home_button.grid(row=0, column=0, pady=10)

        self.home_button = ctk.CTkButton(self.setup.navbar, height=60, width=60, text="Home", font=self.config.card_font,
                                         text_color=self.config.gold_accent_color, image=self.home_button_image,
                                         fg_color=self.config.card_color, hover_color=self.config.hover_color)
        self.home_button.grid(row=1, column=0, pady=10)

        self.quest_button = ctk.CTkButton(self.setup.navbar, height=60, width=60, text="Quest", font=self.config.card_font,
                                          text_color=self.config.gold_accent_color, image=self.quest_button_image,
                                          fg_color=self.config.card_color, hover_color=self.config.hover_color)
        self.quest_button.grid(row=2, column=0, pady=10)

if __name__ == "__main__":
    app = App()
    current_directory = os.getcwd()
    print(current_directory)
    app.main()