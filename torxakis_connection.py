import socket
from enum import Enum


class Command(Enum):
    START = "Start"
    STOP = "Stop"


def handle_command(command, socket):
    if command == Command.START.value:
        print("Received START command")
        socket.send(b'started')
    elif command == Command.STOP.value:
        print("Received STOP command")
        socket.send(b'stopped')
    else:
        print("Unknown command:", command)
        socket.send(b'error')


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

        while True:
            data = client_socket.recv(1024).decode('utf-8')
            print(data)
            handle_command(data.strip(), client_socket)



        client_socket.close()


if __name__ == "__main__":
    start_server()
