from socket import AF_INET, SOCK_STREAM, socket
import sys
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
from logs.client_log_config import logger as client_logger
from common.utils import log


@log
def create_presence(account_name="Guest"):
    out = {ACTION: PRESENCE, TIME: time.time(), USER: {ACCOUNT_NAME: account_name}}
    return out


@log
def process_response(message):
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return "200 : OK"
        return f"400 : {message[ERROR]}"
    raise ValueError


def sender():
    with socket(AF_INET, SOCK_STREAM) as sock:
        sock.connect(flags())
        print("I am a sender")
        while True:
            message_to_server = input(
                "Write a message to the listeners or q to quit the loop: "
            )
            if message_to_server == "q":
                break
            send_message(sock, message_to_server)


def listener():
    with socket(AF_INET, SOCK_STREAM) as sock:
        sock.connect(flags())
        print("I am a listener")
        while True:
            response = get_message(sock)
            print(response)


try:
    if "-o" in sys.argv:
        option = sys.argv[sys.argv.index("-o") + 1]
    else:
        option = "listen"
except IndexError:
    print("You have to define the option (listen or send) after the -o flag.")
    sys.exit(1)

if option == "send":
    sender()
elif option == "listen":
    listener()
else:
    print("option flag got a wrong value, it must be either listen or send")
# if __name__ == "__main__":
#     main()
