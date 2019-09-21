# encoding:utf-8
# @Time     : 2019/5/13 9:24
# @Author   : Jerry Chou
# @File     : hero.py
# @Function : 英雄类

from card import Card
from generate_cards import *

class Hero(Card):
    def __init__(self, hero):
        super().__init__(int(hero[0]), hero[1], hero[2], hero[3], int(hero[4]), int(hero[5]), int(hero[6]), hero[7], hero[8],hero[9])
        # Card.__init__(self, int(hero[0]), hero[1], hero[2], hero[3], int(hero[4]), int(hero[5]), int(hero[6]), hero[7], hero[8],hero[9])
        self.say_hi = hero[12]
        self.surrender = hero[13]
        self.use_skill = False
        self.tired = 0
        self.hero_damage = 0
        self.frostmourne_kill_list = []
        self.cast_list = []
        if hero[8] == 'Shaman':
            stone_totem = parse_card(get_card_info('card_pool.txt',1109).strip('\n'))
            airfury_totem = parse_card(get_card_info('card_pool.txt',1110).strip('\n'))
            heal_totom = parse_card(get_card_info('card_pool.txt',1111).strip('\n'))
            hot_totem = parse_card(get_card_info('card_pool.txt',1112).strip('\n'))
            self.totem = [stone_totem, airfury_totem, heal_totom, hot_totem]

    def add_kill(self, kill):
        """
        添加霜之哀伤消灭的随从
        :param kill: 
        :return: 
        """
        self.frostmourne_kill_list.append(kill)

