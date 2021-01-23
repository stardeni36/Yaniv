from random import shuffle
from operator import itemgetter, attrgetter
from card import ALL_CARDS, VALUE_JOKER


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
        return batch

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
                    print('The winner is %s!' % winner.name)
                    gameover=True
                    break

    def repopulate_deck(self):
        card_inds_to_move = range(1, len(self.stack.cards))  # TODO: make sure the indices are ok
        self.stack.distribute_by_indices(self.deck, card_inds_to_move)
        self.deck.shuffle()

    def draw(self, player):
        response = player.choice_take_card()
        if response == DECK:
            acquisition = self.deck.distribute(player.hand, 1)
            if len(self.deck.cards) == 0:
                self.repopulate_deck()
        elif response == STACK:
            acquisition = self.stack.distribute(player.hand, 1)
        else:
            raise InputError('Invalid draw response!')
        player.announce_acquisition(acquisition[0])
        return response, acquisition[0]

    def finish_game(self, yaniv):
        scores = [(player, player.hand.sum()) for player in self.players]
        scores.sort(key=itemgetter(1))
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
        print("%s's turn." % player.name)
        action = player.action(self.stack.cards[0])
        
        if action == CALL_YANIV:
            return True
            
        elif type(action) == list:
            batch = player.hand.discard_batch(action)
            batch.sort(key=attrgetter('value'), reverse=True)
            response, acquisition = self.draw(player)
            self.stack.cards = batch + self.stack.cards

            batch_nice = ' , '.join([str(card) for card in batch])
            print('%s dropped %s ,' % (player.name, batch_nice))
            if response == DECK:
                print('and took a card from the deck.')
            if response == STACK:
                print('and took the card %s  from the stack.' % str(acquisition))

        else:
            raise InputError('Invalid action!')
        
        return False


if __name__ == '__main__':
    game = Game()
    game.run()

