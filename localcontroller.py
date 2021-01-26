from config import *
from playercontroller import PlayerController

class LocalController(PlayerController):

    def ask_yaniv(self):

        valid_input = False
        while not valid_input:
            answer = input("Choose your action - (p)lay cards or call (y)aniv: ")
            if answer == 'p' or answer == 'y':
                valid_input = True

        if answer == 'y':
            return True

    def ask_play(self, cards, stack_top):

        valid_input = False
        while not valid_input:
            answer = input("Choose card indices to play, separated by commas: ")
            try:
                indices = [int(val.strip()) for val in answer.split(',')]
                valid_input = True
            except ValueError:
                pass  # Try again
        
        return indices

    def ask_draw(self):
        
        valid_input = False
        while not valid_input:
            answer = input('Take a card from the (d)eck or the (s)tack? ')
            if answer == 'd':
                return DECK
            if answer == 's':
                return STACK

    def ask_assaf(self):
        
        valid_input = False
        while not valid_input:
            answer = input("Call (a)ssaf or (n)o? ")
            if answer == 'a' or answer == 'n':
                valid_input = True
    
        if answer == 'a':
            return True
        return False

    def publish_msg(self, msg):
        print(msg)