import os
import yaml
import json

import parser


def fields_from_logs(winlogbeat_file):
    with open(winlogbeat_file, "r") as jsonl_file:
        winlogbeat = [json.loads(line) for line in jsonl_file]

    fields_used = []
    for event in winlogbeat:
        fields_used.extend(parser.get_all_keys(event, ""))
    fields_used = list(set(fields_used))
    fields_used.sort()
    return fields_used


def fields_from_mapping(direction, mapping_file, mapping_type):
    # Direction is either "to" (field used by Sigma rule) or "from" (field that should appear in logs)
    fields_mapped = []
    match mapping_type:
        case "chainsaw":
            fields_mapped = parser.chainsaw_mapping(direction, mapping_file)
        case "logprep":
            parser.logprep_mapping(direction, mapping_file)

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
                    fields_within_entry = parser.get_fields_from_list(sigma_rule["detection"][detection_entry])
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
