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
        if cards!=None:
            self.cards = cards
        if is_shuffle:
            shuffle(self.cards)

    def distribute(self, amount=AMOUNT_ALL, destination):
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
        deck = PackOfCards(cards=ALL_CARDS, is_shuffle=True)
        
        player1 = Player()
        player2 = Player()
        self.players = [player1, player2]
        
        for player in players:
            deck.distribute(7, player.pack)

    def run(self):
        gameover = False
        while not gameover:
            pass

    def turn(self, player):
        pass

game = Game()
game.run()

