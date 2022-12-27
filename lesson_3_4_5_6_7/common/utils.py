import json
import sys
from common.variables import (
    MAX_PACKAGE_LENGTH,
    ENCODING,
    DEFAULT_PORT,
    DEFAULT_IP_ADDRESS,
)
import inspect


def log(func):
    def wrapper(*args, **kwargs):
        if "client" in sys.argv[0]:
            from logs.client_log_config import logger as client_logger

            client_logger.info(
                f"{func.__name__} func was called from {inspect.stack()[1][3]} function, args: {args}, kwargs: {kwargs}"
            )

        else:
            from logs.server_log_config import logger as server_logger

            server_logger.info(
                f"{func.__name__} func was called from {inspect.stack()[1][3]} function, args: {args}, kwargs: {kwargs}"
            )

        return func(*args, **kwargs)

    return wrapper


@log
def flags():
    try:
        if "-p" in sys.argv:
            port = int(sys.argv[sys.argv.index("-p") + 1])
        else:
            port = DEFAULT_PORT
        if port < 1024 or port > 65535:
            raise ValueError
    except IndexError:
        print("You have to define the port number after the -p flag.")
        sys.exit(1)
    except ValueError:
        print("Port numbers are only available in the range from 1024 to 65535.")
        sys.exit(1)

    try:
        if "-a" in sys.argv:
            address = sys.argv[sys.argv.index("-a") + 1]
        else:
            address = DEFAULT_IP_ADDRESS

    except IndexError:
        print("You have to define the address after the -a flag.")
        sys.exit(1)
    return address, port


@log
def get_message(client, max_length=MAX_PACKAGE_LENGTH):
    encoded_response = client.recv(max_length)
    if isinstance(encoded_response, bytes):
        json_response = encoded_response.decode(ENCODING)
        response = json.loads(json_response)
        # if isinstance(response, dict):
        return response
    else:
        print("fuck")


@log
def send_message(sock, message):
    # if not isinstance(message, dict):
    #     raise TypeError
    js_message = json.dumps(message)
    encoded_message = js_message.encode(ENCODING)
    sock.send(encoded_message)
