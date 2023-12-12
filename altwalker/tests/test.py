import adapter
import unittest
import os

class ModelName(unittest.TestCase):
    # Vertices
    def stopped(self):
        pass

    def started(self):
        pass

    # Edges
    def starting(self):
        print("Starting the homeserver")
        self.assertTrue(os.system('docker start synapse') == 0, 'Error starting docker container')

    def stopping(self):
        print("Stopping the homeserver")
        self.assertTrue(os.system('docker stop synapse') == 0, 'Error stopping docker container')


