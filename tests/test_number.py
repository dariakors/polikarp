import unittest
import requests
from parameterized import parameterized


class Tests(unittest.TestCase):

    @parameterized.expand([
        [2, True],
        [3, False],
        ['2', True],
        ['3', False]
    ])
    def test_valid_data(self, number, result):
        response = requests.get('http://localhost/is_even', params={'number': number})
        self.assertEqual(response.json(), result)

    @parameterized.expand([
        ["[1]"],
        ["[1,2]"],
        ["{1}"],
        ["{1: 2}"],
        ["a"],
        [".4e7"],
        ["2.0"],
        ["[]"],
        ["{}"],
        [""],
    ])
    def test_valid_not_int_number(self, number):
        response = requests.get('http://localhost/is_even', params={'number': number})
        self.assertEqual(415, response.status_code)

    @parameterized.expand([
        [{}],
        [[]]
    ])
    def test_missed_number(self, number):
        response = requests.get('http://localhost/is_even', params={'number': number})
        self.assertEqual(400, response.status_code)
        self.assertEqual("You've missed the \"number\" parameter", response.json()['error'])

    @parameterized.expand([
        [[1, 2]],
        [{1: 2, 2: 3}]
    ])
    def test_invalid_not_int_number(self, number):
        response = requests.get('http://localhost/is_even', params={'number': number})
        self.assertEqual(400, response.status_code)
        self.assertEqual('Too much numbers', response.json()['error'])


if __name__ == '__main__':
    unittest.main()
