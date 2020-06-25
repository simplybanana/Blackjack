import random
import pandas as pd

special_cards = {9: 'Jack', 10: 'Queen', 11: 'King', 12: 'Ace'}


def card_given(card, name):
    if card in special_cards:
        print(name + " dealt a " + special_cards[card])
    else:
        print(name + " dealt a " + str(card + 2))


class Deck(object):
    def __init__(self):
        self.deck_size = 52*6
        self.copy_of_cards = 4*6
        self.cards_left = [4*6]*13

    def reset_deck(self):
        self.deck_size = 52 * 6
        self.copy_of_cards = 4 * 6
        self.cards_left = [4 * 6] * 13

    def cardshown(self, card):
        self.cards_left[card] -= 1
        self.deck_size -= 1

    def deal_initial_cards(self, player1, player2):
        cards = []
        for i in range(2):
            card = random.randint(0, 12)
            while self.cards_left[card] == 0:
                card = random.randint(0, 12)
            self.cardshown(card)
            cards.append(card)
            player1.add_value(card)
            player1.update_card_seen(card)
            card_given(card, player1.name)
            card = random.randint(0, 12)
            while self.cards_left[card] == 0:
                card = random.randint(0, 12)
            self.cardshown(card)
            player2.add_value(card)
            player2.update_card_seen(card)
            if i == 1:
                player1.update_card_seen(card)
                card_given(card, player2.name)
                cards.append(card)
        player1.print_total()
        player2.print_total()
        return cards

    def deal_card(self, player1, hand=0):
        card = random.randint(0, 12)
        while self.cards_left[card] == 0:
            card = random.randint(0, 12)
        self.cardshown(card)
        player1.add_value(card, hand)
        player1.update_card_seen(card)
        card_given(card, player1.name)
        """if not player1.check_total():
            player1.print_total()
            print(player1.name + " has lost")"""
        return card


class Player(Deck):
    def __init__(self, name='Dealer', start_mon=0, wager=2):
        self.seen_cards = []
        self.total = [0,0]
        self.cards_in_hand = [[],[]]
        self.name = name
        self.money = start_mon
        self.wager = wager
        self.num_hands = 1
        super().__init__()

    def reset_stats(self, wager=2):
        self.num_hands = 1
        self.seen_cards = []
        self.wager = wager
        self.total = [0,0]
        self.cards_in_hand = [[],[]]

    def add_value(self, card, hand=0):
        self.cards_in_hand[hand].append(card)
        self.get_total(hand)

    def update_card_seen(self, card):
        self.seen_cards.append(card)
        self.deck_size -= 1

    def get_total(self, hand):
        self.total[hand] = 0
        for card in self.cards_in_hand[hand]:
            if card == 12:
                card = 9
            elif card > 8:
                card = 8
            self.total[hand] += card + 2

    def print_total(self):
        print(self.name + " total is " + str(self.total))

    def check_total(self, hand=0):
        aces = self.cards_in_hand[hand].count(12)
        j = 0
        self.get_total(hand)
        while self.total[hand] > 21:
            if j == aces:
                #print(self.name + " total is " + str(self.total))
                #print(self.name + " loses")
                return False
            else:
                self.total[hand] -= 10
                j += 1
        return True

    def double(self):
        self.wager = self.wager*2
        self.deal_card(self, 0)

    def split_hand(self):
        self.cards_in_hand[1].append(self.cards_in_hand[0][1])
        self.cards_in_hand[0].pop(1)
        card1 = self.deal_card(self,0)
        card2 = self.deal_card(self,1)
        self.get_total(0)
        self.get_total(1)
        self.num_hands += 1
        return card1,card2


class Dealer(Player):
    def computerplay(self):
        if self.total[0] >= 17:
            return False
        return True


