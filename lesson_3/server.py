"""Программа-сервер"""

import socket
import json
from common.variables import (
    ACTION,
    RESPONSE,
    MAX_CONNECTIONS,
    PRESENCE,
    TIME,
    USER,
    ERROR,
)
from common.utils import get_message, send_message, flags


def process_client_message(message):
    if (
        ACTION in message
        and message[ACTION] == PRESENCE
        and TIME in message
        and USER in message
    ):
        return {RESPONSE: 200}
    return {RESPONSE: 400, ERROR: "Bad Request"}


def main():
    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    transport.bind(flags())

    transport.listen(MAX_CONNECTIONS)

    while True:
        client, client_address = transport.accept()
        try:
            message_from_client = get_message(client)
            print(message_from_client)
            response = process_client_message(message_from_client)
            send_message(client, response)
            client.close()
        except (ValueError, json.JSONDecodeError):
            print("Received an invalid message from the client.")
            client.close()


if __name__ == "__main__":
    main()
