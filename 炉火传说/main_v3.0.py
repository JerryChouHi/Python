# encoding:utf-8
# @Time     : 2019/2/13 17:37
# @Author   : Jerry Chou
# @File     : main_v3.0.py
# @Function : 法力水晶从1开始递增直到10，根据法力水晶多少来出牌

from fight import *
from generate_cards import generate_cards

CARD_NUM = 10
INIT_HAND_COUNT = 3


class world:
    def __init__(self):
        self.mana = 1
        self.myworldcards = []
        self.enemyworldcards = []
        self.init_hand_count = INIT_HAND_COUNT
        print("**************我的卡牌**************")
        self.mycards = generate_cards(CARD_NUM)
        self.show_cards(self.mycards)
        self.myhandcards = self.mycards[:INIT_HAND_COUNT]
        print("**************敌方卡牌**************")
        self.enemycards = generate_cards(CARD_NUM)
        self.show_cards(self.enemycards)
        self.enemyhandcards = self.enemycards[:INIT_HAND_COUNT]
        self.round = 1

    def turn_round(self):
        self.show_world()

        self.myhandcards.append(self.mycards[self.init_hand_count])
        print("^^^^^^^^^^^^^^^^")
        print("我方手牌:")
        self.show_cards(self.myhandcards)
        mana = self.mana
        for i in range(len(self.myhandcards)-1,-1,-1):
            if self.myhandcards[i].mana <= mana:
                self.myworldcards.append(self.myhandcards[i])
                print(">>>>>>>>>>>>>>>>>>")
                print("\t%s-%s(%s)上场！！！" % (i+1,self.myhandcards[i].name, self.myhandcards[i].mana))
                mana -= self.myhandcards[i].mana
                del self.myhandcards[i]

        print("$$$$$$$$$$$$$$$$$")
        print("我方场上卡牌：")
        for card in self.myworldcards:
            card.show()

        self.enemyhandcards.append(self.enemycards[self.init_hand_count])
        print("^^^^^^^^^^^^^^^^")
        print("敌方手牌:")
        self.show_cards(self.enemyhandcards)
        mana = self.mana
        for i in range(len(self.enemyhandcards)-1,-1,-1):
            if self.enemyhandcards[i].mana <= mana:
                self.enemyworldcards.append(self.enemyhandcards[i])
                print(">>>>>>>>>>>>>>>>>>")
                print("\t%s-%s(%s)上场！！！" % (i+1,self.enemyhandcards[i].name, self.enemyhandcards[i].mana))
                mana -= self.enemyhandcards[i].mana
                del self.enemyhandcards[i]

        print("$$$$$$$$$$$$$$$$$")
        print("敌方场上卡牌：")
        for card in self.enemyworldcards:
            card.show()

        self.round += 1

        # 水晶达到10后不再增加
        if self.mana < 10:
            self.mana += 1

        self.init_hand_count += 1

        # 牌库中有牌时抽牌
        if self.init_hand_count<CARD_NUM:
            self.turn_round()

    def show_world(self):
        print("+++++++++++++++++++++++++++++++++++++++++++++")
        print("当前回合：%s,当前水晶：%s" % (self.round, self.mana))

    def show_cards(self,cards):
        for i,card in enumerate(cards):
            print("\t%s-%s(%s)" % (i+1,card.name, card.mana))




def main():
    game = world()
    game.turn_round()


if __name__ == '__main__':
    main()
