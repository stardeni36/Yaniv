from random import shuffle
from operator import attrgetter
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
            self.shuffle_pack()

    def shuffle_pack(self):
        shuffle(self.cards)

    def __str__(self):
        return str([str(card) for card in self.cards])

    def distribute(self, destination, amount=AMOUNT_ALL):
        if amount == AMOUNT_ALL:
            amount = len(self.cards)
        batch = self.cards[:amount]
        self.cards = self.cards[amount:]
        destination.cards = batch + destination.cards

    def distribute_by_indices(self, destination, indices):
        batch = [self.cards[index] for index in indices]
        for card in batch:
            self.cards.remove(card)
        destination.cards = batch + destination.cards


class Player:
    def __init__(self):
        self.hand = PackOfCards()

    def action(self, stack_top):

        # Start by sorting hand (for convenience)
        self.hand.cards.sort(key=attrgetter('value'))

        print("These are your cards:")
        print(self.hand)
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
                is_valid = lambda x: x in range(len(self.hand.cards))
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
            self.deck.distribute(player.hand, 7)
        self.deck.distribute(self.stack, 1)

    def run(self):
        gameover = False
        while not gameover:
            for player in self.players:
                self.turn(player)
            pass

    def repopulate_deck(self):
        card_inds_to_move = range(1, len(self.stack.cards))  # TODO: make sure the indices are ok
        self.stack.distributed_by_indices(self.deck, card_inds_to_move)
        self.deck.shuffle_pack()

    def draw(self, player):
        response = player.choice_take_card()
        if response == DECK:
            self.deck.distribute(player.hand, 1)
            if len(self.deck.cards) == 0:
                self.repopulate_deck()

        elif response == STACK:
            self.stack.distribute(player.hand, 1)

    def finish_game(self):
        # check other players packs
        for player in self.players: # exclude current one
            sum([card.value for card in player.pack.cards])

    def check_yaniv(self, player):
        if sum([card.value for card in player.pack.cards]) <= 7:
            return True
        else:
            return False

    def turn(self, player):
        action = player.action(self.stack.cards[0])
        if action == CALL_YANIV:
            if self.check_yaniv(player):
                self.finish_game()

        self.draw(player)


        pass


game = Game()
game.run()

