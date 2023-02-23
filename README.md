# sigval
Sigma Mapping Validator

Easy-to-use tool for checking the completeness and validity of a Sigma mapping file.
Currently only supports mapping files written for Chainsaw, but others (e.g., logprep) will be added in the near future.
A mapping file can be compared to either a logfile containing winlogbeat events or a directory containing Sigma rules,
resulting in three modes:
- `mapping-to-logs`: Check if all fields that are mapped ***to*** actually occur in any winlogbeat event,
potentially revealing incorrectly mapped fields.
- `mapping-to-rules`: Check if all fields that are mapped ***from*** actually occur in any Sigma rule,
revealing any obsolete mapped fields.
- `rules-to-mapping`: Check if all fields used by a set of Sigma rules are accounted for in the mapping,
revealing if any are missing.


## Usage
Clone this repo and install `sigval` directly or, if you prefer, in a virtual environment:
```shell
git clone git@github.com:Maspital/sigval.git
cd sigval
pip install -e .
```

Run `sigval --help`, which will list the aforementioned three possible "modes" aka subcommands:
```
~$ sigval --help
Usage: sigval [OPTIONS] COMMAND [ARGS]...

  Tool for quickly checking the validity and completeness of a Sigma rule
  mapping

Options:
  --help  Show this message and exit.

Commands:
  mapping-to-logs   Compare fields mapped *TO* to winlogbeat events
  mapping-to-rules  Compare fields mapped *FROM* to Sigma rules
  rules-to-mapping  Compare fields in Sigma rules to fields mapped *FROM*
```

You can call `--help` again for each of those subcommands, for example:
```
~$ sigval mapping-to-rules --help
Usage: sigval mapping-to-rules [OPTIONS] MAPPING_FILE RULES_DIR

  Compare fields mapped *FROM* to Sigma rules

Options:
  -m, --mapping-type [chainsaw|logprep]
                                  Defines how sigval will parse the mapping
                                  file (default: chainsaw)
  -d, --diff-view                 Format output such that it can be used for
                                  further processing, omit info and warnings.
  --help                          Show this message and exit.
```
Please note that `sigval` expects the winlogbeat file to be `.jsonl`, and the mapping file to be `.yml`.


## Options
- `-m, --mapping-type [chainsaw|logprep]`

    Default is chainsaw.
    You will need to set this option if you use something other than a chainsaw mapping so that sigval knows how to parse it.
    Currently available formats are chainsaw and logprep.
- `-d, --diff-view `

    By default, `sigval` will print some informational stuff, and all found fields will be output as a single "block".
    Setting this will instead cause `sigval` to print each new field in a single line and to omit all other output.
    This can then be used to pipe the output to somewhere else, for example to compare it using something like `diff`.


## Examples

```shell
sigval mapping-to-logs path/to/mapping.yml path/to/winlogbeat.jsonl
```

```shell
sigval rules-to-mapping path/to/mapping.yml dir/containing/rules/ -d
```
