import unittest
import requests
from parameterized import parameterized


class Tests(unittest.TestCase):

    @parameterized.expand([
        [2, True],
        [3, False]
    ])
    def test_valid_data(self, number, result):
        response = requests.get('http://localhost/is_even', params={'number': number})
        self.assertEqual(response.json(), result)

    def test_not_int_number(self, number):
        response = requests.get('http://localhost/is_even', params={'number': number})
        self.assertEqual(415, response.status_code)


if __name__ == '__main__':
    unittest.main()
