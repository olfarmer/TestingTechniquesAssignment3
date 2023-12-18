import json
import os
import time

import requests

# Define base_url as a global variable
base_url = "http://localhost:8008"


def reset_homeserver():
    os.system('docker start synapse')
    os.system('docker exec -it synapse rm /data/homeserver.db')
    os.system('docker restart synapse')
    # Sleep 2 seconds to let the docker container succesfully start, otherwise we will get an error in the following step
    time.sleep(2)


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


def create_room(access_token, room_name):
    url = f"{base_url}/_matrix/client/v3/createRoom"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    data = {
        "creation_content": {"m.federate": False},
        "name": room_name,
        "preset": "public_chat",
        "room_alias_name": room_name,
        "topic": "Topic of " + room_name
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


def send_message(user1_access_token, room1_id, message):
    url = f"{base_url}/_matrix/client/v3/rooms/{room1_id}/state/m.room.message"
    headers = {
        "Authorization": f"Bearer {user1_access_token}"
    }
    data = {
        "body": message,
        "msgtype": "m.text"
    }
    response = requests.put(url, headers=headers, data=json.dumps(data))

    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"

    return response.json()
