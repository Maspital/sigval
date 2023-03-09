import yaml
from sys import exit


def chainsaw_mapping(direction, mapping_file):
    with open(mapping_file, "r") as file:
        mapping = yaml.safe_load(file)

    fields_mapped = []
    for group in mapping["groups"]:
        # there is usually only one group, but theoretically more can be defined
        for field in group["fields"]:
            fields_mapped.append(field[direction])
    fields_mapped = list(set(fields_mapped))
    fields_mapped.sort()
    return fields_mapped


def sigma_mapping(direction, mapping_file):
    # Fields mapped FROM are just they dict keys (aka strings),
    # while the fields mapped TO can be strings, dicts or lists
    with open(mapping_file, "r") as file:
        mapping = yaml.safe_load(file)["fieldmappings"]

    fields_mapped = []
    if direction == "from":
        for field in mapping:
            if type(field) is str:
                fields_mapped.append(field)
    elif direction == "to":
        keys = list(mapping.keys())
        for key in keys:
            data_type = type(mapping[key])
            if data_type is str:
                fields_mapped.append(mapping[key])
            if data_type is dict:
                fields_mapped.extend(list(mapping[key].values()))
            if data_type is list:
                fields_mapped.extend(mapping[key])
            else:
                print(f"\033[91m[WARNING]\033[0m Unexpected data type: {data_type}")

    fields_mapped = list(set(fields_mapped))
    fields_mapped.sort()
    return fields_mapped


def get_all_keys(current_dict, previous_key):
    all_keys = []
    keys = list(current_dict.keys())
    for key in keys:
        data_type = type(current_dict[key])
        if data_type is dict:
            all_keys.extend(
                get_all_keys(current_dict[key], f"{previous_key}{key}."))
        elif data_type in [str, int, list, bool]:
            all_keys.append(f"{previous_key}{key}")
        else:
            print(f"\033[91m[WARNING]\033[0m Unexpected data type: {data_type}")
    return all_keys


def get_fields_from_list(list_of_stuff):
    # Strings and dict values are not desired, only get keys of dicts inside the list
    contained_fields = []
    for entry in list_of_stuff:
        if type(entry) is str:
            pass
        elif type(entry) is dict:
            keys = entry.keys()
            contained_fields.extend(list(keys))
        else:
            print(f"\033[91m[WARNING]\033[0m Unexpected data type: {type(entry)}")
    return contained_fields
