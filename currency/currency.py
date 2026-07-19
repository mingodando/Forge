import customtkinter as ctk
import datetime
import os

from backend.directory_setup import Directory

class Currency:
    def __init__(self):
        self.directory = Directory()

    def main(self):
        pass

    def read_balance(self):
        path = self.directory.balance_file()
        if not os.path.exists(path):
            self.write_balance(0)
        with open(path, "r") as f:
            return int(f.read().strip() or 0)

    def write_balance(self, amount):
        path = self.directory.balance_file()
        with open(path, "w") as f:
            f.write(str(amount))

    def get_currencies(self):
        return self.read_balance()

    def log_change(self, amount):
        path = self.directory.history_file()
        timestamp = datetime.datetime.now().isoformat()
        with open(path, "a") as f:
            f.write(f"{timestamp},{amount}\n")

    def currency_change(self, amount):
        balance = self.read_balance() + amount
        self.write_balance(balance)
        self.log_change(amount)
        return balance

    def get_today_flow(self):
        path = self.directory.history_file()
        today = datetime.date.today()
        gained = 0
        spent = 0
        if os.path.exists(path):
            with open(path, "r") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    timestamp_str, amount_str = line.split(",")
                    entry_date = datetime.datetime.fromisoformat(timestamp_str).date()
                    if entry_date == today:
                        amount = int(amount_str)
                        if amount >= 0:
                            gained += amount
                        else:
                            spent += amount
        return {"in": gained, "out": abs(spent), "net": gained + spent}


if __name__ == "__main__":
    c = Currency()
    print(c.get_currencies())