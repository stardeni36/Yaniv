from config import *
from player import Player
from localcontroller import LocalController
from botcontroller import BotController
from remotecontroller import RemoteController

# Static factory functions
class PlayerFactory():

    def generate_local_player(player_index):
        valid_input = False
        while not valid_input:
            answer = input("Local player %d, please write your name: " % player_index)
            valid_input = answer.isalnum()
        print('Player %s has joined.' % answer)
        return Player(answer, LocalController())
    
    def generate_bot_player(name):
        print('Bot %s has joined.' % name)
        return Player(name, BotController())
    
    def generate_remote_player():
        # Wait for connection
        conn = ''  # From remote
        name = ''  # From remote
        print('Player %s has joined remotely.' % name)
        return Player(name, RemoteController(conn))
    
