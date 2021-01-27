from operator import itemgetter, attrgetter
from time import sleep
import random
from config import *
from card import ALL_CARDS
from packofcards import PackOfCards
from player import Player
from playerspool import PlayersPool
from playerfactory import PlayerFactory


class Game:

    def __init__(self):
        self.deck = PackOfCards(cards=ALL_CARDS, is_shuffle=True)
        self.stack = PackOfCards()
        self.pool = PlayersPool()
        for i in range(NUM_LOCAL_PLAYERS):
            self.pool.add(PlayerFactory.generate_local_player(i+1))
        for name in random.sample(BOT_NAMES, NUM_BOT_PLAYERS):
            self.pool.add(PlayerFactory.generate_bot_player(name))
        for i in range(NUM_REMOTE_PLAYERS):
            self.pool.add(PlayerFactory.generate_remote_player())
        for player in self.pool:
            self.deck.distribute(player.hand, STARTING_HAND_SIZE)
        self.deck.distribute(self.stack, 1)

    def run(self):
        gameover = False
        while not gameover:
            for player in self.pool:
                self.pool.set_current(player)
                sleep(1)
                if self.turn(player):
                    self.pool.publish_msg('%s called Yaniv!' % player.name, ALL)
                    winner, scores = self.finish_game(yaniv=player)
                    self.pool.publish_msg('The winner is %s!' % winner.name, ALL)
                    for player, score in scores:
                        self.pool.publish_msg('{:<20} {:<3}'.format(player.name, score), ALL)
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
        scores = [(player, player.hand.sum()) for player in self.pool]
        scores.sort(key=itemgetter(1))
        yaniv_score = None
        for player, score in scores:
            if yaniv_score is not None and score > yaniv_score:
                break
            if player == yaniv:
                yaniv_score = score
            elif player.is_assaf():
                self.pool.publish_msg('%s called Assaf!' % player.name, ALL)
                return player, scores
        return yaniv, scores

    def turn(self, player):
        self.pool.publish_msg("\n%s's turn." % player.name, ALL)
        action = player.action(self.stack.cards[0])
        
        if action == CALL_YANIV:
            return True
            
        elif type(action) == list:
            batch = player.hand.discard_batch(action)
            batch.sort(key=attrgetter('value'), reverse=True)
            response, acquisition = self.draw(player)
            self.stack.cards = batch + self.stack.cards

            batch_nice = ' , '.join([str(card) for card in batch])
            turn_summary = '%s dropped %s ,\n' % (player.name, batch_nice)
            if response == DECK:
                turn_summary += 'and took a card from the deck.'
            if response == STACK:
                turn_summary += 'and took the card %s  from the stack.' % str(acquisition)
            self.pool.publish_msg(turn_summary, OTHERS)

        else:
            raise InputError('Invalid action!')
        
        return False


if __name__ == '__main__':
    game = Game()
    game.run()

