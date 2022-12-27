from socket import AF_INET, SOCK_STREAM, socket, SO_REUSEADDR, SOL_SOCKET
from select import select
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
from common.utils import log


def read_requests(read_clients, clients):
    responses = {}

    for client in read_clients:
        try:
            data = get_message(client)
            responses[client] = data
        except Exception as e:
            print(e)
            print(f"Client {client.fileno()} {client.getpeername()} has disconnected")
            server_logger.error(
                f"Client {client.fileno()} {client.getpeername()} has disconnected"
            )
            client.close()
            clients.remove(client)
    return responses


def write_responses(requests, clients_write, clients):
    sender_msg = requests.popitem()[1]
    for client in clients_write:
        try:
            resp = sender_msg
            send_message(client, resp)
        except Exception as e:
            print(e)
            # client.fileno() - client socket file descriptor (small integer)
            # client.getpeername() - ip-address and port of client's socket
            print(f"Client {client.fileno()} {client.getpeername()} has disconnected")
            clients.remove(client)
            client.close()


@log
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
    clients = []
    with socket(AF_INET, SOCK_STREAM) as sock:
        sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        sock.bind(flags())
        sock.listen(MAX_CONNECTIONS)
        sock.settimeout(1)

        while True:
            try:
                client, client_address = sock.accept()
            except OSError:
                pass
            else:
                server_logger.debug(f"Connection request from {client_address}.")
                clients.append(client)
                server_logger.debug("Connection was successfully made.")
            finally:
                print("...")
                read_from = []
                write_to = []
                try:
                    read_from, write_to, _ = select(clients, clients, [], 0)
                except Exception as e:
                    print(e)
                    pass
                requests = read_requests(read_from, clients)
                if requests:
                    write_responses(requests, write_to, clients)
                    server_logger.info("The messages are sent.")


if __name__ == "__main__":
    main()
