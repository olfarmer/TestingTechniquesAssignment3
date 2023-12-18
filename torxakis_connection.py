import os
import re
import socket
from enum import Enum

import adapter


savedTokens = {}
roomIds = {}

class Command(Enum):
    START = "Start"
    STOP = "Stop"
    CREATE_USER = "CreateUser"
    LOGIN_USER = "LoginUser"
    CREATE_ROOM = "CreateRoom"
    SEND_MESSAGE = "SendMessage"

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
    elif command == Command.CREATE_ROOM.value:
        print("Received CREATE_ROOM command")
        try:
            # Token, room name
            json = adapter.create_room(savedTokens[args[0]], args[1])
            roomIds[args[1]] = json["room_id"]
            socket.send(b"created\n")
            return
        except AssertionError as e:
            print(e)
            socket.send(b'error\n')
            return
        except Exception as e:
            print("Error executing the command: " + e)
    elif command == Command.SEND_MESSAGE.value:
        print("Received SEND_MESSAGE command")
        try:
            # Token, room name, message
            json = adapter.send_message(savedTokens[args[0]], roomIds[args[1]], args[2])
            socket.send(b"sent\n")
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
            print("data:" + data)
            if data is None or data.strip() == "":
                continue

            command, args = extract_command_args(data)

            handle_command(command.strip(), args, client_socket)
    finally:
        client_socket.close()


def extract_command_args(s):

    match = re.match(r'(\w+)\((.*)\)', s)
    if match:
        command = match.group(1)
        args = match.group(2).split(',') if match.group(2) else []
        args = [s.replace('"', '') for s in args]
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
