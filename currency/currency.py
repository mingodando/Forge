import customtkinter as ctk
import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAVE_PATH = os.path.join(BASE_DIR, "save.json")

class Currency:
    def __init__(self):
        pass
    def main(self):
        pass
    def read_file(self):
        with open(SAVE_PATH, "r") as f:
            return json.load(f)
    def get_currencies(self):
        data = self.read_file()
        currency = data.get("coins")
        print(currency)

if __name__ == "__main__":
    c = Currency()
    c.get_currencies()