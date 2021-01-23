HEART_GRAPHIC = ['🂱', '🂲', '🂳', '🂴', '🂵', '🂶', '🂷', '🂸', '🂹', '🂺', '🂻', '🂽', '🂾']
LEAF_GRAPHIC = ['🂡', '🂢', '🂣', '🂤', '🂥', '🂦', '🂧', '🂨', '🂩', '🂪', '🂫', '🂭', '🂮']
DIAMOND_GRAPHIC = ['🃁', '🃂', '🃃', '🃄', '🃅', '🃆', '🃇', '🃈', '🃉', '🃊', '🃋', '🃍', '🃎']
CLUBS_GRAPHIC = ['🃑', '🃒', '🃓', '🃔', '🃕', '🃖', '🃗', '🃘', '🃙', '🃚', '🃛', '🃝', '🃞']
JOKER_GRAPHIC = ['🃟', '🃟']

SUIT_HEART = 0
SUIT_LEAF = 1
SUIT_DIAMOND = 2
SUIT_CLUBS = 3
SUIT_JOKER = 4

class Card:
    def __init__(self, value, suit, graphic):
        self.value = value
        self.suit = suit
        self.graphic = graphic

    def __str__(self):
        return self.graphic
    
HEART_CARDS =   [Card(value, SUIT_HEART, graphic) \
                for value, graphic in enumerate(HEART_GRAPHIC, 1)]

LEAF_CARDS =    [Card(value, SUIT_LEAF, graphic) \
                for value, graphic in enumerate(LEAF_GRAPHIC, 1)]

DIAMOND_CARDS = [Card(value, SUIT_DIAMOND, graphic) \
                for value, graphic in enumerate(DIAMOND_GRAPHIC, 1)]

CLUBS_CARDS =   [Card(value, SUIT_CLUBS, graphic) \
                for value, graphic in enumerate(CLUBS_GRAPHIC, 1)]

JOKER_CARDS =   [Card(0, SUIT_JOKER, graphic) \
                for graphic  in JOKER_GRAPHIC]

ALL_CARDS = HEART_CARDS + LEAF_CARDS + DIAMOND_CARDS + CLUBS_CARDS + JOKER_CARDS
