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


def logprep_mapping(direction, mapping_file):
    print("Parsing for logprep mapping not yet implemented. Exiting...")
    exit(1)


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
