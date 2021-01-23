from config import *
from random import shuffle

class PackOfCards:
    def __init__(self, cards=None, is_shuffle=False):
        self.cards = []
        if cards:  # not None
            self.cards = cards
        if is_shuffle:
            self.shuffle()

    def shuffle(self):
        shuffle(self.cards)

    def __str__(self):
        nice = '---------' + '----'*len(self.cards)
        nice += '\n'
        nice += '| index | '
        nice += ' | '.join(str(index) for index in range(len(self.cards)))
        nice += ' | \n'
        nice += '| card  | '
        nice += ' | '.join([str(card) for card in self.cards])
        nice += ' | \n'
        nice += '---------' + '----'*len(self.cards)
        return nice

    def distribute(self, destination, amount):
        batch = self.cards[:amount]
        self.cards = self.cards[amount:]
        destination.cards = batch + destination.cards
        return batch

    def discard_batch(self, indices):
        batch = [self.cards[index] for index in indices]
        for card in batch:
            self.cards.remove(card)
        return batch

    def distribute_by_indices(self, destination, indices):
        batch = self.discard_batch(indices)
        destination.cards = batch + destination.cards

    def sum(self):
        sum_of_values = sum([min(card.value, 10) for card in self.cards])
        return sum_of_values
