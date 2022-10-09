import json
import socket
import time
from common.variables import (
    ACTION,
    PRESENCE,
    TIME,
    USER,
    ACCOUNT_NAME,
    RESPONSE,
    ERROR,
)
from common.utils import get_message, send_message, flags


def create_presence(account_name="Guest"):
    out = {ACTION: PRESENCE, TIME: time.time(), USER: {ACCOUNT_NAME: account_name}}
    return out


def process_ans(message):
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return "200 : OK"
        return f"400 : {message[ERROR]}"
    raise ValueError


def main():
    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.connect(flags())
    message_to_server = create_presence()
    send_message(transport, message_to_server)
    try:
        answer = process_ans(get_message(transport))
        print(answer)
    except (ValueError, json.JSONDecodeError):
        print("Failed to decode server message.")


if __name__ == "__main__":
    main()
