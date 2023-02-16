import click

import validate_mapping as val
from file_handler import fields_from_rules, fields_from_logs, fields_from_mapping


logs_file = "test_files/winlogbeat.jsonl"
mapping_file = "test_files/mapping.yml"
rules_dir = "test_files/rules/"

# TODO: Implement a proper CLI, until then crappy hardcode for testing


@click.group()
def cli():
    pass


@cli.command()
# @click.option('--path', prompt='Enter a path')
def mapping_to_logs():
    """Compare fields mapped [TO] to winlogbeat events"""
    fields_mapped_to = fields_from_mapping("to", mapping_file)
    fields_occurring_in_events = fields_from_logs(logs_file)

    val.compare_mapping_to_logs(fields_mapped_to, fields_occurring_in_events)


@cli.command()
def mapping_to_rules():
    """Compare fields mapped [FROM] to Sigma rules"""
    fields_mapped_from = fields_from_mapping("from", mapping_file)
    fields_used_by_rules = fields_from_rules(rules_dir)

    val.compare_mapping_to_rules(fields_mapped_from, fields_used_by_rules)


@cli.command()
def rules_to_mapping():
    """Compare fields in Sigma rules to fields mapped [FROM]"""
    fields_mapped_from = fields_from_mapping("from", mapping_file)
    fields_used_by_rules = fields_from_rules(rules_dir)

    val.compare_rules_to_mapping(fields_used_by_rules, fields_mapped_from)


if __name__ == '__main__':
    cli()
