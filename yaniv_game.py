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
        self.all_cards = HEART + LEAF + DIAMOND + CLUBS + JOKERS
        shuffle(self.all_cards)

    def distribute_cards_to_players(self, player_num):
        cards_dictionary = {}
        for player_index in range(player_num):
            player_cards = self.all_cards[player_index:player_index+7]
            cards_dictionary[player_index] = player_cards
        kupa = self.all_cards[player_num * 7:]
        cards_dictionary['kupa'] = kupa
        return cards_dictionary




# class Game:
#     # TODO in init:
#     # call PackOfCards and its permutation method
#     # call its method for giving 7 cards to each player
#     # the rest will be the kupa

poc = PackOfCards()
print(poc.distribute_cards_to_players(2))


