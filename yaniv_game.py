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

    
    def distributed_by_indices(self, destination, indices):
        pass


class Player:
    def __init__(self):
        self.pack = PackOfCards()

    def action(self, stack_top):
        print("These are your cards:")
        print(self.pack)
        print("The top of the stack is: %s" % stack_top)

        # Ask first action and validate input
        valid_input = False
        while not valid_input:
            answer = input("Choose your action - (p)lay cards or call (y)aniv: ")
            if answer == 'p' or answer == 'y':
                valid_input = True

        if answer == 'y':
            return CALL_YANIV
        
        # Ask second action and validate input
        valid_input = False
        while not valid_input:
            answer = input("Choose card indices to play, separated by commas: ")
            try:
                indices = [int(val.strip()) for val in answer.split(',')]
                is_valid = lambda x: x in range(len(self.pack.cards))
                if False not in [is_valid(index) for index in indices]:
                    valid_input = True
            except ValueError:
                pass  # Try again
        
        return indices


    def choice_take_card(self):
        while True:
            response = input('Take a card from the deck or the stack? ')
            if response == 'deck':
                return DECK
            if response == 'stack':
                return STACK



class Game:

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
        action = player.action(self.stack.cards[0])

        self.draw(player)
        pass


game = Game()
game.run()

