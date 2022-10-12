import json
import sys
import unittest
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from unittest.mock import patch

from common.variables import *
from common.utils import get_message, send_message


class TestUtils(unittest.TestCase):
    test_message = {
        "action": "presence",
        "time": 1,
        "type": "status",
        "user": {"account_name": "Guest", "password": ""},
    }
    test_correct_response = {
        "response": 200,
        "time": 1,
        "alert": "Connection was successfully established",
    }
    test_error_response = {"response": 400, "time": 1, "error": "Connection error"}

    def setUp(self):
        # Test socket for the server
        self.server_socket = socket(AF_INET, SOCK_STREAM)
        self.server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.server_socket.bind((DEFAULT_IP_ADDRESS, DEFAULT_PORT))
        self.server_socket.listen(MAX_CONNECTIONS)

        # Test socket for the client
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect((DEFAULT_IP_ADDRESS, DEFAULT_PORT))
        self.client, self.client_address = self.server_socket.accept()

    def tearDown(self):
        self.client.close()
        self.client_socket.close()
        self.server_socket.close()

    @patch.object(sys, "argv", ["server.py", "-p"])
    def test_patch_wrong_system_args_err(self):
        self.assertRaises(IndexError, lambda: sys.argv[2])

    @patch.object(sys, "argv", ["server.py", "-p", 1025])
    def test_patch_correct_system_arguments(self):
        self.assertEqual(1025, sys.argv[2])  # works without lambda

    def test_send_wrong_message_to_server_err(self):
        self.assertRaises(TypeError, send_message, self.client_socket, "not dict")

    def test_send_correct_message_to_server(self):
        send_message(self.client_socket, self.test_message)
        test_response = self.client.recv(MAX_PACKAGE_LENGTH)
        test_response = json.loads(test_response.decode(ENCODING))

        self.assertEqual(self.test_message, test_response)

    def test_send_longer_than_max_length_message_err(self):
        message = json.dumps(self.test_message)
        self.client.send(message.encode(ENCODING))

        self.assertRaises(
            json.decoder.JSONDecodeError, get_message, self.client_socket, 5
        )

    def test_get_message_200(self):
        message = json.dumps(self.test_correct_response)
        self.client.send(message.encode(ENCODING))
        response = get_message(self.client_socket)

        self.assertEqual(self.test_correct_response, response)

    def test_get_message_400(self):
        message = json.dumps(self.test_error_response)
        self.client.send(message.encode(ENCODING))
        response = get_message(self.client_socket)

        self.assertEqual(self.test_error_response, response)

    def test_get_message_not_dict_err(self):
        message = json.dumps("not dict")
        self.client.send(message.encode(ENCODING))

        self.assertRaises(ValueError, get_message, self.client_socket)

    def test_get_message_dict(self):
        message = json.dumps(self.test_correct_response)
        self.client.send(message.encode(ENCODING))

        self.assertIsInstance(get_message(self.client_socket), dict)


if __name__ == "__main__":
    unittest.main()
