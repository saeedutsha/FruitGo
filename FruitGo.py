#Two player FruitGo, with minimax computer player.
#Utsha, 2018

from random import shuffle
from copy import deepcopy
from itertools import combinations

class Deck(object):
    def __init__(self):
        card_names = ['Mango', 'Guava', 'Strawberry', 'DoubleCherry', 'TripleCherry', 'SingleCherry', 'YellowApple', 'RedApple', 'GreenApple', 'Ripe', 'Banana']
        counts = [14, 14, 14, 12, 8, 6, 10, 5, 5, 6, 4]

        self.cards = []
        for i in range(len(counts)):
            for j in range(counts[i]):
                self.cards.append(card_names[i])

        shuffle(self.cards)

    def deal(self, n):
        return self.cards[0:n], self.cards[n:2*n]

class GameState(object):
    def __init__(self):
        D = Deck()
        self.p1_hand, self.p2_hand = D.deal(6)
        self.p1_table, self.p2_table = [], []

    def swap(self):
        self.p1_hand, self.p2_hand = self.p2_hand, self.p1_hand

    def finished(self):
        return self.p1_hand == [] and self.p2_hand == []

    def get_hands(self):
        return self.p1_hand, self.p2_hand

    def add_to_p1_table(self, card):
        if self.p1_table.count('Ripe') > 0 and 'Apple' in card:
            self.p1_table.remove('Ripe')
            self.p1_table.append(card + 'Ripe')
        else:
            self.p1_table.append(card)

    def add_to_p2_table(self, card):
        if self.p2_table.count('Ripe') > 0 and 'Apple' in card:
            self.p2_table.remove('Ripe')
            self.p2_table.append(card + 'Ripe')
        else:
            self.p2_table.append(card)

    def get_tables(self):
        return self.p1_table, self.p2_table

    def play(self, p1_move, p2_move):
        p1_valid, p2_valid = False, False
        p1_chop, p2_chop = False, False

        if p1_move[0] == 0 and self.p1_hand.count(p1_move[1]) > 0:
            p1_valid = True
        elif p1_move[0] == 1 and self.p1_table.count('Banana') > 0 and self.p1_hand.count(p1_move[1][0]) > 0 and self.p1_hand.count(p1_move[1][1]) > 0:
            p1_valid, p1_chop = True, True

        if p2_move[0] == 0 and self.p2_hand.count(p2_move[1]) > 0:
            p2_valid = True
        elif p2_move[0] == 1 and self.p2_table.count('Banana') > 0 and self.p2_hand.count(p2_move[1][0]) > 0 and self.p2_hand.count(p2_move[1][1]) > 0:
            p2_valid, p2_chop = True, True

        if p1_valid and p2_valid:
            if p1_chop:
                self.p1_hand.remove(p1_move[1][0])
                self.add_to_p1_table(p1_move[1][0])

                self.p1_hand.remove(p1_move[1][1])
                self.add_to_p1_table(p1_move[1][1])

                self.p1_table.remove('Banana')
                self.p1_hand.append('Banana')

            else:
                self.p1_hand.remove(p1_move[1])
                self.add_to_p1_table(p1_move[1])

            if p2_chop:
                self.p2_hand.remove(p2_move[1][0])
                self.add_to_p2_table(p2_move[1][0])

                self.p2_hand.remove(p2_move[1][1])
                self.add_to_p2_table(p2_move[1][1])

                self.p2_table.remove('Banana')
                self.p2_hand.append('Banana')

            else:
                self.p2_hand.remove(p2_move[1])
                self.add_to_p2_table(p2_move[1])

            self.swap()

        else:
            print 'Invalid play'

    def score(self):
        p1_total, p1_maki = eval_table(self.p1_table)
        p2_total, p2_maki = eval_table(self.p2_table)
        maki_diff = 0

        if p1_maki > p2_maki:
            maki_diff = 6
            if p2_maki > 0:
                maki_diff = 3
        if p2_maki > p1_maki:
            maki_diff = -6
            if p1_maki > 0:
                maki_diff = -3

        return p1_total - p2_total + maki_diff

def eval_table(table):
    total, maki = 0, 0

    total += 5 * (table.count('Mango') / 2)
    total += 10 * (table.count('Guava') / 3)
    total += (table.count('Strawberry') * (table.count('Strawberry') + 1)) / 2
    maki += table.count('SingleCherry') + 2 * table.count('DoubleCherry') + 3 * table.count('TripleCherry')
    total += table.count('GreenApple')
    total += 2 * table.count('YellowApple')
    total += 3 * table.count('RedApple')
    total += 3 * table.count('GreenAppleRipe')
    total += 6 * table.count('YellowAppleRipe')
    total += 9 * table.count('RedAppleRipe')

    return total, maki

