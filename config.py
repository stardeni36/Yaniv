
# Configuration
STARTING_HAND_SIZE = 7

# Enums
DECK = 'deck'
STACK = 'stack'
CALL_YANIV = 0
CALL_ASSAF = 1
SUIT_HEART = 0
SUIT_LEAF = 1
SUIT_DIAMOND = 2
SUIT_CLUBS = 3
SUIT_JOKER = 4
VALUE_JOKER = 0
ALL = 0
CURRENT = 1
OTHERS = 2

class InputError(Exception):
    pass