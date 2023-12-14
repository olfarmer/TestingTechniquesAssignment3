import adapter
import unittest
import os
import random_username.generate as ru
import secrets
import json
import random
import time

def setUpRun():
    adapter.reset_homeserver()

class ModelName(unittest.TestCase):
    # Vertices
    def starting(self):
        pass

    def started(self):
        pass

    def createdUser(self):
        pass

    def createdRoom(self):
        pass

    def stopped(self):
        pass

    # Edges
    def e_starting(self):
        print("Starting the homeserver")
        self.assertTrue(os.system('docker start synapse') == 0, 'Error starting docker container')
        # Sleep 2 seconds to let the docker container succesfully start, otherwise we will get an error in the following step
        time.sleep(2)
        

    def stopping(self):
        print("Stopping the homeserver")
        self.assertTrue(os.system('docker stop synapse') == 0, 'Error stopping docker container')

    def creatingUser(self, data):
        print("Creating a user")
        username = ru.generate_username()
        password = secrets.token_urlsafe(10)

        response = adapter.create_user(username[0], password)

        users = json.loads(data['users'])
        users.append({'username': username[0], 'password': password, 'access_token': response['access_token']})
        data['users'] = json.dumps(users).replace('"', "'")

    def creatingRoom(self, data):
        print("Creating a room")
        users = json.loads(data['users'].replace("'", '"'))
        rooms = json.loads(data['rooms'].replace("'", '"'))

        room_name = ru.generate_username()[0]
        user = random.choice(users)

        response = adapter.create_room(user['access_token'], room_name)

        rooms.append({'room_name': room_name, 'owner': user['username'], 'room_id': response['room_id'], 'users': [user['username']]})
        data['rooms'] = json.dumps(rooms).replace('"', "'")

    def sendingMessage(self, data):
        print("Sending message")
        users = json.loads(data['users'].replace("'", '"'))
        rooms = json.loads(data['rooms'].replace("'", '"'))

        room = random.choice(rooms)
        user = random.choice(room['users'])

        access_token = [x for x in users if x['username'] == user][0]['access_token']

        adapter.send_message(access_token, room['room_id'], 'message')

class ImprovedModel(unittest.TestCase):
    # Vertices
    def idle(self):
        pass

    def createUser(self, data):
        print("Creating a user")
        username = data['username']
        password = data['password']

        response = adapter.create_user(username, password)

        users = json.loads(data['users'].replace("'", '"'))
        users.append({'username': username, 'password': password, 'access_token': response['access_token']})
        data['users'] = json.dumps(users).replace('"', "'")

    def createRoom(self):
        pass

    # Edges
    def creatingUser(self, data):
        pass

    def loginUser(self):
        pass

    def dontLoginUser(self):
        pass

    def creatingRoom(self, data):
        print("Creating a room")
        users = json.loads(data['users'].replace("'", '"'))
        rooms = json.loads(data['rooms'].replace("'", '"'))

        room_name = ru.generate_username()[0]
        user = random.choice(users)

        response = adapter.create_room(user['access_token'], room_name)

        rooms.append({'room_name': room_name, 'owner': user['username'], 'room_id': response['room_id'], 'users': [user['username']]})
        data['rooms'] = json.dumps(rooms).replace('"', "'")

    def createdRoom(self):
        pass

    def sendingMessage(self, data):
        print("Sending message")
        users = json.loads(data['users'].replace("'", '"'))
        rooms = json.loads(data['rooms'].replace("'", '"'))

        room = random.choice(rooms)
        user = random.choice(room['users'])

        access_token = [x for x in users if x['username'] == user][0]['access_token']

        adapter.send_message(access_token, room['room_id'], 'message')