def main():
    G = GameState()
    game_mode = 0

    print "\nFruitGo!\n"
    while not(game_mode in ['1','2']):
        game_mode = raw_input("1. Human vs Human, 2. Human vs Robot: ")

    while not(G.finished()):
        p1_hand, p2_hand = G.get_hands()
        p1_table, p2_table = G.get_tables()

        print '\n'
        print "p1's hand: " + str(p1_hand) + '\n'
        print "p1's table: " + str(p1_table) + '\n'
        print "p2's hand: " + str(p2_hand) + '\n'
        print "p2's table: " + str(p2_table) + '\n'

        #Human vs Human
        if game_mode == '1':
            p1_input = raw_input("p1's play: ")

            if p1_input[:9] == 'Swap for ':
                p1_select = [1, [p1_input[(p1_input.index('for ') + 4):p1_input.index(' and')], p1_input[p1_input.index('and ') + 4:]]]
            else:
                p1_select = [0, p1_input]

            p2_input = raw_input("p2's play: ")

            if p2_input[:9] == 'Swap for ':
                p2_select = [1, [p2_input[(p2_input.index('for ') + 4):p2_input.index(' and')], p2_input[p2_input.index('and ') + 4:]]]
            else:
                p2_select = [0, p2_input]

        #Human vs Robot
        elif game_mode == '2':
            p1_input = raw_input("p1's play: ")

            if p1_input[:9] == 'Swap for ':
                p1_select = [1, [p1_input[(p1_input.index('for ') + 4):p1_input.index(' and')], p1_input[p1_input.index('and ') + 4:]]]
            else:
                p1_select = [0, p1_input]

            p2_select = find_p2_best_move(deepcopy(G), -1000, 1000)[0]

            if p2_select[0] == 0:
                p2_play = p2_select[1]
            elif p2_select[0] == 1:
                p2_play = 'Swap for ' + p2_select[1][0] + ' and ' +  p2_select[1][1]

            print "p2's play: " + p2_play

        G.play(p1_select,p2_select)

    p1_table, p2_table = G.get_tables()
    score_diff = G.score()

    print '\n'
    print "p1's table: " + str(p1_table) + '\n'
    print "p2's table: " + str(p2_table) + '\n'

    if score_diff > 0:
        print "p1 wins by " + str(score_diff)
    elif score_diff < 0:
        print "p2 wins by " + str(-score_diff)
    else:
        print "p1 and p2 rejoice in their shared victory!"

def find_p2_best_move(G, alpha, beta):
    p1_hand, p2_hand = G.get_hands()
    p1_table, p2_table = G.get_tables()
    
    if len(p2_hand) == 1:
        H = deepcopy(G)
        H.play([0,p1_hand[0]],[0,p2_hand[0]])
        return [0,p2_hand[0]], H.score()

    p1_moves = [[0,c] for c in set(p1_hand)]
    if 'Banana' in p1_table:
        p1_swaps_set = set(combinations(p1_hand,2))
        p1_swaps = [[1,list(s)] for s in p1_swaps_set]

        wasabi_swap_reorders = []
        for s in p1_swaps:
            if 'Ripe' in s[1] and ('Apple' in s[1][0] or 'Apple' in s[1][1]):
                 wasabi_swap_reorders.append([1,[s[1][1],s[1][0]]])

        p1_swaps += wasabi_swap_reorders
        p1_moves += p1_swaps

    p2_moves = [[0,c] for c in set(p2_hand)]
    if 'Banana' in p2_table:
        p2_swaps_set = set(combinations(p2_hand,2))
        p2_swaps = [[1,list(s)] for s in p2_swaps_set]

        wasabi_swap_reorders = []
        for s in p2_swaps:
            if 'Ripe' in s[1] and ('Apple' in s[1][0] or 'Apple' in s[1][1]):
                 wasabi_swap_reorders.append([1,[s[1][1],s[1][0]]])

        p2_swaps += wasabi_swap_reorders
        p2_moves += p2_swaps

    ev_p2 = 1000
    for p2_move in p2_moves:
        ev_p1 = -1000

        for p1_move in p1_moves:
            H = deepcopy(G)
            H.play(p1_move, p2_move)

            ev_p1 = max(ev_p1, find_p2_best_move(H, ev_p1, ev_p2)[1])

            if beta < ev_p1:
                break

        if ev_p1 < ev_p2:
            p2_best_move = p2_move
        ev_p2 = min(ev_p1, ev_p2)

        if alpha > ev_p2:
            break

    return p2_best_move, ev_p2

if __name__ == '__main__':
    main()
