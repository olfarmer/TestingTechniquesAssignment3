import os
import re
import socket
from enum import Enum

import adapter


savedTokens = {}

class Command(Enum):
    START = "Start"
    STOP = "Stop"
    CREATE_USER = "CreateUser"
    LOGIN_USER = "LoginUser"

def handle_command(command, args, socket):
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
    elif command == Command.CREATE_USER.value:
        print("Received CREATE_USER command")
        try:
            json = adapter.create_user(args[0], args[1])
            socket.send(b"created\n")
            savedTokens[args[0]] = json["access_token"]
            return
        except AssertionError as e:
            print(e)
            socket.send(b'error\n')
            return
    elif command == Command.LOGIN_USER.value:
        print("Received LOGIN_USER command")
        try:
            json = adapter.login_user(args[0], args[1])
            socket.send(b"loggedIn\n")
            savedTokens[args[0]] = json["access_token"]
            return
        except AssertionError as e:
            print(e)
            socket.send(b'error\n')
            return
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

            command, args = extract_command_args(data)

            handle_command(command.strip(), args, client_socket)

    finally:
        client_socket.close()


def extract_command_args(s):
    s = s.replace('"', "")
    match = re.match(r'(\w+)\((.*)\)', s)
    if match:
        command = match.group(1)
        args = match.group(2).split(',') if match.group(2) else []
    else:
        match = re.match(r'(\w+)', s)
        if match:
            command = match.group(1)
            args = []
        else:
            return None, None
    return command, args


if __name__ == "__main__":
    start_server()
