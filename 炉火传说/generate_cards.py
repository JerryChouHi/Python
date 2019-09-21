# encoding:utf-8
# @Time     : 2019/2/14 15:59
# @Author   : Jerry Chou
# @File     : generate_cards.py
# @Function :

from parse import parse_card
import random
import linecache


def generate_cards(num):
    """
    从牌库中随机取num张卡牌生成套牌，同一张橙卡最多用1张，其他卡最多2张
    :param num: 套牌数量
    :return: 
    """
    f = open('card_pool.txt', 'r', encoding='UTF-8')
    cards_line = f.readlines()
    cards = []
    card_name = []
    count = 0
    while count < num:
        random_line = random.randint(0, len(cards_line) - 1)
        card = parse_card(cards_line[random_line])
        if card.color == 'golden':
            if card_name.count(card.name) < 1:
                cards.append(card)
                card_name.append(card.name)
                count += 1
        else:
            if card_name.count(card.name) < 2:
                cards.append(card)
                card_name.append(card.name)
                count += 1
    f.close()
    return cards


def generate_mycards():
    """
    指定我方套牌
    :return: 打乱顺序
    """
    f = open('cards_my.txt', 'r', encoding='UTF-8')
    cards_line = f.readlines()
    del cards_line[0]
    random.shuffle(cards_line)
    cards = []
    for i in range(0, len(cards_line)):
        card_info = get_card_info('card_pool.txt', int(cards_line[i].strip('\n')))
        card = parse_card(card_info.strip('\n'))
        cards.append(card)
    f.close()
    return cards


def generate_enemycards():
    """
    指定敌方套牌
    :return: 打乱顺序
    """
    f = open('cards_enemy.txt', 'r', encoding='UTF-8')
    cards_line = f.readlines()
    del cards_line[0]
    random.shuffle(cards_line)
    cards = []
    for i in range(0, len(cards_line)):
        card_info = get_card_info('card_pool.txt', int(cards_line[i].strip('\n')))
        card = parse_card(card_info.strip('\n'))
        cards.append(card)
    f.close()
    return cards


def get_card_info(path, card_id):
    """
    通过卡牌id来获取卡牌信息
    :param card_id: 
    :param path: 
    :return: 
    """
    return linecache.getline(path, card_id)
