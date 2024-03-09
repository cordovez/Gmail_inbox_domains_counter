import json


def count_items_in_file(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)

        return len(data)


file_path = "domain_count.json"
item_count = count_items_in_file(file_path)
print(f"Number of items in {file_path}: {item_count}")
