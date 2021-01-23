from random import shuffle

HEART = ['🂱', '🂲', '🂳', '🂴', '🂵', '🂶', '🂷', '🂸', '🂹', '🂺', '🂻', '🂽', '🂾']
LEAF = ['🂡', '🂢', '🂣', '🂤', '🂥', '🂦', '🂧', '🂨', '🂩', '🂪', '🂫', '🂭', '🂮']
DIAMOND = ['🃁', '🃂', '🃃', '🃄', '🃅', '🃆', '🃇', '🃈', '🃉', '🃊', '🃋', '🃍', '🃎']
CLUBS = ['🃑', '🃒', '🃓', '🃔', '🃕', '🃖', '🃗', '🃘', '🃙', '🃚', '🃛', '🃝', '🃞']
JOKERS = ['🃟', '🃟']
ALL_CARDS = HEART + LEAF + DIAMOND + CLUBS + JOKERS

AMOUNT_ALL = None


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

    def drop_card(self):
        print("these are your cards:")
        print(self.player_cards)
        # choose card index to drop it - TODO: allow multiple cards
        index = int(input("please choose card index to drop: "))
        dropped_card = self.player_cards.pop(index)
        print("dropped cards: ", dropped_card)
        print("these are your cards:")
        print(self.player_cards)

    def take_card(self):
        # TODO take_last dropped
        # TODO take from kupa
        pass


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
        response = input('take a card from the deck or the stack?')
        if response == 'deck':
            pass
        elif response == 'stack':
            self.stack.distribute(player.pack, 1)

    def turn(self, player):
        # TODO: drop cards
        self.draw(player)
        pass


game = Game()
game.run()

