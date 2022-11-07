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
from logs.server_log_config import logger as server_logger


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
    server_logger.debug("Connection request.")

    while True:
        client, client_address = transport.accept()
        try:
            server_logger.debug("Connection was successfully made.")
            message_from_client = get_message(client)
            print(message_from_client)
            response = process_client_message(message_from_client)
            send_message(client, response)
            server_logger.info("The message was sent.")
            client.close()
        except (ValueError, json.JSONDecodeError):
            server_logger.error("Received an invalid message from the client.")
            client.close()


if __name__ == "__main__":
    main()
