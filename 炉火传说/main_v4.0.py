# encoding:utf-8
# @Time     : 2019/2/19 17:37
# @Author   : Jerry Chou
# @File     : main_v4.0.py
# @Function : 1.法力水晶从1开始每轮+1直到10
#             2.每轮敌我双方交替出牌，出的卡牌水晶总数不能超过本轮水晶数
#             3.上场的卡牌随机攻击对方场上卡牌，如果对方场上没有卡牌，则攻击对方英雄
#             4.一方英雄死亡，游戏结束

from generate_cards import generate_cards
from fight import *
from random import randint

CARD_NUM = 10
INIT_HAND_COUNT = 3
HERO_HEALTH = 30


class world:
    def __init__(self):
        self.mana = 1
        self.myworldcards = []
        self.enemyworldcards = []
        self.myherohealth = HERO_HEALTH
        self.enemyherohealth = HERO_HEALTH
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
        self.myturn = True

    def turn_round(self):
        self.show_world()
        if self.init_hand_count < CARD_NUM:
            self.myhandcards.append(self.mycards[self.init_hand_count])
        print("^^^^我方手牌^^^^^^^^^^^^")
        self.show_cards(self.myhandcards)
        mana = self.mana
        for i in range(len(self.myhandcards) - 1, -1, -1):
            if self.myhandcards[i].mana <= mana:
                self.myworldcards.append(self.myhandcards[i])
                print(">>>>>>>>>>>>>>>>>>")
                print("\t%s-%s(%s)上场！！！" % (i + 1, self.myhandcards[i].name, self.myhandcards[i].mana))
                mana -= self.myhandcards[i].mana
                del self.myhandcards[i]

        print("$$$$我方场上卡牌$$$$$$$$$$$$$")
        for card in self.myworldcards:
            card.show()

        self.myworldcards, self.enemyworldcards, self.enemyherohealth = self.battle(self.myworldcards,
                                                                                    self.enemyworldcards,
                                                                                    self.enemyherohealth)

        if self.hero_death(self.enemyherohealth):
            print("~~~~~~~~~~~~游戏结束，恭喜你获得胜利！！！~~~~~~~~~~~~")
        else:
            self.myturn = False

            if self.init_hand_count < CARD_NUM:
                self.enemyhandcards.append(self.enemycards[self.init_hand_count])
            print("^^^^敌方手牌^^^^^^^^^^^^")
            self.show_cards(self.enemyhandcards)
            mana = self.mana
            for i in range(len(self.enemyhandcards) - 1, -1, -1):
                if self.enemyhandcards[i].mana <= mana:
                    self.enemyworldcards.append(self.enemyhandcards[i])
                    print(">>>>>>>>>>>>>>>>>>")
                    print("\t%s-%s(%s)上场！！！" % (i + 1, self.enemyhandcards[i].name, self.enemyhandcards[i].mana))
                    mana -= self.enemyhandcards[i].mana
                    del self.enemyhandcards[i]

            print("$$$$敌方场上卡牌$$$$$$$$$$$$$")
            for card in self.enemyworldcards:
                card.show()

            self.enemyworldcards, self.myworldcards, self.myherohealth = self.battle(self.enemyworldcards,
                                                                                     self.myworldcards,
                                                                                     self.myherohealth)

            if self.hero_death(self.myherohealth):
                print("~~~~~~~~~~~游戏结束，你输了游戏！！！~~~~~~~~~~~~~")
            else:
                self.round += 1

                # 水晶达到10后不再增加
                if self.mana < 10:
                    self.mana += 1

                self.init_hand_count += 1

                self.myturn = True

                self.turn_round()

    def show_world(self):
        print("++++++++++++++++++当前回合：%s,当前水晶：%s" % (self.round, self.mana))

    def show_cards(self, cards):
        for i, card in enumerate(cards):
            print("\t%s-%s(%s)" % (i + 1, card.name, card.mana))

    def battle(self, mycards, enemycards, enemyherohealth):
        """
        我方卡牌依次随机攻击对方卡牌，如果对方没有卡牌，攻击对方英雄
        :param mycards: 
        :param enemycards: 
        :param enemyherohealth: 
        :return: 
        """
        if len(mycards) > 0:
            for i in range(len(mycards) - 1, -1, -1):
                if mycards[i].alive:
                    if len(enemycards) > 0:
                        print("------------攻击----------------")
                        enemy_id = self.attack_who(enemycards)
                        print("%s%s-%s attack %s%s-%s" % (
                            mycards[i].name, mycards[i].damage, mycards[i].remain_health,
                            enemycards[enemy_id].name, enemycards[enemy_id].damage, enemycards[enemy_id].remain_health))
                        mycards[i].attack(enemycards[enemy_id])
                        mycards[i].show()
                        enemycards[enemy_id].show()
                        if mycards[i].alive == False:
                            del mycards[i]
                        if enemycards[enemy_id].alive == False:
                            del enemycards[enemy_id]
                    else:
                        if self.myturn:
                            print("%%%%%%%%%%%敌方英雄生命：", enemyherohealth)
                            print("%s-%s攻击敌方英雄" % (mycards[i].name, mycards[i].damage))
                            enemyherohealth -= mycards[i].damage
                            print("%%%%%%%%%%%敌方英雄生命：", enemyherohealth)
                        else:
                            print("%%%%%%%%%%%我方英雄生命：", enemyherohealth)
                            print("%s-%s攻击我方英雄" % (mycards[i].name, mycards[i].damage))
                            enemyherohealth -= mycards[i].damage
                            print("%%%%%%%%%%%我方英雄生命：", enemyherohealth)
        return mycards, enemycards, enemyherohealth

    def attack_who(self, cards):
        """
        随机找一个对方场上的一个卡牌的id
        :param obj: 
        :return: 
        """
        card_id = randint(0, len(cards) - 1)
        return card_id

    def hero_death(self, hero):
        """
        英雄是否死亡
        :param hero: 
        :return: 
        """
        if hero <= 0:
            return True


def main():
    game = world()
    game.turn_round()


if __name__ == '__main__':
    main()
