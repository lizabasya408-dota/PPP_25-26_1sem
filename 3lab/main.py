if __name__ == "__main__":
    
def traverse_structure(data, path=None, depth=0, history=None):
    if path is None:
        path = []
    if history is None:
        history = []

    if isinstance(data, dict):
        for key, value in data.items():
            new_path = path + [key]
            traverse_structure(value, new_path, depth + 1, history)
    elif isinstance(data, list):
        for index, value in enumerate(data):
            new_path = path + [index]
            traverse_structure(value, new_path, depth + 1, history)
    else:
        record = {
            "depth": depth,
            "path": path,
            "value": data
        }
        history.append(record)

    return history

sample_json = {
    "id": 101,
    "info": {
        "name": "Alice",
        "skills": ["Python", "Git"],
        "location": {
            "city": "Wonderland",
            "coords": [55.1, 33.2]
        }
    },
    "is_active": True
}

result = traverse_structure(sample_json)

for item in result:
    print(item)
