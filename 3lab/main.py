def traverse_structure(obj, depth=0, path=None, history=None):
    if path is None:
        path = []
    if history is None:
        history = []

    if isinstance(obj, dict):
        for key, value in obj.items():
            new_path = path + [key]
            history.append({
                'depth': depth,
                'key_or_index': key,
                'value': value,
                'path': new_path
            })
            traverse_structure(value, depth + 1, new_path, history)
    elif isinstance(obj, list):
        for index, item in enumerate(obj):
            new_path = path + [index]
            history.append({
                'depth': depth,
                'key_or_index': index,
                'value': item,
                'path': new_path
            })
            traverse_structure(item, depth + 1, new_path, history)
    return history

if __name__ == "__main__":
       main()
