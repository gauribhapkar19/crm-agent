import os

file_path = "../../data/email-data-advanced.json"

print("Reading:", os.path.abspath(file_path))

with open(file_path, "r") as f:
    print("File opened successfully")

    content = f.read()

    print("First 200 chars:")
    print(content[:200])