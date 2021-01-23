from random import shuffle
from card import ALL_CARDS

AMOUNT_ALL = None
DECK = 0
STACK = 1
CALL_YANIV = 0
CALL_ASSAF = 1

class PackOfCards:
    def __init__(self, cards=None, is_shuffle=False):
        self.cards = []
        if cards:  # not None
            self.cards = cards
        if is_shuffle:
            shuffle(self.cards)

    def distribute(self, destination, amount=AMOUNT_ALL):
        if amount == AMOUNT_ALL:
            amount = len(self.cards)
        batch = self.cards[:amount]
        self.cards = self.cards[amount:]
        destination.cards += batch


class Player:
    def __init__(self):
        self.pack = PackOfCards()

    def action(self):
        print("These are your cards:")
        print(self.pack)

        valid_input = False
            while not valid_input:
            answer = int(input("Choose your action - (p)lay cards or call (y)aniv: "))
            if answer == 'p' or answer == 'y':
                valid_input = True

        if answer == 'y'
            return CALL_YANIV
        
        valid_input = False
        while not valid_input:
            answer = int(input("Choose card indices to play, separated by commas: "))
            splitted = answer.split(',')
            try
            if False not in [val.isnumeric() for val in splitted]:
                valid_input = True
        
        indices = [int(splitted)]
        dropped_card = self.player_cards.pop(index)
        print("dropped cards: ", dropped_card)
        print("these are your cards:")
        print(self.player_cards)

    def choice_take_card(self):
        while True:
            response = input('take a card from the deck or the stack? ')
            if response == 'deck':
                return DECK
            if response == 'stack':
                return STACK



class Game:
    # TODO in init:
    # call PackOfCards and its permutation method
    # call its method for giving 7 cards to each player
    # the rest will be the kupa

    def __init__(self):
        self.deck = PackOfCards(cards=ALL_CARDS, is_shuffle=True)
        self.stack = PackOfCards()

        player1 = Player()
        player2 = Player()
        self.players = [player1, player2]
        
        for player in self.players:
            self.deck.distribute(player.pack, 7)
        self.deck.distribute(self.stack, 1)

    def run(self):
        gameover = False
        while not gameover:
            for player in self.players:
                self.turn(player)
            pass

    def draw(self, player):
        response = player.choice_take_card()
        if response == DECK:
            self.deck.distribute(player.pack, 1)
        elif response == STACK:
            self.stack.distribute(player.pack, 1)

    def turn(self, player):
        player.action(self.stack[0])
        self.draw(player)
        pass


game = Game()
game.run()

