import os
import yaml
import json


def fields_from_logs(winlogbeat_file):
    with open(winlogbeat_file, "r") as jsonl_file:
        winlogbeat = [json.loads(line) for line in jsonl_file]

    fields_used = []
    for event in winlogbeat:
        fields_used.extend(get_all_keys(event, ""))
    fields_used = list(set(fields_used))
    fields_used.sort()
    return fields_used


def fields_from_mapping(direction, mapping_file):
    # Direction is either "to" or "from"
    with open(mapping_file, "r") as file:
        mapping = yaml.safe_load(file)

    fields_mapped = []
    for field in mapping["groups"][0]["fields"]:
        fields_mapped.append(field[direction])
    fields_mapped = list(set(fields_mapped))
    fields_mapped.sort()
    return fields_mapped


def fields_from_rules(sigma_dir):
    fields_used = []
    for subdir, dirs, files in os.walk(sigma_dir):
        for file in files:
            with open(os.path.join(subdir, file)) as yaml_file:
                sigma_rule = yaml.safe_load(yaml_file)

            if not sigma_rule:
                # Can happen if the file is simply empty or fully commented out
                continue

            detection_entries = list(sigma_rule["detection"].keys())
            for detection_entry in detection_entries:
                data_type = type(sigma_rule["detection"][detection_entry])
                if data_type is str:
                    continue
                elif data_type is list:
                    fields_within_entry = get_fields_from_list(sigma_rule["detection"][detection_entry])
                    for field in fields_within_entry:
                        fields_used.append(field.partition("|")[0])
                elif data_type is dict:
                    fields_within_entry = list(sigma_rule["detection"][detection_entry].keys())
                    for field in fields_within_entry:
                        fields_used.append(field.partition("|")[0])
                else:
                    print(f"\033[91m[WARNING]\033[0m Unexpected data type: {data_type}")

    fields_used = list(set(fields_used))
    fields_used.sort()
    return fields_used


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
            print(f"\033[93m[WARNING]\033[0m Unexpected data type: {data_type}")
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
