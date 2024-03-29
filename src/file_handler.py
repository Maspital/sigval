import os
import yaml
import json

import content_parser


def fields_from_logs(winlogbeat_file):
    with open(winlogbeat_file, "r") as jsonl_file:
        winlogbeat = [json.loads(line) for line in jsonl_file]

    fields_used = []
    for event in winlogbeat:
        fields_used.extend(content_parser.get_all_keys(event, ""))
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
    if mapping_type == "chainsaw":
        fields_mapped = content_parser.chainsaw_mapping(direction, mapping)
    elif mapping_type == "sigma":
        fields_mapped = content_parser.sigma_mapping(direction, mapping)

    if not fields_mapped:
        print_error("mapping file")
    return fields_mapped


def fields_from_rules(sigma_dir):
    fields_used = []
    for subdir, dirs, files in os.walk(sigma_dir):
        for file in files:
            if not file.endswith(".yml"):
                continue

            with open(os.path.join(subdir, file)) as yaml_file:
                sigma_rule = yaml.safe_load(yaml_file)

            if not sigma_rule:
                # Can happen if the file is simply empty or fully commented out
                continue
            fields_used.extend(content_parser.fields_from_rule(sigma_rule))

    fields_used = list(set(fields_used))
    fields_used.sort()

    if not fields_used:
        print_error("Sigma rule directory")
    return fields_used


def print_error(cause):
    print(f"\033[91m[WARNING] No fields were obtained from the provided {cause}, results will likely be incorrect. "
          f"Are you sure this is the correct path?\033[0m\n")
