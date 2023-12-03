import os

import requests

# Define base_url as a global variable
base_url = "http://localhost:8008"


def reset_database():
    os.system('docker exec -it synapse rm /data/homeserver.db')
    os.system('docker restart synapse')


def create_user(username, password):
    url = f"{base_url}/_matrix/client/r0/register"
    headers = {'Content-Type': 'application/json'}
    data = {
        "username": username,
        "password": password,
        "auth": {"type": "m.login.dummy"}
    }

    response = requests.post(url, headers=headers, json=data)
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"

    return response.json()


def login_user(username, password):
    url = f"{base_url}/_matrix/client/v3/login"
    headers = {'Content-Type': 'application/json'}
    data = {
        "type": "m.login.password",
        "identifier": {"type": "m.id.user", "user": f"@{username}:my.matrix.host"},
        "password": password
    }

    response = requests.post(url, headers=headers, json=data)
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"

    return response.json()


def create_room(access_token, invites):
    url = f"{base_url}/_matrix/client/v3/createRoom"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    data = {
        "creation_content": {"m.federate": False},
        "name": "room1",
        "preset": "public_chat",
        "room_alias_name": "room1",
        "topic": "Topic of room1",
        "invite": invites
    }

    response = requests.post(url, headers=headers, json=data)
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"

    return response.json()


def join_room(access_token, room_id):
    url = f"{base_url}/_matrix/client/v3/join/{room_id}"
    headers = {'Authorization': f'Bearer {access_token}'}

    response = requests.post(url, headers=headers)
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"

    return response.json()
