import os

from backend.directory_setup import Directory
from currency import currency

directory = Directory()
current_directory = directory.quest_file()

os.makedirs(current_directory, exist_ok=True)

# for i in range(1,11):
#     file_name = f"test_{i}.txt"
#
#     new_directory = os.path.join(current_directory, file_name)
#
#     with open(new_directory, "w") as file:
#         file.write("hi")

files = sorted(
    os.listdir(current_directory),
    key=lambda name: int(os.path.splitext(name)[0].removeprefix("test_")),
)

for index, name in enumerate(files, start=1):
    old_path = os.path.join(current_directory, name)
    new_path = os.path.join(current_directory, f"test_{index}.txt")
    if old_path != new_path:
        os.rename(old_path, new_path)

numbers = [int(os.path.splitext(fname)[0].removeprefix("test_")) for fname in os.listdir(current_directory)]
largest_number = max(numbers, default=0)

print(largest_number)