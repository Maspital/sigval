import unittest
import yaml

from parser import chainsaw_mapping, sigma_mapping, fields_from_rule, get_all_keys

base_path = "src/tests/dummy_files"
case = unittest.TestCase()


def test_chainsaw_mapping_good_input():
    with open(f"{base_path}/chainsaw_good.yml", "r") as file:
        good_mapping = yaml.safe_load(file)

    desired_out_to = ["winlog.event_data.AccessList", "winlog.event_data.AccessMask", "winlog.event_data.Accesses",
                      "winlog.event_data.AccountName", "event.action"]
    desired_out_from = ["AccessList", "AccessMask", "Accesses", "AccountName", "Action"]
    actual_out_to = chainsaw_mapping("to", good_mapping)
    actual_out_from = chainsaw_mapping("from", good_mapping)

    case.assertCountEqual(desired_out_to, actual_out_to)
    case.assertCountEqual(desired_out_from, actual_out_from)


def test_chainsaw_mapping_bad_input():
    with open(f"{base_path}/chainsaw_bad.yml", "r") as file:
        bad_mapping = yaml.safe_load(file)

    with case.assertRaises(TypeError):
        chainsaw_mapping("to", bad_mapping)


def test_sigma_mapping_good_input():
    with open(f"{base_path}/sigma_good.yml", "r") as file:
        good_mapping = yaml.safe_load(file)

    desired_out_to = ["event.code", "user.domain", "winlog.event_data.SubjectDomainName",
                      "query", "host", "server_name"]
    desired_out_from = ["EventID", "SubjectDomainName", "dest_domain"]
    actual_out_to = sigma_mapping("to", good_mapping)
    actual_out_from = sigma_mapping("from", good_mapping)

    case.assertCountEqual(desired_out_to, actual_out_to)
    case.assertCountEqual(desired_out_from, actual_out_from)


def test_sigma_mapping_bad_input():
    with open(f"{base_path}/sigma_bad.yml", "r") as file:
        bad_mapping = yaml.safe_load(file)

    with case.assertRaises(TypeError):
        sigma_mapping("to", bad_mapping)


def test_fields_from_rule_good_input():
    with open(f"{base_path}/rule_good.yml", "r") as file:
        good_rule = yaml.safe_load(file)

    desired_out = ["c-useragent", "c-uri", "resp_mime_types", "c-uri", "Image"]
    actual_out = fields_from_rule(good_rule)

    case.assertCountEqual(desired_out, actual_out)


def test_fields_from_rule_bad_input():
    with open(f"{base_path}/rule_bad.yml", "r") as file:
        bad_rule = yaml.safe_load(file)

    with case.assertRaises(TypeError):
        fields_from_rule(bad_rule)


def test_get_all_keys():
    example_json = {
        "key1_1": 1234,
        "key1_2": 1234,
        "key1_3": {
            "key2_1": 1234,
            "key2_2": 1234,
            "key2_3": {"key3_1": 1234,
                       "key3_2": 1234,
                       "key3_3": 1234},
        }
    }
    desired_out = ['key1_1', 'key1_2', 'key1_3.key2_1', 'key1_3.key2_2', 'key1_3.key2_3.key3_1',
                   'key1_3.key2_3.key3_2', 'key1_3.key2_3.key3_3']
    actual_out = get_all_keys(example_json, "")
    case.assertCountEqual(desired_out, actual_out)
