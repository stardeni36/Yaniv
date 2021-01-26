from operator import attrgetter
from config import *
from packofcards import PackOfCards
from playercontroller import PlayerController

class Player:
    def __init__(self, name, controller):
        self.hand = PackOfCards()
        self.name = name
        self.controller = controller

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

        state_summary = "This is your hand:\n"
        state_summary += str(self.hand) + '\n'
        state_summary += 'Total value: %d\n' % self.hand.sum()
        state_summary += "The top of the stack is: %s ." % stack_top
        self.publish_msg(state_summary)

        is_yaniv_possible = self.check_yaniv()

        if is_yaniv_possible:
            if self.controller.ask_yaniv():
                return CALL_YANIV
        
        valid_play = False
        while not valid_play:
            indices = self.controller.ask_play(self.hand.cards, stack_top)
            valid_play = self.validate_indices_to_drop(indices)
        return indices
        

    def choice_take_card(self):
        return self.controller.ask_draw()
    
    def is_assaf(self):
        return self.controller.ask_assaf()

    def announce_acquisition(self, acquisition):
        self.publish_msg('New card acquired: %s .' % acquisition)

    def publish_msg(self, msg):
        self.controller.publish_msg(msg)