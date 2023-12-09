import os
import socket
from enum import Enum


class Command(Enum):
    START = "Start"
    STOP = "Stop"


def handle_command(command, socket):

    if command == Command.START.value:
        print("Received START command")
        if os.system('docker start synapse') == 0:
            socket.send(b'started\n')
        else:
            socket.send(b'error\n')
    elif command == Command.STOP.value:
        print("Received STOP command")
        if os.system('docker stop synapse') == 0:
            socket.send(b'stopped\n')
        else:
            socket.send(b'error\n')
    else:
        print("Unknown command:", command)
        socket.send(b'error\n')


def start_server():
    host = 'localhost'
    port = 7890

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen()

    print(f"Server listening on {host}:{port}")

    client_socket, client_address = server_socket.accept()
    print(f"Accepted connection from {client_address}")
    try:
        while True:
            data = client_socket.recv(1024).decode('utf-8')
            handle_command(data.strip(), client_socket)

    finally:
        client_socket.close()


if __name__ == "__main__":
    start_server()
