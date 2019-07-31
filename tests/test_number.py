import unittest
import requests
from parameterized import parameterized


class Tests(unittest.TestCase):

    @parameterized.expand([
        ['0', True],
        ['2', True],
        ['-2', True],
        ['    2    ', True]
    ])
    def test_even_numbers(self, query_params, result):
        response = requests.get('http://localhost/is_even?number=' + query_params)
        self.assertEqual(response.json(), result)

    @parameterized.expand([
        ['1', False],
        ['-1', False],
        ['     -1    ', False]
    ])
    def test_odd_numbers(self, query_params, result):
        response = requests.get('http://localhost/is_even?number=' + query_params)
        self.assertEqual(response.json(), result)

    def test_too_long_uri(self):
        # 8193 - nginx limit for uri by default
        max_length_for_query_string = 8193 - len('http://localhost/is_even?number=') + 1
        response = requests.get('http://localhost/is_even' + '?number=' + '9'*max_length_for_query_string)
        self.assertEqual(414, response.status_code)
        self.assertEqual("Request-URI Too Large", response.reason)

    @parameterized.expand([
        ["=[]"],
        ["=[1]"],
        ["=[1,2]"],
        ["={}"],
        ["={1}"],
        ["={1: 2}"],
        ["=()"],
        ["=(1)"],
        ["=(1, 2)"],
        [""],
        ["="],
        ["=''"],
        ["=a"],
        ["=.4e7"],
        ["=2.0"],
        ["='2'"],
        ["=True"],
        ["=None"]
    ])
    def test_not_int_number(self, query_string):
        response = requests.get('http://localhost/is_even?number' + query_string)
        self.assertEqual(415, response.status_code)
        self.assertEqual('Number must be integer', response.json()['error'])

    def test_missed_number(self):
        response = requests.get('http://localhost/is_even?numb')
        self.assertEqual(400, response.status_code)
        self.assertEqual("You've missed the 'number' parameter", response.json()['error'])

    def test_invalid_not_int_number(self):
        response = requests.get('http://localhost/is_even?number=1&number=2')
        self.assertEqual(400, response.status_code)
        self.assertEqual('Too much numbers', response.json()['error'])

    def test_not_allowed_method(self):
        response = requests.post('http://localhost/is_even?number=2')
        self.assertEqual(405, response.status_code)
        self.assertEqual('METHOD NOT ALLOWED', response.reason)


if __name__ == '__main__':
    unittest.main()
