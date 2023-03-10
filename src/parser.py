def chainsaw_mapping(direction, mapping):
    fields_mapped = []
    for group in mapping["groups"]:
        # there is usually only one group, but theoretically more can be defined
        for field in group["fields"]:
            if type(field[direction]) is str:
                fields_mapped.append(field[direction])
            else:
                raise TypeError(f"Unexpected data type \"{type(field[direction])}\" for value \"{field[direction]}\" "
                                f"when parsing chainsaw mapping file.")
    fields_mapped = list(set(fields_mapped))
    fields_mapped.sort()
    return fields_mapped


def sigma_mapping(direction, mapping):
    # Fields mapped FROM are just they dict keys (aka strings),
    # while the fields mapped TO can be strings, dicts or lists
    mapping = mapping["fieldmappings"]
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
            elif data_type is dict:
                fields_mapped.extend(list(mapping[key].values()))
            elif data_type is list:
                fields_mapped.extend(mapping[key])
            else:
                raise TypeError(f"Unexpected data type \"{data_type}\" for value \"{mapping[key]}\" "
                                f"when parsing sigma mapping file.\n Expected str, dict or list.")

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
            raise TypeError(f"Unexpected data type \"{data_type}\" for value \"{current_dict[key]}\" "
                            f"when parsing log entries. Expected dict, str, int, list or bool.")
    return all_keys


def fields_from_list_in_rule(list_of_stuff):
    # Strings and dict values within Sigma rule are not desired, only get keys of dicts inside the list
    contained_fields = []
    for entry in list_of_stuff:
        if type(entry) is str:
            pass
        elif type(entry) is dict:
            keys = entry.keys()
            contained_fields.extend(list(keys))
        else:
            raise TypeError(f"Unexpected data type \"{type(entry)}\" for value \"{entry}\" "
                            f"when parsing sigma rule. Expected str or dict.")
    return contained_fields


def fields_from_rule(sigma_rule):
    fields_used = []
    detection_entries = list(sigma_rule["detection"].keys())
    for detection_entry in detection_entries:
        content = sigma_rule["detection"][detection_entry]
        data_type = type(content)
        if data_type is str:
            continue
        elif data_type is list:
            fields_within_entry = fields_from_list_in_rule(content)
            for field in fields_within_entry:
                fields_used.append(field.partition("|")[0])
        elif data_type is dict:
            fields_within_entry = list(content.keys())
            for field in fields_within_entry:
                fields_used.append(field.partition("|")[0])
        else:
            raise TypeError(f"Unexpected data type \"{data_type}\" for value \"{content}\" "
                            f"when parsing sigma rule. Expected str, list or dict.")
    return fields_used
