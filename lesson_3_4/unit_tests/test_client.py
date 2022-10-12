import unittest
from common.variables import RESPONSE, ERROR, USER, ACCOUNT_NAME, TIME, ACTION, PRESENCE
from client import create_presence, process_response


class TestClass(unittest.TestCase):
    def test_presense(self):
        test = create_presence()
        test[TIME] = 1.1  # otherwise the test will fail
        self.assertEqual(
            test, {ACTION: PRESENCE, TIME: 1.1, USER: {ACCOUNT_NAME: "Guest"}}
        )

    def test_200_response(self):
        self.assertEqual(process_response({RESPONSE: 200}), "200 : OK")

    def test_400_response(self):
        self.assertEqual(
            process_response({RESPONSE: 400, ERROR: "Bad Request"}), "400 : Bad Request"
        )

    def test_no_response(self):
        self.assertRaises(ValueError, process_response, {ERROR: "Bad Request"})

    def test_400_no_error(self):
        self.assertRaises(KeyError, process_response, {RESPONSE: 400})


if __name__ == "__main__":
    unittest.main()
