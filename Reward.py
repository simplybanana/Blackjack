import numpy as np
import pandas as pd
import BlackJack
import random


def create_q_table():
    q_table = pd.DataFrame()
    m = 0
    for i in range(4,23):
        for j in range(0,13):
            for k in range(0,2):
                q = pd.DataFrame(
                    {'total': i, 'dealer card': j, 'Start': k, 'Ace': 0, 'same card': 0, 'Check': 0, 'Hit': 0,
                     'Split': 0, 'Double': 0}, index=[m])
                m += 1
                q_table = q_table.append(q)
                q = pd.DataFrame(
                    {'total': i, 'dealer card': j, 'Start': k, 'Ace': 1, 'same card': 0, 'Check': 0, 'Hit': 0,
                     'Split': 0, 'Double': 0}, index=[m])
                m += 1
                q_table = q_table.append(q)
                q = pd.DataFrame(
                    {'total': i, 'dealer card': j, 'Start': k, 'Ace': 0, 'same card': 1, 'Check': 0, 'Hit': 0,
                     'Split': 0, 'Double': 0}, index=[m])
                m += 1
                q_table = q_table.append(q)
                q = pd.DataFrame(
                    {'total': i, 'dealer card': j, 'Start': k, 'Ace': 1, 'same card': 1, 'Check': 0, 'Hit': 0,
                     'Split': 0, 'Double': 0}, index=[m])
                m += 1
                q_table = q_table.append(q)
    q_table.to_csv('states.csv')
    #q_table.to_excel('states.xlsx')


def update_q_table():
    states = pd.read_csv('states.csv', index_col=0)
    for j in range(2, 4):
        for l in range(0, 13):
            for k in range(0, 13):
                alpha = .8
                gamma = .4
                epsilon = .8
                for i in range(1000):
                    print('%%%%%%%%%%%%%%%NEW GAME%%%%%%%%%%%%%%%%%%%%%%%')
                    deck = BlackJack.Deck()
                    human = BlackJack.ComputerHuman('ComputerHuman', wager=1)
                    computer = BlackJack.Dealer()
                    #deck.deal_initial_cards(human, computer)
                    human.cards_in_hand[0].append(j)
                    human.cards_in_hand[0].append(l)
                    print(human.cards_in_hand[0][0], human.cards_in_hand[0][1])
                    computer.cards_in_hand[0].append(random.randint(0,12))
                    computer.cards_in_hand[0].append(k)
                    print(computer.cards_in_hand[0][1])
                    hand = 0
                    start = 0
                    next_max = 0
                    reward = 0
                    while human.status[0] != 'c' or human.status[1] != 'c':
                        if human.status[0] == 'c' and human.status[1] != 'c':
                            hand = 1
                        human.check_total(hand)
                        b, c, d, e, f = state_var(human, computer, start, hand, states)
                        index_state = states[b & c & d & e & f].index.tolist()[0]
                        if random.uniform(0, 1) < epsilon:
                            human.status[hand] = random.choice(['c', 'h', 's', 'd'])
                        else:
                            print("INDEX: ",states.iloc[index_state, 5:9].idxmax(axis=1))
                            human.status[hand] = states.iloc[index_state, 5:9].idxmax(axis=1)[0].lower()
                        num = decision(human.status[hand])
                        old_value = states.iloc[index_state, num]
                        if human.status[hand] == 'c':
                            computer_play(computer, deck)
                            if not human.check_total(hand):
                                reward = -human.wager
                            elif not computer.check_total(0):
                                reward = human.wager*2
                            else:
                                result, total = BlackJack.compare(human, computer, hand)
                                if result == 1:
                                    reward = human.wager*2
                                elif result == 2:
                                    reward = -human.wager
                                elif result == 3:
                                    reward = human.wager*.1
                            next_max = states.iloc[index_state, 5:9].max()
                            human.status[hand] = 'c'
                        elif human.status[hand] == 'h':
                            deck.deal_card(human, hand)
                            start = 1
                            if human.check_total(hand):
                                b, c, d, e, f = state_var(human, computer, start,hand,states)
                                next_index_state = states[b & c & d & e & f].index.tolist()[0]
                                next_max = states.iloc[next_index_state, 5:9].max()
                                reward = human.wager * .1
                            else:
                                reward = -human.wager
                                human.status[hand] = 'c'
                                next_max = states.iloc[index_state, 5:9].max()
                        elif human.status[hand] == 's':
                            if start == 0 and human.cards_in_hand[hand][0] == human.cards_in_hand[hand][1]:
                                start = 1
                                human.split_hand()
                                human.status[0] = 'h'
                                human.status[1] = 'h'
                                b, c, d, e, f = state_var(human, computer, start, 0, states)
                                next_index_state = states[b & c & d & e & f].index.tolist()[0]
                                next_max = states.iloc[next_index_state, 5:9].max()
                                b, c, d, e, f = state_var(human, computer, start, 1, states)
                                next_index_state = states[b & c & d & e & f].index.tolist()[0]
                                next_max += states.iloc[next_index_state, 5:9].max()
                                reward = 2*human.wager * .1
                            else:
                                reward = -1
                                next_max = states.iloc[index_state, 5:9].max()
                        elif human.status[hand] == 'd':
                            if start == 0:
                                human.double()
                                start = 1
                                if human.check_total(hand):
                                    computer_play(computer, deck)
                                    result, total = BlackJack.compare(human, computer, hand)
                                    if result == 1:
                                        reward = human.wager*2
                                    elif result == 2:
                                        reward = -human.wager
                                    elif result == 3:
                                        reward = human.wager * .1
                                    next_max = states.iloc[index_state, 5:9].max()
                                    human.status[0] = 'c'
                                else:
                                    reward = -human.wager
                                    human.status[hand] = 'c'
                                    next_max = states.iloc[index_state, 5:9].max()
                            else:
                                reward = -1
                                next_max = states.iloc[index_state, 5:9].max()
                        new_value = (1-alpha)*old_value + alpha*(reward + gamma*next_max)
                        states.iloc[index_state, num] = new_value
                    if i % 50 == 0:
                        epsilon -= .035
                        alpha -= .035
                    states.to_csv('states.csv')


def computer_play(computer,deck):
    compdecision = computer.computerplay()
    while compdecision:
        deck.deal_card(computer)
        if not computer.check_total():
            break
        compdecision = computer.computerplay()


def state_var(human,computer,start,hand,states):
    if human.cards_in_hand[hand][0] == human.cards_in_hand[hand][1]:
        same = 0
    else:
        same = 1
    if 12 in human.cards_in_hand[hand]:
        aces = 0
    else:
        aces = 1
    human.check_total(hand)
    b = states['total'] == human.total[hand]
    c = states['dealer card'] == computer.cards_in_hand[0][1]
    d = states['Start'] == start
    e = states['Ace'] == aces
    f = states['same card'] == same
    return b,c,d,e,f


def decision(action):
    if action == "c":
        num = 5
    elif action == "h":
        num = 6
    elif action == "s":
        num = 7
    elif action == "d":
        num = 8
    else:
        num = 0
    return num


create_q_table()
update_q_table()
