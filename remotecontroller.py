import pickle
from config import *
from playercontroller import PlayerController

class RemoteController(PlayerController):

    def __init__(self, conn):
        self.conn = conn

    def __del__(self):
        self.conn.close()

    def ask_yaniv(self):
        self.conn.send('y'.encode())
        if self.conn.recv(256).decode() == 't':
            return True
        return False

    def ask_assaf(self):
        self.conn.send('a'.encode())
        if self.conn.recv(256).decode() == 't':
            return True
        return False

    def ask_play(self, cards, stack_top):
        self.conn.send('c'.encode())
        data = pickle.dumps((cards, stack_top))
        self.conn.send(data)
        answer = list(self.conn.recv(256).decode())
        return [int(b) for b in answer]

    def ask_draw(self):
        self.conn.send('d'.encode())
        if self.conn.recv(256).decode() == 's':
            return STACK
        return DECK

    def publish_msg(self, msg):
        self.conn.send('p'.encode())
        self.conn.send(msg.encode())