class ComputerHuman(Player):
    def __init__(self, name="Ideal", wager=2):
        self.status = ['h','c']
        super().__init__(name,wager=wager)

    def hard_hands(self, hand=0):
        if 11 >= self.total[hand] >= 9:
            if self.num_hands != 2 and len(self.cards_in_hand[hand]) == 2:
                if self.total[hand] == 9:
                    if self.seen_cards[-1] in [1,2,3,4]:
                        self.status[hand] = 'd'
                elif self.total[hand] == 10:
                    if self.seen_cards[-1] <= 7:
                        self.status[hand] = 'd'
                elif self.total[hand] == 11:
                    if self.seen_cards[-1] != 12:
                        self.status[hand] = 'd'
        elif self.total[hand] == 12 and 4 >= self.seen_cards[-1] >= 2:
            self.status[hand] = 'c'
        elif 16 >= self.total[hand] >= 13 and self.seen_cards[-1] <= 4:
            self.status[hand] = 'c'
        elif 21 >= self.total[hand] >= 17:
            self.status[hand] = 'c'

    def soft_hands(self, hand=0):
        if 17 >= self.total[hand] >= 13:
            if self.num_hands != 2 and len(self.cards_in_hand[hand]) == 2:
                if self.total[hand] == 13:
                    self.status[hand] = 'd'
                elif 15 >= self.total[hand] >= 14 and 4 >= self.seen_cards[-1] >= 3:
                    self.status[hand] = 'd'
                elif self.total[hand] == 16 and 4 >= self.seen_cards[-1] >= 2:
                    self.status[hand] = 'd'
                elif self.total[hand] == 17 and 4 >= self.seen_cards[-1] >= 1:
                    self.status[hand] = 'd'
        elif self.total[hand] == 18:
            if self.num_hands != 2 and len(self.cards_in_hand[hand]) == 2:
                if 4 >= self.seen_cards[-1] >= 1:
                    self.status[hand] = 'd'
            elif self.seen_cards[-1] <= 6:
                self.status[hand] = 'c'
        elif 21 >= self.total[hand] >= 19:
            self.status[hand] = 'c'

    def splits(self,hand=0):
        if 3 >= self.cards_in_hand[0][0] >= 2 and 5 >= self.seen_cards[-1] >= 2:
            self.status[hand] = 's'
        elif self.cards_in_hand[0][0] == 5 and 7 >= self.seen_cards[-1]:
            self.status[hand] = 'd'
        elif self.cards_in_hand[0][0] == 6 and 4 >= self.seen_cards[-1] >= 1:
            self.status[hand] = 's'
        elif self.cards_in_hand[0][0] == 7 and self.seen_cards[-1] <= 5:
            self.status[hand] = 's'
        elif self.cards_in_hand[0][0] == 8:
            self.status[hand] = 's'
        elif self.cards_in_hand[0][0] == 9:
            if self.seen_cards[-1] in [0, 1, 2, 3, 4, 6, 7]:
                self.status[hand] = 's'
            else:
                self.status[hand] = 'c'
        elif 11 >= self.cards_in_hand[0][0] >= 8:
            self.status[hand] = 'c'
        elif self.cards_in_hand[0][0] == 12:
            self.status[hand] = 's'

    def opt_play(self, hand=0):
        aces = self.cards_in_hand[hand].count(12)
        if aces == 2 and self.num_hands == 1 and self.cards_in_hand[0][0] == self.cards_in_hand[0][1]:
            self.splits()
        elif aces == 0:
            if self.num_hands == 1 and self.cards_in_hand[0][0] == self.cards_in_hand[0][1] and len(self.cards_in_hand[0]) == 2:
                self.splits()
            else:
                self.hard_hands(hand)
        else:
            self.soft_hands(hand)

    def reinforce(self, hand=0):
        states = pd.read_csv('states.csv', index_col=0)
        if self.cards_in_hand[hand][0] == self.cards_in_hand[hand][1]:
            same = 0
        else:
            same = 1
        if 12 in self.cards_in_hand[hand]:
            aces = 0
        else:
            aces = 1
        if len(self.seen_cards) > 3:
            start = 1
        else:
            start = 0
        self.check_total(hand)
        b = states['total'] == self.total[hand]
        c = states['dealer card'] == self.seen_cards[2]
        d = states['Start'] == start
        e = states['Ace'] == aces
        f = states['same card'] == same
        index_state = states[b & c & d & e & f].index.tolist()[0]
        self.status[hand] = states.iloc[index_state, 5:9].idxmax(axis=1)[0].lower()
        print("INDEX: ", index_state)


def compare(player1, player2, hand=0):
    under = player1.check_total(hand)
    if player1.total[hand] > player2.total[0] and under:
        print(player1.name + " has won")
        player1.money += player1.wager
        print("Money: $" + str(player1.money))
        return 1, player1.total[hand]
    elif player2.total[0] > player1.total[hand] or not under:
        print(player2.name + " has won")
        player1.money -= player1.wager
        print("Money: $" + str(player1.money))
        return 2, player2.total[0]
    else:
        print('It was a Tie')
        print("Money: $" + str(player1.money))
        return 3, player2.total[0]


