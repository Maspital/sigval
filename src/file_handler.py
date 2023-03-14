import os
import yaml
import json

import parser

ERR = "\033[91m[ERROR]"
END = "\033[0m"


def fields_from_logs(winlogbeat_file):
    with open(winlogbeat_file, "r") as jsonl_file:
        winlogbeat = [json.loads(line) for line in jsonl_file]

    fields_used = []
    for event in winlogbeat:
        fields_used.extend(parser.get_all_keys(event, ""))
    fields_used = list(set(fields_used))
    fields_used.sort()

    if not fields_used:
        print_error("log file")
    return fields_used


def fields_from_mapping(direction, mapping_file, mapping_type):
    # Direction is either "to" (field used by Sigma rule) or "from" (field that should appear in logs)
    with open(mapping_file, "r") as file:
        mapping = yaml.safe_load(file)

    fields_mapped = []
    match mapping_type:
        case "chainsaw":
            fields_mapped = parser.chainsaw_mapping(direction, mapping)
        case "sigma":
            fields_mapped = parser.sigma_mapping(direction, mapping)

    if not fields_mapped:
        print_error("mapping file")
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
            fields_used.extend(parser.fields_from_rule(sigma_rule))

    fields_used = list(set(fields_used))
    fields_used.sort()

    if not fields_used:
        print_error("Sigma rule directory")
    return fields_used


def print_error(cause):
    print(f"{ERR} No fields were obtained from the provided {cause}, results will likely be incorrect. "
          f"Are you sure this is the correct path?{END}\n")
