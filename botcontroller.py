from time import sleep
import random
from config import *
from playercontroller import PlayerController

class BotController(PlayerController):

    def ask_yaniv(self):
        return True

    def ask_assaf(self):
        return True

    def ask_play(self, cards, stack_top):
        sleep(2)
        maximal_index = max(range(len(cards)), key=lambda i: cards[i].value)
        return [maximal_index]

    def ask_draw(self):
        sleep(1)
        random_number = random.random()
        if random_number > 0.5:
            return DECK
        else:
            return STACK

    def publish_msg(self, msg):
        pass#print('Beep beep')