WARN = "\033[93m[WARNING]"
INFO = "\033[92m[INFO]"
END = "\033[0m"


def compare_mapping_to_logs(fields_mapped_to, fields_used_in_events, diff_view):
    fields_without_usage = []

    for field in fields_mapped_to:
        if field not in fields_used_in_events:
            fields_without_usage.append(field)

    if diff_view:
        print(*fields_without_usage, sep="\n")
        return

    print("=" * 25 + " COMPARING MAPPED FIELDS TO FIELDS IN EVENTS " + "=" * 25)
    if fields_without_usage:
        print(f"{WARN} The following fields are mapped TO in your mapping, "
              f"but don't occur in any event:{END}")
        print(fields_without_usage)
        print(f"{WARN} Total amount of unused fields in mapping file: {len(fields_without_usage)}{END}\n")
    else:
        print(f"{INFO} All fields mapped to occur in at least one event.{END}\n")


def compare_mapping_to_rules(fields_mapped_from, fields_used_by_rules, diff_view):
    obsolete_mappings = []

    for field in fields_mapped_from:
        if field not in fields_used_by_rules:
            obsolete_mappings.append(field)

    if diff_view:
        print(*obsolete_mappings, sep="\n")
        return

    print("=" * 25 + " COMPARING MAPPED FIELDS TO FIELDS IN SIGMA RULES " + "=" * 25)
    if obsolete_mappings:
        print(f"{WARN} The following fields appear in your mapping, but are not used by any "
              f"Sigma rule:{END}")
        print(obsolete_mappings)
        print(f"{WARN} Total amount of obsolete fields in mapping: {len(obsolete_mappings)}{END}\n")
    else:
        print(f"{INFO} All fields present in the mapping are used by at least one Sigma rule.{END}\n")


def compare_rules_to_mapping(fields_used_by_rules, fields_mapped_from, diff_view):
    fields_without_mapping = []

    for field in fields_used_by_rules:
        if field not in fields_mapped_from:
            fields_without_mapping.append(field)

    if diff_view:
        print(*fields_without_mapping, sep="\n")
        return

    print("=" * 25 + " COMPARING FIELDS IN SIGMA RULES TO MAPPED FIELDS " + "=" * 25)
    if fields_without_mapping:
        print(f"{WARN} The following fields are used by a Sigma rule, but are not mapped FROM in your "
              f"mapping:{END}")
        print(fields_without_mapping)
        print(f"{WARN} Total amount of unmapped fields in Sigma rules: {len(fields_without_mapping)}{END}\n")
    else:
        print(f"{INFO} All fields used by Sigma are present in the mapping.{END}\n")
