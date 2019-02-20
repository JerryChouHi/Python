# encoding:utf-8
# @Time     : 2019/2/14 15:59
# @Author   : Jerry Chou
# @File     : generate_cards.py
# @Function :

from parse import parse_card
from random import randint


def generate_cards(num):
    f = open('card_pool.txt', 'r', encoding='UTF-8')
    cards_line = f.readlines()
    cards = []
    for i in range(num):
        cards.append(parse_card(cards_line[randint(0, len(cards_line) - 1)]))
        # cards[i].show()
    return cards
