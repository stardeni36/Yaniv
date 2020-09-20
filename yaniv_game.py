from random import shuffle

HEART = ['🂱', '🂲', '🂳', '🂴', '🂵', '🂶', '🂷', '🂸', '🂹', '🂺', '🂻', '🂽', '🂾']
LEAF = ['🂡', '🂢', '🂣', '🂤', '🂥', '🂦', '🂧', '🂨', '🂩', '🂪', '🂫', '🂭', '🂮']
DIAMOND = ['🃁', '🃂', '🃃', '🃄', '🃅', '🃆', '🃇', '🃈', '🃉', '🃊', '🃋', '🃍', '🃎']
CLUBS = ['🃑', '🃒', '🃓', '🃔', '🃕', '🃖', '🃗', '🃘', '🃙', '🃚', '🃛', '🃝', '🃞']
JOKERS = ['🃟', '🃟']


class PackOfCards:
    def __init__(self):
        # define all cards in the pack
        # 52 cards + 2 jokers -> 54
        self.all_cards = self.shuffle_cards(HEART + LEAF + DIAMOND + CLUBS + JOKERS)
        print(self.all_cards)

    def shuffle_cards(self, cards):
        # permute method for every game
        shuffle(cards)
        return cards

    def distribute_cards_to_players(self):
        pass



# class Game:
#     # TODO in init:
#     # call PackOfCards and its permutation method
#     # call its method for giving 7 cards to each player
#     # the rest will be the kupa

poc = PackOfCards()


