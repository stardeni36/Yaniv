from config import *

class PlayersPool:
    def __init__(self):
        self.players = []
        self.current = None

    def __iter__(self):
        return iter(self.players)

    def add(self, player):
        self.players.append(player)

    def set_current(self, player):
        self.current = player

    def publish_msg(self, msg, destination):
        for player in self.players:
            if destination == ALL or \
                (destination == CURRENT and player == self.current) or \
                (destination == OTHERS and player != self.current):

                player.publish_msg(msg)

