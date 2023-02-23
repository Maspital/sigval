import unittest

from parser import get_all_keys


def test_get_all_keys():
    case = unittest.TestCase()
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
    desired_output = ['key1_1', 'key1_2', 'key1_3.key2_1', 'key1_3.key2_2', 'key1_3.key2_3.key3_1',
                      'key1_3.key2_3.key3_2', 'key1_3.key2_3.key3_3']
    actual_output = get_all_keys(example_json, "")
    case.assertCountEqual(desired_output, actual_output)
