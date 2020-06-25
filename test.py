class Deck(object):
    def __init__(self):
        self.cards_in_deck = [4]*13
        self.deck_size = sum(self.cards_in_deck)
        self.cards_in_hand = []
        self.total = 0

    def subtract_cards(self,card):
        self.cards_in_deck[card] -= 1
        self.deck_size -= 1
        self.cards_in_hand.append(card)
        self.get_total()

    def get_total(self):
        self.total = 0
        for card in self.cards_in_hand:
            if card == 12:
                card = 9
            elif card > 8:
                card = 8
            self.total += card + 2

    def prob(self, tot, basechance=1, chance=None, theodeck=None):
        if chance is None:
            chance = [0]
        if theodeck is None:
            theodeck = self.cards_in_deck
        j = 0
        goal = 21
        if tot == goal:
            return chance
        else:
            good_cards = goal-tot
            for i in range(1, good_cards+1):
                
                chance.append(basechance)
                j += 1
        return chance

    def recur_prob(self, tot, chance, j, theodeck):

        return chance

"""deck = Deck()
deck.subtract_cards(7)
deck.subtract_cards(8)
deck.prob(deck.total)
print(deck.total)
print(deck.deck_size)"""
a = ['c','d']
a[0] = 'e'
print(a)
