import click

from validate_mapping import compare_mapping_to_logs, compare_rules_to_mapping, compare_mapping_to_rules
from file_handler import fields_from_rules, fields_from_logs, fields_from_mapping


_global_options = [
    click.option('--mapping-type', "-m", type=click.Choice(['chainsaw', 'sigma'], case_sensitive=False),
                 default="sigma", help="Defines how sigval will parse the mapping file (default: sigma)"),
    click.option("--diff-view", "-d", is_flag=True, default=False,
                 help="Format output such that it can be used for further processing, omit info and warnings."),
]


@click.group()
def cli():
    """Tool for quickly checking the validity and completeness of a Sigma rule mapping"""
    pass


def global_options(func):
    for option in reversed(_global_options):
        func = option(func)
    return func


@cli.command()
@global_options
@click.argument("mapping_file")
@click.argument("winlogbeat_file")
def mapping_to_logs(mapping_type, diff_view, mapping_file, winlogbeat_file):
    """Compare fields mapped *TO* to winlogbeat events"""
    prelude(diff_view)
    fields_mapped_to = fields_from_mapping("to", mapping_file, mapping_type)
    fields_occurring_in_events = fields_from_logs(winlogbeat_file)
    compare_mapping_to_logs(fields_mapped_to, fields_occurring_in_events, diff_view)


@cli.command()
@global_options
@click.argument("mapping_file")
@click.argument("rules_dir")
def mapping_to_rules(mapping_type, diff_view, mapping_file, rules_dir):
    """Compare fields mapped *FROM* to Sigma rules"""
    prelude(diff_view)
    fields_mapped_from = fields_from_mapping("from", mapping_file, mapping_type)
    fields_used_by_rules = fields_from_rules(rules_dir)
    compare_mapping_to_rules(fields_mapped_from, fields_used_by_rules, diff_view)


@cli.command()
@global_options
@click.argument("mapping_file")
@click.argument("rules_dir")
def rules_to_mapping(mapping_type, diff_view, mapping_file, rules_dir):
    """Compare fields in Sigma rules to fields mapped *FROM*"""
    prelude(diff_view)
    fields_mapped_from = fields_from_mapping("from", mapping_file, mapping_type)
    fields_used_by_rules = fields_from_rules(rules_dir)
    compare_rules_to_mapping(fields_used_by_rules, fields_mapped_from, diff_view)


def prelude(diff_view):
    logo = r"""
       _____ _      _    __      __
      / ___/(_)___ | |  / /___ _/ /
      \__ \/ / __ `/ | / / __ `/ / 
     ___/ / / /_/ /| |/ / /_/ / /  
    /____/_/\__, / |___/\__,_/_/   
           /____/  v1.0.0                    
        """
    if not diff_view:
        print(logo)


if __name__ == '__main__':
    cli()
