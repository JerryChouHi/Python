# encoding:utf-8
# @Time     : 2019/2/13 17:37
# @Author   : Jerry Chou
# @File     : main_v2.0.py
# @Function : 双方随机得到多张卡牌，所有卡牌混战，直至一方全部死亡

from fight import *
from generate_cards import generate_cards
from random import randint
CARD_NUM = 2


def main():
    print("**************我的卡牌**************")
    mycards = generate_cards(CARD_NUM)
    print("**************敌方卡牌**************")
    enemycards = generate_cards(CARD_NUM)

    print()
    print("$$$$$$$$$$$$开始游戏$$$$$$$$$$$$")
    if randint(0, 1) == 1:
        battle(mycards, enemycards, 1)
    else:
        battle(enemycards, mycards, 1)

    print("$$$$$$$$$$$$游戏结束$$$$$$$$$$$$")
    print()

    if anybody_alive(mycards):
        print("您赢得了游戏！！！")
    elif anybody_alive(enemycards):
        print("您输了游戏，继续加油！！！")
    else:
        print("平分秋色！！！")


if __name__ == '__main__':
    main()
