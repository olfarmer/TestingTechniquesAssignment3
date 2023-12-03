import socket
from enum import Enum


class Command(Enum):
    START = "start"
    STOP = "stop"


def handle_command(command):
    if command[0] == Command.START.value:
        print("Received START command with parameter:", command[1])

    elif command[0] == Command.STOP.value:
        print("Received STOP command with parameter:", command[1])

    else:
        print("Unknown command:", command[0])


def start_server():
    host = 'localhost'
    port = 7890

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()

    print(f"Server listening on {host}:{port}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address}")

        data = client_socket.recv(1024).decode('utf-8')

        if data:
            commands = data.split('\n')

            for command_str in commands:
                command_str = command_str.strip()

                if not command_str:
                    continue

                try:
                    command = tuple(command_str.split('('))
                    handle_command(command)
                except Exception as e:
                    print("Error processing command:", e)
        else:
            print("No data received from client")

        client_socket.close()


if __name__ == "__main__":
    start_server()
