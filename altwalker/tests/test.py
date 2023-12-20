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

    def loginUser(self, data):
        username = data['username']
        password = data['password']

        response = adapter.login_user(username, password)

        data['username'] = ''
        data['password']= ''
        

    def dontLoginUser(self, data):
        data['username'] = ''
        data['password']= ''

    def creatingRoom(self, data):
        print("Creating a room")
        users = json.loads(data['users'].replace("'", '"'))
        rooms = json.loads(data['rooms'].replace("'", '"'))
        room_name = data['roomname']

        user = random.choice(users)
        without_user = [e for e in users if e != user]

        users_to_invite = list(map(lambda x: x['access_token'] , random.choices(without_user, k=random.randint(0, len(without_user)))))

        response = adapter.create_room(user['access_token'], room_name)

        rooms.append({'room_name': room_name, 'owner': user['username'], 'room_id': response['room_id'], 'invited_users': users_to_invite, 'joined_users': [user['access_token']]})
        data['rooms'] = json.dumps(rooms).replace('"', "'")
        data['invited_users'] = json.dumps(users_to_invite).replace('"', "'")

    def createdRoom(self, data):
        data['roomname'] = ''
        data['invited_users'] = '[]'

    def sendingMessage(self, data):
        print("Sending message")
        users = json.loads(data['users'].replace("'", '"'))
        rooms = json.loads(data['rooms'].replace("'", '"'))

        room = random.choice(rooms)
        access_token = random.choice(room['joined_users'])

        adapter.send_message(access_token, room['room_id'], 'message')

    def addUserToRoom(self, data):
        return
        #This does not work completely yet
        print("Adding user to room")
        invited_users = data['invited_users']
        rooms = json.loads(data['rooms'].replace("'", '"'))
        room_name = data['roomname']

        room = [x for x in rooms if x['room_name'] == room_name][0]

        user = random.choice(invited_users)

        response = adapter.join_room(user, room['room_id'])

        invited_users = invited_users.remove(user)

        data['invited_users'] = json.dumps(invited_users).replace('"', "'")
        room['invited_users'] = invited_users.remove(user)
        room['joined_users'] = room['joined_users'].append(user)

        data['rooms'] = json.dumps(rooms).replace('"', "'")
        