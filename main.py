import customtkinter as ctk
from PIL import Image

from config import Config
from home_page import Home

class App:
    def __init__(self):
        #--- Main Window Activation ---#
        self.root = None

        #--- Other File Activation ---#
        self.home = Home()
        self.config = Config()
        self.config.main()

        #--- Navbar Widgets ---#
        self.title_home_button = None
        self.home_button = None

        #--- Images ---#
        self.forge_raw_image = None
        self.forge_button_image = None
        self.home_raw_image = None
        self.home_button_image = None

#----- Starting Functions -----#
    def main(self):
        self.root = ctk.CTk()
        self.root.title("Forge")
        self.root.geometry("1280x720")

        self.home.create_home_page(self.root)
        self.home.navbar.columnconfigure(0, weight=1)
        self.setup_navbar()

        self.root.mainloop()

    def setup_images(self):
        self.forge_raw_image = Image.open(r"E:\Programming\PycharmProjectss\ForgeApp\images\forge_logo.jpg")
        self.home_raw_image = Image.open(r"E:\Programming\PycharmProjectss\ForgeApp\images\home_logo.jpg")

        return self.forge_raw_image
    def setup_navbar(self):
        self.setup_images()

        self.forge_button_image = ctk.CTkImage(light_image = self.forge_raw_image,
                                              dark_image = self.forge_raw_image)

        self.home_button_image = ctk.CTkImage(light_image = self.home_raw_image,
                                              dark_image = self.home_raw_image)

        self.title_home_button = ctk.CTkButton(self.home.navbar, height=60, width=60, text="Forge", image=self.forge_button_image, command=lambda: self.home.on_click_home(), fg_color=self.config.card_color)
        self.title_home_button.grid(row=0, column=0, pady=10)

        self.home_button = ctk.CTkButton(self.home.navbar, height=60, width=60, text="Home", font=self.config.card_font, text_color=self.config.gold_accent_color, image=self.home_button_image, fg_color=self.config.card_color)
        self.home_button.grid(row=1, column=0, pady=10)

if __name__ == "__main__":
    app = App()
    app.main()