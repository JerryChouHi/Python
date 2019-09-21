# encoding:utf-8
# @Time     : 2019/2/22 17:37
# @Author   : Jerry Chou
# @File     : main_v6.0.py
# @Function : 1.法力水晶从1开始每轮+1直到10
#             2.每轮敌我双方交替出牌，出的卡牌水晶总数不能超过本轮水晶数
#             3.上场的卡牌随机攻击对方场上卡牌，如果对方场上没有卡牌，则攻击对方英雄
#             4.一方英雄死亡，游戏结束
#             5.增加疲劳机制：抽完卡牌，每个回合扣血，扣血量每个回合+1
#             6.如果敌方场上卡牌>1,手动选择攻击的卡牌

from generate_cards import generate_cards
from fight import *
from random import randint

CARD_NUM = 30
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
        self.tired = 0

    def turn_round(self):
        self.show_world()
        if self.init_hand_count < CARD_NUM:
            self.myhandcards.append(self.mycards[self.init_hand_count])
            self.enemyhandcards.append(self.enemycards[self.init_hand_count])
        else:
            self.tired += 1
            print("oooooooooooooooooooooooooo本回合疲劳值为：%s" % self.tired)

        print("我方英雄血量：%s" % self.myherohealth)
        self.myherohealth -= self.tired
        if self.hero_death(self.myherohealth):
            print("~~~~~~~~~~~游戏结束，你输了游戏：我方英雄疲劳死！！！~~~~~~~~~~~~~")
        else:
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
            if len(self.myworldcards) == 0:
                print("场上没有卡牌！！！")

            self.myworldcards, self.enemyworldcards, self.enemyherohealth = self.battle(self.myworldcards,
                                                                                        self.enemyworldcards,
                                                                                        self.enemyherohealth, False)

            if self.hero_death(self.enemyherohealth):
                print("~~~~~~~~~~~~游戏结束，恭喜你获得胜利：敌方英雄被我方卡牌打死！！！~~~~~~~~~~~~")
            else:
                self.myturn = False
                print("敌方英雄血量：%s" % self.enemyherohealth)
                self.enemyherohealth -= self.tired

                if self.hero_death(self.enemyherohealth):
                    print("~~~~~~~~~~~游戏结束，恭喜你获得胜利：敌方英雄疲劳死！！！~~~~~~~~~~~~~")
                else:
                    print("^^^^敌方手牌^^^^^^^^^^^^")
                    self.show_cards(self.enemyhandcards)
                    mana = self.mana
                    for i in range(len(self.enemyhandcards) - 1, -1, -1):
                        if self.enemyhandcards[i].mana <= mana:
                            self.enemyworldcards.append(self.enemyhandcards[i])
                            print(">>>>>>>>>>>>>>>>>>")
                            print(
                                "\t%s-%s(%s)上场！！！" % (i + 1, self.enemyhandcards[i].name, self.enemyhandcards[i].mana))
                            mana -= self.enemyhandcards[i].mana
                            del self.enemyhandcards[i]

                    print("$$$$敌方场上卡牌$$$$$$$$$$$$$")
                    for card in self.enemyworldcards:
                        card.show()
                    if len(self.enemyworldcards) == 0:
                        print("场上没有卡牌！！！")

                    self.enemyworldcards, self.myworldcards, self.myherohealth = self.battle(self.enemyworldcards,
                                                                                             self.myworldcards,
                                                                                             self.myherohealth, True)

                    if self.hero_death(self.myherohealth):
                        print("~~~~~~~~~~~游戏结束，你输了游戏：我方英雄被敌方卡牌打死！！！~~~~~~~~~~~~~")
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

    def battle(self, mycards, enemycards, enemyherohealth, Auto):
        """
        攻击对方
        :param mycards: 
        :param enemycards: 
        :param enemyherohealth: 
        :param Auto: True随机对象  False手动选择
        :return: 
        """
        if len(mycards) > 0:
            for i in range(len(mycards) - 1, -1, -1):
                if mycards[i].alive:
                    if len(enemycards) > 0:
                        print("------------攻击----------------")
                        print("{0}({1}-{2}) 准备攻击：".format(mycards[i].name, mycards[i].damage, mycards[i].remain_health))
                        enemy_id = self.attack_who(enemycards, Auto)
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
                            print("%s-%s攻击敌方英雄" % (mycards[i].name, mycards[i].damage))
                            enemyherohealth -= mycards[i].damage
                            print("%%%%%%%%%%%敌方英雄生命：", enemyherohealth)
                        else:
                            print("%s-%s攻击我方英雄" % (mycards[i].name, mycards[i].damage))
                            enemyherohealth -= mycards[i].damage
                            print("%%%%%%%%%%%我方英雄生命：", enemyherohealth)
        return mycards, enemycards, enemyherohealth

    def attack_who(self, cards, auto):
        """
        敌方场上卡牌数量>1,且auto为False时，手动选择攻击对象
        :param cards: 
        :param auto: True随机对象  False手动选择
        :return: 
        """
        if len(cards) == 1:
            return 0
        elif auto:
            card_id = randint(0, len(cards) - 1)
            return card_id
        else:
            for i in range(len(cards)):
                print("{0}-{1}({2}-{3})".format(i, cards[i].name, cards[i].damage, cards[i].remain_health), end=' ')
            who = int(input("\n请选择你要攻击的卡牌："))
            if who<0 or who>=len(cards):
                print("输入有误，请重新选择！！！")
                return self.attack_who(cards, auto)
            return who

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
