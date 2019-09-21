# encoding:utf-8
# @Time     : 2019/5/13 10:45
# @Author   : Jerry Chou
# @File     : card_collection.py
# @Function : 卡牌集合

import random
from generate_cards import *
from parse import *


def get_card_pool():
    """
    获取卡池中的非衍生卡
    :return: 
    """
    card_list = []
    f = open('card_pool.txt', 'r', encoding='UTF-8')
    cards_line = f.readlines()
    while '\n' in cards_line:
        cards_line.remove('\n')
    for card_line in cards_line:
        card = parse_card(card_line)
        if card.occupation != 'Derivation':
            card_list.append(card)
    f.close()
    return card_list

def lich_king_cards():
    """
    巫妖王的衍生卡，随机返回一个
    :return: 
    """
    lich_king_list = [parse_card(get_card_info(1013).strip('\n')),  # 对一个敌方角色造成5点伤害，或为一个友方角色恢复5点生命值
                      parse_card(get_card_info(1014).strip('\n')),  # 从你对手的牌库里偷取一个随从，并把它加入你的手牌
                      parse_card(get_card_info(1015).strip('\n')),  # 消灭一个随从，你的英雄受到等同于它生命值的伤害
                      parse_card(get_card_info(1016).strip('\n')),  # 对所有敌方角色造成3点伤害
                      parse_card(get_card_info(1017).strip('\n')),  # 使你的随从获得+2/+2和“无法才成为法术或英雄技能的目标”
                      parse_card(get_card_info(1018).strip('\n')),  # 消灭所有随从，每有一个随从被消灭，就弃掉你牌库顶端的1张牌
                      parse_card(get_card_info(1019).strip('\n')),  # 弃掉你牌库顶端的5张牌，召唤其中所有被弃掉的随从
                      parse_card(get_card_info(1020).strip('\n'))]  # 亡语：召唤所有被该武器消灭的随从
    return random.choice(lich_king_list)


def ysera_cards():
    """
    伊瑟拉的衍生卡，随机返回一个
    :return: 
    """
    ysera_list = [parse_card(get_card_info(1021).strip('\n')),  # 将一个随从返回到其拥有者的手上
                  parse_card(get_card_info(1022).strip('\n')),  # 使一个角色获得+5+5，并在你下个回合开始时摧毁它
                  parse_card(get_card_info(1023).strip('\n')),  # 对所有除伊瑟拉外的生物造成五点伤害
                  parse_card(get_card_info(1024).strip('\n')),  # 无法成为英雄能力或者法术的目标
                  parse_card(get_card_info(1025).strip('\n'))  #
                  ]
    return random.choice(ysera_list)


def master_treasure_chest_cards():
    """
    大师宝箱的衍生卡,随机返回一个
    :return: 
    """
    master_treasure_chest_list = [parse_card(get_card_info(1027).strip('\n')),  # 将你的手牌替换为传说随从
                                  parse_card(get_card_info(1028).strip('\n')),  # 抽一张牌，将该牌的复制置入你的手牌，直到手牌数量达到上限
                                  parse_card(get_card_info(1029).strip('\n')),  # 抽三张牌，其法力值消耗为0点
                                  parse_card(get_card_info(1030).strip('\n'))  # 发现一张传说随从牌，召唤它的两个复制
                                  ]
    return random.choice(master_treasure_chest_list)
