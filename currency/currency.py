import customtkinter as ctk
import json
import os

from backend.directory_setup import Directory

class Currency:
    def __init__(self):
        self.directory = Directory()

    def main(self):
        pass
    def read_file(self):
        path = self.directory.main()
        with open(path, "r") as f:
            return json.load(f)
    def get_currencies(self):
        data = self.read_file()
        currency = data.get("coins")
        print(currency)

if __name__ == "__main__":
    c = Currency()
    c.get_currencies()