from operator import attrgetter
from config import *
from packofcards import PackOfCards

class Player:
    def __init__(self, name):
        self.hand = PackOfCards()
        self.name = name

    def check_yaniv(self):
        sum = self.hand.sum()
        if sum <= 7:
            return True
        else:
            return False

    def validate_indices_to_drop(self, indices):
        is_in_range = lambda x: x in range(len(self.hand.cards))
        if False in [is_in_range(index) for index in indices]:
            return False

        # Play of multiple cards in a single turn
        if len(indices) > 1:
            cards_to_check = [self.hand.cards[ind] for ind in indices]
            values_of_cards_to_check = [card.value for card in cards_to_check]
            num_jokers = values_of_cards_to_check.count(VALUE_JOKER)

            # Check whether all the cards have the same value
            if len(set(values_of_cards_to_check)) == 1 or \
                (len(set(values_of_cards_to_check)) == 2 and num_jokers > 0):
                return True
            
            # Check whether the cards form a streak (at least 3) of the same suit
            if len(indices) < 3:
                return False
            cards_without_jokers = sorted([card for card in cards_to_check if card.value != VALUE_JOKER], key=attrgetter('value'))
            prev_card = cards_without_jokers[0]
            for card in cards_without_jokers[1:]:
                if card.suit != prev_card.suit:
                    return False
                diff = card.value - prev_card.value
                jokers_needed = diff - 1
                if jokers_needed > num_jokers:
                    return False
                num_jokers -= jokers_needed
                prev_card = card
            
        return True

    def action(self, stack_top):

        # Start by sorting hand (for convenience)
        self.hand.cards.sort(key=attrgetter('value'))

        print("This is your hand:")
        print(self.hand)
        print("The top of the stack is: %s ." % stack_top)

        is_yaniv_possible = self.check_yaniv()

        if is_yaniv_possible:
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
                if self.validate_indices_to_drop(indices):
                    valid_input = True
            except ValueError:
                pass  # Try again
        
        return indices

    def choice_take_card(self):
        while True:
            response = input('Take a card from the (d)eck or the (s)tack? ')
            if response == 'd':
                return DECK
            if response == 's':
                return STACK
    
    def is_assaf(self):
        valid_input = False
        while not valid_input:
            answer = input("Call (a)ssaf or (n)o? ")
            if answer == 'a' or answer == 'n':
                valid_input = True
    
        if answer == 'a':
            return True
        return False

    def announce_acquisition(self, acquisition):
        print('New card acquired: %s .' % acquisition)
