from random import shuffle
from operator import itemgetter, attrgetter
from card import ALL_CARDS


STARTING_HAND_SIZE = 7
AMOUNT_ALL = None
DECK = 'deck'
STACK = 'stack'
CALL_YANIV = 0
CALL_ASSAF = 1


class InputError(Exception):
    pass


class PackOfCards:
    def __init__(self, cards=None, is_shuffle=False):
        self.cards = []
        if cards:  # not None
            self.cards = cards
        if is_shuffle:
            self.shuffle()

    def shuffle(self):
        shuffle(self.cards)

    def __str__(self):
        nice = '---------' + '----'*len(self.cards)
        nice += '\n'
        nice += '| index | '
        nice += ' | '.join(str(index) for index in range(len(self.cards)))
        nice += ' | \n'
        nice += '| card  | '
        nice += ' | '.join([str(card) for card in self.cards])
        nice += ' | \n'
        nice += '---------' + '----'*len(self.cards)
        return nice

    def distribute(self, destination, amount=AMOUNT_ALL):
        if amount == AMOUNT_ALL:
            amount = len(self.cards)
        batch = self.cards[:amount]
        self.cards = self.cards[amount:]
        destination.cards = batch + destination.cards

    def discard_batch(self, indices):
        batch = [self.cards[index] for index in indices]
        for card in batch:
            self.cards.remove(card)
        return batch

    def distribute_by_indices(self, destination, indices):
        batch = self.discard_batch(indices)
        destination.cards = batch + destination.cards

    def sum(self):
        sum_of_values = sum([min(card.value, 10) for card in self.cards])
        return sum_of_values



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

        # if multiple: check both cases - same value or range of numbers with the same suit
        if len(indices) > 1:
            cards_to_check = [self.hand.cards[ind] for ind in indices]

            # check if they have the same value
            values_of_cards_to_check = [card.value for card in cards_to_check]
            # all values are equal
            if len(set(values_of_cards_to_check)) == 1:
                return True
            # 2 values, one is 0 (joker)
            elif len(set(values_of_cards_to_check)) == 2 and (0 in values_of_cards_to_check):
                return True

            # Verify that all values (except jokers) are unique
            values_without_jokers = [val for val in values_of_cards_to_check if val != 0]
            if len(values_without_jokers) != len(set(values_without_jokers)):
                return False

            # check if having the same suit and form a range
            suits_of_cards_to_check = [card.suit for card in cards_to_check]
            if len(set(suits_of_cards_to_check)) == 1 or (len(set(suits_of_cards_to_check)) == 2 and (0 in values_of_cards_to_check)):
                expected_length = max(values_of_cards_to_check) - min(values_of_cards_to_check) + 1
                if expected_length >= 3 and (len(values_of_cards_to_check) == expected_length):
                    return True
                else:
                    return False
            else:
                return False
            #
            # suits_of_cards_to_check = [card.suit for card in cards_to_check]
            # if len(set(suits_of_cards_to_check)) == 1:
            #     if expected_length >= 3 and (len(values_of_cards_to_check) == expected_length):
            #         return True
            #     else:
            #         return False
            # elif len(set(suits_of_cards_to_check)) == 2 and (0 in values_of_cards_to_check):
            #     num_jokers = values_of_cards_to_check.count(0)
            #     if expected_length >= 3 and (len(values_of_cards_to_check) == expected_length):
            #     # check if jokers complete the range
            #     sorted_values = sorted(values_without_jokers)
            #     should_be_equal_to = list(range(sorted_values[0], sorted_values[-1] + 1))
            #     if (len(should_be_equal_to) - len(sorted_values)) == num_jokers:
            #         return True
            #     else:
            #         return False
            # else:
            #     return False
        return True

    def action(self, stack_top):

        # Start by sorting hand (for convenience)
        self.hand.cards.sort(key=attrgetter('value'))

        print("This is your hand:")
        print(self.hand)
        print("The top of the stack is: %s" % stack_top)

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
            answer = input("Call (a)ssaf or (n)o?")
            if answer == 'a' or answer == 'n':
                valid_input = True

        if answer == 'a':
            return True
        return False


class Game:

    def __init__(self):
        self.deck = PackOfCards(cards=ALL_CARDS, is_shuffle=True)
        self.stack = PackOfCards()

        player1 = Player("Stav")
        player2 = Player("Eyal")
        self.players = [player1, player2]
        
        for player in self.players:
            self.deck.distribute(player.hand, STARTING_HAND_SIZE)
        self.deck.distribute(self.stack, 1)

    def run(self):
        gameover = False
        while not gameover:
            for player in self.players:
                if self.turn(player):
                    print('%s called Yaniv!' % player.name)
                    winner = self.finish_game(yaniv=player)
                    print('%s is the winner!' % winner.name)
                    gameover=True
                    break


    def repopulate_deck(self):
        card_inds_to_move = range(1, len(self.stack.cards))  # TODO: make sure the indices are ok
        self.stack.distribute_by_indices(self.deck, card_inds_to_move)
        self.deck.shuffle()

    def draw(self, player):
        response = player.choice_take_card()
        if response == DECK:
            self.deck.distribute(player.hand, 1)
            if len(self.deck.cards) == 0:
                self.repopulate_deck()
        elif response == STACK:
            self.stack.distribute(player.hand, 1)
        else:
            raise InputError('Invalid draw response!')
        return response

    def finish_game(self, yaniv):
        scores = [(player, player.hand.sum()) for player in self.players]
        scores.sort(key=itemgetter[1])
        yaniv_score = None
        for player, score in scores:
            if yaniv_score is not None and score > yaniv_score:
                break
            if player == yaniv:
                yaniv_score = score
            elif player.is_assaf():
                print('%s called Assaf!' % player.name)
                return player
        return yaniv

    def turn(self, player):
        print("%s's turn" % player.name)
        action = player.action(self.stack.cards[0])
        
        if action == CALL_YANIV:
            return True
            
        elif type(action) == list:
            batch = player.hand.discard_batch(action)
            response = self.draw(player)
            self.stack.cards = batch + self.stack.cards

            batch_nice = ' , '.join([str(card) for card in batch])
            print('%s dropped %s ,' % (player.name, batch_nice))
            print('and took a card from the %s.' % response)

        else:
            raise InputError('Invalid action!')
        
        return False


if __name__ == '__main__':
    game = Game()
    game.run()

