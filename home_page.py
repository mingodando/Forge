import customtkinter as ctk

from config import Config

class Home:
    def __init__(self):
        self.config = Config()
        self.config.main()

        self.root = None
        self.topbar = None
        self.navbar = None
        self.content_frame = None

#----- Starting Functions -----#
    def create_home_page(self, root):
        self.root = root
        self.topbar = ctk.CTkFrame(self.root, width=1160, height=100)
        self.topbar.grid(row=0, column=1, sticky="n")
        self.topbar.configure(fg_color=self.config.topbar_color)
        self.navbar = ctk.CTkFrame(self.root, width=120, height=720)
        self.navbar.grid(row=0, column=0, rowspan=2, sticky="ns")
        self.navbar.configure(fg_color=self.config.navbar_color)
        self.navbar.grid_propagate(False)
        self.content_frame = ctk.CTkFrame(self.root, width=1160, height=620)
        self.content_frame.grid(row=1, column=1, sticky="nsew")
        self.content_frame.configure(fg_color=self.config.bg_color)

    def on_click_home(self):
        self.content_frame.tkraise()