def play():
    deck = Deck()
    human = ComputerHuman()
    computer = Dealer()
    deck.deal_initial_cards(human, computer)
    decision = human.humanplay()
    j = True
    k = True
    while decision:
        deck.deal_card(human)
        if not human.check_total():
            j = False
            break
        decision = human.humanplay()
    compdecision = computer.computerplay()
    while compdecision and j:
        deck.deal_card(computer)
        compdecision = computer.computerplay()
        if not computer.check_total():
            k = False
            break
    if j and k:
        human.print_total()
        computer.print_total()
        compare(human, computer)
    elif k:
        computer.print_total()
    elif j:
        human.print_total()


def test_play():
    deck = Deck()
    human = ComputerHuman('ComputerHuman')
    computer = Dealer()
    for k in range(1000):
        deck.deal_initial_cards(human, computer)
        hand = 0
        while human.status[0] != 'c' or human.status[1] != 'c':
            if human.status[0] == 'c' and human.status[1] != 'c':
                hand = 1
            human.opt_play(hand)
            if human.status[hand] == 'd':
                human.double()
                human.status[hand] = 'c'
            elif human.status[hand] == 's':
                human.split_hand()
                human.status[0] = 'h'
                human.status[1] = 'h'
                if human.cards_in_hand[0][0] == '12':
                    human.status[0] = 'c'
                    human.status[1] = 'c'
            elif human.status[hand] == 'h':
                deck.deal_card(human, hand)
            under = human.check_total(hand)
            if not under:
                human.status[hand] = 'c'
        compdecision = computer.computerplay()
        while compdecision:
            deck.deal_card(computer)
            if not computer.check_total():
                break
            compdecision = computer.computerplay()
        i = 1
        while i <= human.num_hands:
            if not human.check_total(i - 1):
                print("ComputerHuman Lost")
                human.money -= human.wager
                print("Money: $" + str(human.money))
            elif not computer.check_total():
                print("Dealer lost")
                human.money += human.wager
                print("Money: $" + str(human.money))
            else:
                compare(human, computer, i - 1)
            i += 1
        if deck.deck_size <= 75:
            deck.reset_deck()
        human.reset_stats()
        human.status = ['h', 'c']
        computer.reset_stats()
    return human.money


def reinforce_play():
    deck = Deck()
    human = ComputerHuman('ComputerHuman')
    computer = Dealer()
    for k in range(1000):
        print("%%%%%%%%New Game%%%%%%%%%%%%")
        deck.deal_initial_cards(human, computer)
        hand = 0
        while human.status[0] != 'c' or human.status[1] != 'c':
            if human.status[0] == 'c' and human.status[1] != 'c':
                hand = 1
            human.reinforce(hand)
            if human.status[hand] == 'd':
                print('double')
                human.double()
                human.status[hand] = 'c'
            elif human.status[hand] == 's':
                print('split')
                human.split_hand()
                human.status[0] = 'h'
                human.status[1] = 'h'
                if human.cards_in_hand[0][0] == '12':
                    print("aces")
                    human.status[0] = 'c'
                    human.status[1] = 'c'
            elif human.status[hand] == 'h':
                print('hit')
                deck.deal_card(human, hand)
            under = human.check_total(hand)
            print(human.total[hand])
            print(under)
            if not under:
                print('over')
                human.status[hand] = 'c'
        compdecision = computer.computerplay()
        while compdecision:
            deck.deal_card(computer)
            if not computer.check_total():
                break
            compdecision = computer.computerplay()
        i = 1
        while i <= human.num_hands:
            if not human.check_total(i - 1):
                print("ComputerHuman Lost")
                human.money -= human.wager
                print("Money: $" + str(human.money))
            elif not computer.check_total():
                print("Dealer lost")
                human.money += human.wager
                print("Money: $" + str(human.money))
            else:
                compare(human, computer, i - 1)
            i += 1
        if deck.deck_size <= 75:
            deck.reset_deck()
        human.reset_stats()
        human.status = ['h', 'c']
        computer.reset_stats()
    return human.money


if __name__ == '__main__':
    re_mon = 0
    t_mon = 0
    for i in range(100):
        re_mon += reinforce_play()
    """for i in range(100):
        t_mon += test_play()"""
    print(re_mon/100)
    print(t_mon/100)
    #reinforce_play()