import socket
import pickle
from config import *
from localcontroller import LocalController

s = socket.socket()
s.connect((HOST, PORT))
name = input('Please enter your name: ')
s.send(name.encode())

controller = LocalController()

gameover = False
while not gameover:
    msg = s.recv(1).decode()
    if msg == 'y':
        if controller.ask_yaniv():
            s.send('t'.encode())
        else:
            s.send('f'.encode())
    elif msg == 'a':
        if controller.ask_assaf():
            s.send('t'.encode())
        else:
            s.send('f'.encode())
    elif msg == 'c':
        data = s.recv(4096)
        (cards, stack_top) = pickle.loads(data)
        answer = controller.ask_play(cards, stack_top)
        answer = ''.join([str(ind) for ind in answer])
        s.send(answer.encode())
    elif msg == 'd':
        if controller.ask_draw() == STACK:
            s.send('s'.encode())
        else:
            s.send('d'.encode())
    elif msg == 'p':
        print(s.recv(2048).decode())

s.close()