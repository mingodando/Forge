import customtkinter as ctk

from home_page import Home

class App:
    def __init__(self):
        #--- Main Window Activation ---#
        self.root = None

        #--- Other File Activation ---#
        self.home = Home()

        #--- Navbar Widgets ---#
        self.title_home_button = None


    def main(self):
        self.root = ctk.CTk()
        self.root.title("Forge")
        self.root.geometry("1280x720")

        self.home.create_home_page(self.root)

        self.root.mainloop()

    def navbar(self):
        self.title_home_button = ctk.CTkButton(self.navbar, text="Forge", command=lambda: self.home.on_click_home())

if __name__ == "__main__":
    app = App()
    app.main()