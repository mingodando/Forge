from datetime import datetime
import json

class Time:
    def __init__(self):
        self.dt = None
        self.time_format = None
        self.current_time = None
        self.username = None
        self.time = None
        self.today_date = None

    def find_time(self):
        self.dt = datetime.now().time()

        self.time_format = self.dt.strftime("%H:%M")
        print(self.time_format)

        if "00:00" <= self.time_format < "11:59":
            return "Good Morning"
        elif "12:00" <= self.time_format < "16:59":
            return "Good Afternoon"
        else:
            return "Good Evening"

    def print_time(self):
        self.current_time = self.find_time()

        with open("save.json", "r") as file:
            data = json.load(file)

        self.username = data["username"]

        return f"{self.current_time}, {self.username}!"

    def print_date(self):
        self.today_date = datetime.now().strftime("%A")
        self.time = self.find_time().strip("Good ")

        return f"{self.today_date} {self.time}"
