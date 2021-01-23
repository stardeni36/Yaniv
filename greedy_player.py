from time import sleep
import random
from operator import attrgetter
from config import *
from packofcards import PackOfCards


class GreedyPlayer:
    def __init__(self, name):
        self.hand = PackOfCards()
        self.name = name

    def check_yaniv(self):
        sum = self.hand.sum()
        if sum <= 7:
            return True
        else:
            return False

    def action(self, stack_top):

        # Start by sorting hand (for convenience)
        self.hand.cards.sort(key=attrgetter('value'))

        is_yaniv_possible = self.check_yaniv()

        if is_yaniv_possible:
            return CALL_YANIV

        # Ask second action and validate input
        maximal_index = max(range(len(self.hand.cards)), key=lambda i: self.hand.cards[i].value)
        indices = [maximal_index]
        sleep(2)
        return indices

    def choice_take_card(self):
        sleep(1)
        random_number = random.random()
        if random_number > 0.5:
            return DECK
        else:
            return STACK

    def is_assaf(self):
        return True

    def announce_acquisition(self, acquisition):
        pass
