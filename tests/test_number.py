import unittest
import requests
from parameterized import parameterized


class Tests(unittest.TestCase):

    @parameterized.expand([
        ['?number=1', False],
        ['?number=2', True],
        ['?number=-1', False],
        ['?number=-2', True]
    ])
    def test_valid_data(self, query_string, result):
        response = requests.get('http://localhost/is_even' + query_string)
        self.assertEqual(response.json(), result)

    @parameterized.expand([
        ['?number=[]'],
        ["?number=[1]"],
        ["?number=[1,2]"],
        ['?number={}'],
        ["?number={1}"],
        ["?number={1: 2}"],
        ['?number=()'],
        ["?number=(1, 2)"],
        ["?number"],
        ["?number="],
        ["?number=''"],
        ["?number=a"],
        ["?number=.4e7"],
        ["?number=2.0"],
        ['?number="2"'],
        ['?number=True'],
        ['?number=None']
    ])
    def test_not_int_number(self, query_string):
        response = requests.get('http://localhost/is_even' + query_string)
        self.assertEqual(415, response.status_code)
        self.assertEqual('Number must be integer', response.json()['error'])

    def test_missed_number(self):
        response = requests.get('http://localhost/is_even?numb')
        self.assertEqual(400, response.status_code)
        self.assertEqual("You've missed the \"number\" parameter", response.json()['error'])

    def test_invalid_not_int_number(self):
        response = requests.get('http://localhost/is_even?number=1&number=2')
        self.assertEqual(400, response.status_code)
        self.assertEqual('Too much numbers', response.json()['error'])


if __name__ == '__main__':
    unittest.main()
