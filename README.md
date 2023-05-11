# sigval
Sigma Mapping Validator

Easy-to-use tool for checking the completeness of a Sigma mapping file within the context of existing log files and rules.
Currently only supports mapping files written for the Sigma converter and Chainsaw, others will be added as needed.
A mapping file can be compared to either a logfile containing events or a directory containing Sigma rules,
resulting in three modes:
- `mapping-to-logs`: Check if all fields that are mapped ***to*** actually occur in any event,
potentially revealing incorrectly mapped fields.
- `mapping-to-rules`: Check if all fields that are mapped ***from*** actually occur in any Sigma rule,
revealing any obsolete mapped fields.
- `rules-to-mapping`: Check if all fields used by a set of Sigma rules are accounted for in the mapping,
revealing if any are missing.

Requires Python `v3.7` or higher.


## Usage
Clone this repo and install `sigval` in a virtual environment:
```shell
git clone git@github.com:Maspital/sigval.git
cd sigval
python -m venv "sigval" && pip install -e .
```

Run `tox` to verify functionality and `sigval --help`,
which will list the aforementioned three possible "modes" aka subcommands:
```
~$ sigval --help
Usage: sigval [OPTIONS] COMMAND [ARGS]...

  Tool for quickly checking the validity and completeness of a Sigma rule
  mapping

Options:
  --help  Show this message and exit.

Commands:
  mapping-to-logs   Compare fields mapped *TO* to events
  mapping-to-rules  Compare fields mapped *FROM* to Sigma rules
  rules-to-mapping  Compare fields in Sigma rules to fields mapped *FROM*
```

You can call `--help` again for each of those subcommands, for example:
```
~$ sigval mapping-to-rules --help
Usage: sigval mapping-to-rules [OPTIONS] MAPPING_FILE RULES_DIR

  Compare fields mapped *FROM* to Sigma rules

Options:
  -m, --mapping-type [chainsaw|sigma]
                                  Defines how sigval will parse the mapping
                                  file (default: sigma)
  -d, --diff-view                 Format output such that it can be used for
                                  further processing, omit info and warnings.
  --help                          Show this message and exit.
```
Please note that `sigval` expects the log file to be `.jsonl`, and the mapping file to be `.yml`.


## Options
- `-m, --mapping-type [chainsaw|sigma]`

    Default is Sigma.
    You will need to set this option if you use something other than a default sigma mapping so that sigval knows how to parse it.
    Currently available formats are chainsaw and sigma.
- `-d, --diff-view `

    By default, `sigval` will print some informational stuff, and all found fields will be output as a single "block".
    Setting this will instead cause `sigval` to print each new field in a single line and to omit all other output.
    This can then be used to pipe the output to somewhere else, for example to compare it using something like `diff`.


## Examples
You can use the rules, mappings and logs in `example_files` to test `sigval`.
- ```shell
  sigval mapping-to-logs example_files/sigma_winlogbeat_mapping.yml example_files/winlogbeat_logs.jsonl
    ```
  Produces a lot of fields that don't occur in any event because our log sample is rather small and a lot of fields are 
  incorrectly mapped.

- ```shell
  sigval mapping-to-logs example_files/chainsaw_winlogbeat_mapping.yml example_files/winlogbeat_logs.jsonl -m chainsaw
  ```
  Still some fields not occurring in any event, but a lot less due to the mapping being refined.

- ```shell
  sigval rules-to-mapping example_files/sigma_winlogbeat_mapping.yml example_files/sigma_rules/
  ```
  Shows that most fields used by our rules are present, but some (like those used by network rules) are missing.

- ```shell
  sigval rules-to-mapping example_files/sigma_zeek_mapping.yml example_files/sigma_rules/
  ```
  Complains about a lot more missing fields because now those used by windows rules are missing.
