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


class Player:
    def __init__(self, cards):
        self.player_cards = cards

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


# class Game:
#     # TODO in init:
#     # call PackOfCards and its permutation method
#     # call its method for giving 7 cards to each player
#     # the rest will be the kupa

poc = PackOfCards()
cards_dict = poc.distribute_cards_to_players(2)
player = Player(cards_dict[0])
player.drop_card()


