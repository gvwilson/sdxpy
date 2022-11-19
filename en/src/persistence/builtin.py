# [save]
def save(writer, thing):
    if isinstance(thing, bool):
        print(f"bool:{thing}", file=writer)

    elif isinstance(thing, float):
        print(f"float:{thing}", file=writer)

    elif isinstance(thing, int):
        print(f"int:{thing}", file=writer)

    # [extras]
    elif isinstance(thing, str):
        lines = thing.split("\n")
        print(f"str:{len(lines)}", file=writer)
        for line in lines:
            print(line, file=writer)

    # [save_list]
    elif isinstance(thing, list):
        print(f"list:{len(thing)}", file=writer)
        for item in thing:
            save(writer, item)
    # [/save_list]

    # [save_str]
    elif isinstance(thing, set):
        print(f"set:{len(thing)}", file=writer)
        for item in thing:
            save(writer, item)
    # [/save_str]

    # [save_dict]
    elif isinstance(thing, dict):
        print(f"dict:{len(thing)}", file=writer)
        for (key, value) in thing.items():
            save(writer, key)
            save(writer, value)
    # [/save_dict]

    # [/extras]
    else:
        raise ValueError(f"unknown type of thing {type(thing)}")
# [/save]

# [load]
def load(reader):
    line = reader.readline()[:-1]
    assert line, "Nothing to read"
    fields = line.split(":", maxsplit=1)
    assert len(fields) == 2, f"Badly-formed line {line}"
    key, value = fields

    if key == "bool":
        names = {"True": True, "False": False}
        assert value in names, f"Unknown Boolean {value}"
        return names[value]

    elif key == "float":
        return float(value)

    elif key == "int":
        return int(value)

    # [extras]
    # [load_str]
    elif key == "str":
        return "\n".join([reader.readline()[:-1] for _ in range(int(value))])
    # [/load_str]

    # [load_list]
    elif key == "list":
        return [load(reader) for _ in range(int(value))]
    # [/load_list]

    elif key == "set":
        return {load(reader) for _ in range(int(value))}

    elif key == "dict":
        result = {}
        for _ in range(int(value)):
            k = load(reader)
            v = load(reader)
            result[k] = v
        return result

    # [/extras]
    else:
        raise ValueError(f"unknown type of thing {line}")
# [/load]
