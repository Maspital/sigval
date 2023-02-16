def compare_mapping_to_logs(fields_mapped_to, fields_used_in_events):
    print("=" * 25 + " COMPARING MAPPED FIELDS TO FIELDS IN EVENTS " + "=" * 25)
    fields_without_usage = []

    for field in fields_mapped_to:
        if field not in fields_used_in_events:
            fields_without_usage.append(field)

    if fields_without_usage:
        print("\033[93m[WARNING] The following fields are mapped TO in your mapping, "
              "but don't occur in any event:\033[0m")
        print(fields_without_usage)
        print(f"\033[93m[WARNING] Total amount of unused fields in mapping file: {len(fields_without_usage)}\033[0m\n")
    else:
        print("\033[92m[INFO] All fields mapped to occur in at least one event.\033[0m\n")


def compare_rules_to_mapping(fields_used_by_rules, fields_mapped_from):
    print("=" * 25 + " COMPARING FIELDS IN SIGMA RULES TO MAPPED FIELDS " + "=" * 25)
    fields_without_mapping = []

    for field in fields_used_by_rules:
        if field not in fields_mapped_from:
            fields_without_mapping.append(field)

    if fields_without_mapping:
        print("\033[93m[WARNING] The following fields are used by a Sigma rule, but are not mapped FROM in your "
              "mapping:\033[0m")
        print(fields_without_mapping)
        print(f"\033[93m[WARNING] Total amount of unmapped fields in Sigma rules: {len(fields_without_mapping)}\033[0m\n")
    else:
        print("\033[92m[INFO] All fields used by Sigma are present in the mapping.\033[0m\n")


def compare_mapping_to_rules(fields_mapped_from, fields_used_by_rules):
    print("=" * 25 + " COMPARING MAPPED FIELDS TO FIELDS IN SIGMA RULES " + "=" * 25)
    obsolete_mappings = []
    for field in fields_mapped_from:
        if field not in fields_used_by_rules:
            obsolete_mappings.append(field)

    if obsolete_mappings:
        print("\033[93m[WARNING] The following fields appear in your mapping, but are not used by any "
              "Sigma rule:\033[0m")
        print(obsolete_mappings)
        print(f"\033[93m[WARNING] Total amount of obsolete fields in mapping: {len(obsolete_mappings)}\033[0m\n")
    else:
        print("\033[92m[INFO] All fields present in the mapping are used by at least one Sigma rule.\033[0m\n")
