import pygame
import BlackJack
import random
import time


black = (0,0,0)
white = (255,255,255)
suits = ['C', 'H', 'D', 'S']
special = {12: 'A', 11: 'K', 10: 'Q', 9: 'J'}


class Screen(object):
    def __init__(self):
        pygame.init()
        self.font = pygame.font.Font(None, 64)
        self.display_width = 800
        self.display_height = 800
        self.gameDisplay = pygame.display.set_mode((self.display_width, self.display_height))
        pygame.display.set_caption('Roger\'s Gambling Addiction')
        pygame.display.update()
        self.deck = BlackJack.Deck()
        self.player1 = BlackJack.Player('Human', 10, 2)
        self.player2 = BlackJack.Dealer()
        self.cards_shown = []
        self.player1_cards = [[],[]]
        self.player2_cards = []
        self.temp = 0
        self.round = 1
        self.i = 0
        self.hands = 1
        self.offset = [0, 0]
        self.crashed = False
        self.game_over = False
        self.clock = pygame.time.Clock()

    def clear_display(self):
        self.gameDisplay.fill(black)
        self.cards_shown = []
        self.player1_cards = [[],[]]
        self.player2_cards = []
        self.offset = [0, 0]
        self.hands = 1
        self.player1.reset_stats()
        self.player2.reset_stats()
        self.crashed = False
        self.game_over = False
        self.clock = pygame.time.Clock()
        pygame.display.update()

    def hand_text(self, side):
        self.gameDisplay.fill(black,(0,200,800,450))
        orig_surf = self.font.render('', True, pygame.Color('royalblue'))
        if side == 0:
            orig_surf = self.font.render('Left Hand', True, pygame.Color('royalblue'))
        elif side == 1:
            orig_surf = self.font.render('Right Hand', True, pygame.Color('royalblue'))
        self.gameDisplay.blit(orig_surf, (300, 400))
        pygame.display.update()

    def loss_sequence(self):
        self.gameDisplay.fill(black, (0, 200, 800, 450))
        orig_surf = self.font.render('Game Over. You Lose', True, pygame.Color('red'))
        self.gameDisplay.blit(orig_surf, (200, 400))
        self.lose_money()
        pygame.display.update()

    def win_sequence(self):
        self.gameDisplay.fill(black, (0, 200, 800, 450))
        orig_surf = self.font.render('You Win', True, pygame.Color('royalblue'))
        self.gameDisplay.blit(orig_surf, (300, 400))
        self.win_money()
        pygame.display.update()

    def win_money(self):
        self.player1.money += self.player1.wager
        print("Money: $" + str(self.player1.money))

    def lose_money(self):
        self.player1.money -= self.player1.wager
        print("Money: $" + str(self.player1.money))

    def win_compare(self, winner, total):
        self.gameDisplay.fill(black, (0, 200, 800, 450))
        if winner == 1:
            orig_surf = self.font.render('You Win with a score of ' + str(total), True, pygame.Color('royalblue'))
            self.gameDisplay.blit(orig_surf, (100, 400))
            pygame.display.update()
        elif winner == 2:
            orig_surf = self.font.render('Dealer Wins with a score of ' + str(total), True, pygame.Color('royalblue'))
            self.gameDisplay.blit(orig_surf, (100, 400))
            pygame.display.update()
        elif winner == 3:
            orig_surf = self.font.render('Tie with a score of ' + str(total), True, pygame.Color('royalblue'))
            self.gameDisplay.blit(orig_surf, (100, 400))
            pygame.display.update()

    def flip_dealer_card(self):
        temp = self.offset[1]
        self.offset[1] = 0
        card = self.player2.cards_in_hand[0][0]
        if card in special:
            num = special[card] + random.choice(suits)
        else:
            num = str(card + 2) + random.choice(suits)
        pic = pygame.image.load('d:\\Personal Projects\\BlackJack\\Cards\\' + num + '.png')
        width = pic.get_width()
        xpos = int(self.display_width / 2 - (width * .1) / 2) + self.offset[1]
        ypos = 0
        self.show_card(pic, xpos, ypos)
        pygame.display.update()
        self.offset[1] += temp

    def shift_cards(self):
        self.gameDisplay.fill(black)
        self.offset = [0,0]
        for i in self.player2_cards:
            pic = pygame.image.load('d:\\Personal Projects\\BlackJack\\Cards\\' + i + '.png')
            width = pic.get_width()
            xpos = int(self.display_width / 2 - (width * .1) / 2) + self.offset[1]
            ypos = 0
            self.show_card(pic, xpos, ypos)
            pygame.display.update()
            self.offset[1] += int(width * .1)
        for i in self.player1_cards[0]:
            pic = pygame.image.load('d:\\Personal Projects\\BlackJack\\Cards\\' + i + '.png')
            width = pic.get_width()
            height = pic.get_height()
            xpos = 0 + self.offset[0]
            ypos = int(self.display_height - (height * .1))
            self.show_card(pic, xpos, ypos)
            pygame.display.update()
            self.offset[0] += int(width * .1)
            self.temp = int(width*.1)*2

        self.offset[0] = 0
        for i in self.player1_cards[1]:
            pic = pygame.image.load('d:\\Personal Projects\\BlackJack\\Cards\\' + i + '.png')
            width = pic.get_width()
            height = pic.get_height()
            xpos = int(self.display_width / 2 - (width * .1) / 2) + self.offset[0]
            ypos = int(self.display_height - (height * .1))
            self.show_card(pic, xpos, ypos)
            pygame.display.update()
            self.offset[0] += int(width * .1)

    def round_text(self):
        orig_surf = self.font.render('Round '+str(self.round), True, pygame.Color('white'))
        text_surf = orig_surf.copy()
        alpha = 255
        timer = 500
        while True:
            if timer > 0:
                timer -= 1
            else:
                if alpha > 0:
                    alpha = max(0, alpha-4)
                    text_surf = orig_surf.copy()
                    text_surf.fill((255, 255, 255, alpha), special_flags=pygame.BLEND_RGBA_MULT)
                else:
                    break
            self.gameDisplay.fill(black)
            self.gameDisplay.blit(text_surf, (300, 400))
            pygame.display.update()

    def show_card(self, img, x, y):
        img = pygame.transform.rotozoom(img, 0, .1)
        time.sleep(.1)
        self.gameDisplay.blit(img, (x, y))
        pygame.display.update()

    def choosecard(self, card, player, hand=0):
        if card in special:
            num = special[card] + random.choice(suits)
        else:
            num = str(card + 2) + random.choice(suits)
        pic = pygame.image.load('d:\\Personal Projects\\BlackJack\\Cards\\' + num + '.png')
        width = pic.get_width()
        height = pic.get_height()
        if type(player) is BlackJack.Player:
            if self.hands == 2:
                if hand == 0:
                    xpos = 0 + self.offset[0]
                    ypos = int(self.display_height - (height * .1))
                else:
                    xpos = int(self.display_width / 2 - (width * .1) / 2) + self.offset[0]
                    ypos = int(self.display_height - (height * .1))
            else:
                xpos = int(self.display_width / 2 - (width * .1) / 2) + self.offset[0]
                ypos = int(self.display_height - (height * .1))
            self.player1_cards[hand].append(num)
            self.offset[0] += int(width * .1)
        else:
            self.player2_cards.append(num)
            xpos = int(self.display_width / 2 - (width * .1) / 2) + self.offset[1]
            ypos = 0
            self.offset[1] += int(width * .1)
        self.show_card(pic, xpos, ypos)

    def inital_cards(self):
        card = self.deck.deal_initial_cards(self.player1, self.player2)
        num = "gray_back"
        self.player2_cards.append(num)
        pic = pygame.image.load('d:\\Personal Projects\\BlackJack\\Cards\\' + num + '.png')
        width = pic.get_width()
        xpos = int(self.display_width / 2 - (width * .1) / 2) + self.offset[1]
        ypos = 0
        self.show_card(pic, xpos, ypos)
        self.offset[1] += int(width * .1)
        for k in range(len(card)):
            if k == len(card) - 1:
                self.choosecard(card[k], self.player2)
            else:
                self.choosecard(card[k], self.player1)
            pygame.display.update()

    def fuctionApp(self):
            if __name__ == '__main__':
                while not self.crashed:
                    if self.i != self.round:
                        self.round_text()
                        self.inital_cards()
                        self.i += 1
                        side = 0
                    if self.player1.total[0] == 21 and len(self.player1.cards_in_hand[0]) == 2 and self.hands == 1:
                        self.flip_dealer_card()
                        if self.player2.total[0] != 21:
                            self.player1.money += self.player1.wager / 2
                            self.win_sequence()
                            self.game_over = True
                            time.sleep(4)
                            self.clear_display()
                            if self.deck.deck_size < 75:
                                self.deck.reset_deck()
                            self.round += 1
                        else:
                            winner, total = self.compare(self.player1,self.player2)
                            self.game_over = True
                            self.win_compare(winner, total)
                            time.sleep(4)
                            self.clear_display()
                            if self.deck.deck_size < 75:
                                self.deck.reset_deck()
                            self.round += 1
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            self.crashed = True
                        if self.hands == 2:
                            self.hand_text(side)
                        else:
                            side = 0
                        if event.type == pygame.KEYDOWN:
                            if not self.game_over:
                                if self.hands == 1:
                                    if event.key == pygame.K_d and len(self.player1.cards_in_hand[0]) == 2:
                                        card = self.deck.deal_card(self.player1)
                                        self.choosecard(card, self.player1)
                                        if not self.player1.check_total():
                                            self.game_over = True
                                            self.loss_sequence()
                                            self.loss_sequence()
                                            time.sleep(4)
                                            self.clear_display()
                                            if self.deck.deck_size < 75:
                                                self.deck.reset_deck()
                                            self.round += 1
                                        else:
                                            self.flip_dealer_card()
                                            computer_hit = self.player2.computerplay()
                                            while computer_hit:
                                                card = self.deck.deal_card(self.player2)
                                                self.choosecard(card, self.player2)
                                                computer_hit = self.player2.computerplay()
                                            if not self.player2.check_total():
                                                self.game_over = True
                                                self.win_sequence()
                                                self.win_sequence()
                                                time.sleep(4)
                                                self.clear_display()
                                                if self.deck.deck_size < 75:
                                                    self.deck.reset_deck()
                                                self.round += 1
                                            else:
                                                winner, total = BlackJack.compare(self.player1, self.player2)
                                                self.game_over = True
                                                self.win_compare(winner, total)
                                                self.win_compare(winner, total)
                                                time.sleep(4)
                                                self.clear_display()
                                                if self.deck.deck_size < 75:
                                                    self.deck.reset_deck()
                                                self.round += 1
                                    if event.key == pygame.K_s and \
                                            self.player1.cards_in_hand[0][0] == self.player1.cards_in_hand[0][1] and \
                                            len(self.player1.cards_in_hand[0]) == 2:
                                        card1, card2 = self.player1.split_hand()
                                        self.player1_cards[1].append(self.player1_cards[0][1])
                                        self.player1_cards[0].pop(1)
                                        self.choosecard(card1, self.player1, 0)
                                        self.choosecard(card2, self.player1, 1)
                                        self.shift_cards()
                                        self.hands += 1
                                        if self.player1.cards_in_hand[0][0] == 12:
                                            self.flip_dealer_card()
                                            computer_hit = self.player2.computerplay()
                                            while computer_hit:
                                                card = self.deck.deal_card(self.player2)
                                                self.choosecard(card, self.player2)
                                                computer_hit = self.player2.computerplay()
                                            if not self.player2.check_total():
                                                self.game_over = True
                                                self.win_sequence()
                                                time.sleep(4)
                                                self.clear_display()
                                                if self.deck.deck_size < 75:
                                                    self.deck.reset_deck()
                                                self.round += 1
                                            else:
                                                winner, total = BlackJack.compare(self.player1, self.player2,0)
                                                self.game_over = True
                                                self.win_compare(winner, total)
                                                winner, total = BlackJack.compare(self.player1, self.player2, 1)
                                                self.win_compare(winner, total)
                                                time.sleep(4)
                                                self.clear_display()
                                                if self.deck.deck_size < 75:
                                                    self.deck.reset_deck()
                                                self.round += 1
                                    elif event.key == pygame.K_h:
                                        card = self.deck.deal_card(self.player1)
                                        self.choosecard(card, self.player1)
                                        if not self.player1.check_total():
                                            self.game_over = True
                                            self.loss_sequence()
                                            time.sleep(4)
                                            self.clear_display()
                                            if self.deck.deck_size < 75:
                                                self.deck.reset_deck()
                                            self.round += 1
                                    elif event.key == pygame.K_c:
                                        self.flip_dealer_card()
                                        computer_hit = self.player2.computerplay()
                                        while computer_hit:
                                            card = self.deck.deal_card(self.player2)
                                            self.choosecard(card, self.player2)
                                            computer_hit = self.player2.computerplay()
                                        if not self.player2.check_total():
                                            self.game_over = True
                                            self.win_sequence()
                                            time.sleep(4)
                                            self.clear_display()
                                            if self.deck.deck_size < 75:
                                                self.deck.reset_deck()
                                            self.round += 1
                                        else:
                                            winner, total = BlackJack.compare(self.player1, self.player2)
                                            self.game_over = True
                                            self.win_compare(winner, total)
                                            time.sleep(4)
                                            self.clear_display()
                                            if self.deck.deck_size < 75:
                                                self.deck.reset_deck()
                                            self.round += 1
                                elif self.hands == 2:
                                    loss = [0,0]
                                    if event.key == pygame.K_h:
                                        card = self.deck.deal_card(self.player1, side)
                                        self.choosecard(card, self.player1, side)
                                        if not self.player1.check_total():
                                            loss[side] = 1
                                            if side == 1 and loss[side] == 1 and loss[1] == loss[0]:
                                                self.loss_sequence()
                                                self.loss_sequence()
                                                self.game_over = True
                                                time.sleep(4)
                                                self.clear_display()
                                                if self.deck.deck_size < 75:
                                                    self.deck.reset_deck()
                                                self.round += 1
                                            side += 1
                                            self.offset[0] = self.temp
                                    if event.key == pygame.K_c:
                                        if side == 0:
                                            side += 1
                                            self.offset[0] = self.temp
                                        else:
                                            self.flip_dealer_card()
                                            computer_hit = self.player2.computerplay()
                                            while computer_hit:
                                                card = self.deck.deal_card(self.player2)
                                                self.choosecard(card, self.player2)
                                                computer_hit = self.player2.computerplay()
                                            if not self.player2.check_total():
                                                self.game_over = True
                                                self.win_sequence()
                                                time.sleep(4)
                                                self.clear_display()
                                                if self.deck.deck_size < 75:
                                                    self.deck.reset_deck()
                                                self.round += 1
                                            else:
                                                winner, total = BlackJack.compare(self.player1, self.player2)
                                                self.game_over = True
                                                self.win_compare(winner, total)
                                                time.sleep(1)
                                                winner, total = BlackJack.compare(self.player1, self.player2, 1)
                                                self.win_compare(winner, total)
                                                time.sleep(4)
                                                self.clear_display()
                                                if self.deck.deck_size < 75:
                                                    self.deck.reset_deck()
                                                self.round += 1
                            if event.key == pygame.K_r:
                                self.clear_display()
                                if self.deck.deck_size < 75:
                                    self.deck.reset_deck()
                                self.round += 1
                pygame.quit()


display = Screen()
display.fuctionApp()
