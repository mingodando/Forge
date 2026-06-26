import customtkinter as ctk

from config import Config
from home_page import Home

class App:
    def __init__(self):
        #--- Main Window Activation ---#
        self.root = None

        #--- Other File Activation ---#
        self.home = Home()
        self.config = Config()

        #--- Navbar Widgets ---#
        self.title_home_button = None

#----- Starting Functions -----#
    def main(self):
        self.root = ctk.CTk()
        self.root.title("Forge")
        self.root.geometry("1280x720")

        self.home.create_home_page(self.root)
        self.setup_navbar()

        self.root.mainloop()

    def setup_navbar(self):
        self.home.navbar.columnconfigure(0, weight=1)
        self.title_home_button = ctk.CTkButton(self.home.navbar, text="Forge", command=lambda: self.home.on_click_home())
        self.title_home_button.grid(row=0, column=0, pady=10)

if __name__ == "__main__":
    app = App()
    app.main()