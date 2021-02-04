import pickle
from time import sleep
from config import *
from playercontroller import PlayerController

TICK = 0.3

class RemoteController(PlayerController):

    def __init__(self, conn):
        self.conn = conn

    def __del__(self):
        self.conn.close()

    def ask_yaniv(self):
        self.conn.send('y'.encode())
        sleep(TICK)
        if self.conn.recv(256).decode() == 't':
            return True
        sleep(TICK)
        return False

    def ask_assaf(self):
        self.conn.send('a'.encode())
        sleep(TICK)
        if self.conn.recv(256).decode() == 't':
            sleep(TICK)
            return True
        sleep(TICK)
        return False

    def ask_play(self, cards, stack_top):
        self.conn.send('c'.encode())
        sleep(TICK)
        data = pickle.dumps((cards, stack_top))
        self.conn.send(data)
        sleep(TICK)
        answer = list(self.conn.recv(256).decode())
        sleep(TICK)
        return [int(b) for b in answer]

    def ask_draw(self):
        self.conn.send('d'.encode())
        sleep(TICK)
        if self.conn.recv(256).decode() == 's':
            sleep(TICK)
            return STACK
        sleep(TICK)
        return DECK

    def publish_msg(self, msg):
        self.conn.send('p'.encode())
        sleep(TICK)
        self.conn.send(msg.encode())
        sleep(TICK)
