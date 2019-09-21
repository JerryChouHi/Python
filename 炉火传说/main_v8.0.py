# encoding:utf-8
# @Time     : 2019/3/4 17:37
# @Author   : Jerry Chou
# @File     : main_v8.0.py
# @Function : 1.法力水晶从1开始每轮+1直到10
#             2.每轮敌我双方交替出牌，出的卡牌水晶总数不能超过本轮水晶数
#             3.上场的卡牌随机攻击对方场上卡牌，如果对方场上没有卡牌，则攻击对方英雄
#             4.一方英雄死亡，游戏结束
#             5.增加疲劳机制：抽完卡牌，每个回合扣血，扣血量每个回合+1
#             6.如果敌方场上卡牌>1,手动选择攻击的卡牌
#             7.我方回合选择上场的卡牌
#             8.增加战士英雄技能，先选择卡牌是否上场，后选择是否使用英雄技能

from generate_cards import generate_cards
from fight import *
from random import randint

CARD_NUM = 30
INIT_HAND_COUNT = 3
HERO_HEALTH = 30


class Hero:
    def __init__(self, hero_class, hero_name):
        self.health = 30
        self.hero_class = hero_class
        self.hero_name = hero_name

    def health_change(self, change):
        self.health += change


class world:
    def __init__(self):
        self.mana = 1
        self.myworldcards = []
        self.enemyworldcards = []
        # self.myherohealth = HERO_HEALTH
        self.myhero = Hero('warrior', '加尔鲁什·地狱咆哮')
        # self.enemyherohealth = HERO_HEALTH
        self.enemyhero = Hero('warrior', '加尔鲁什·地狱咆哮')
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

    def use_power(self, hero):
        if hero.hero_class == 'warrior':
            hero.health += 2

    def turn_round(self):
        self.show_world()
        my_mana = self.mana
        if self.init_hand_count < CARD_NUM:
            self.myhandcards.append(self.mycards[self.init_hand_count])
            self.enemyhandcards.append(self.enemycards[self.init_hand_count])
        else:
            self.tired += 1
            print("oooooooooooooooooooooooooo本回合疲劳值为：%s" % self.tired)

        print("我方英雄血量：%s" % self.myhero.health)
        # self.myhero.health -= self.tired
        self.myhero.health_change(-self.tired)
        if self.hero_death(self.myhero.health):
            print("~~~~~~~~~~~游戏结束，你输了游戏：我方英雄疲劳死！！！~~~~~~~~~~~~~")
        else:
            my_mana = self.goto_world(self.myhandcards, my_mana)
            print("my_mana = ", my_mana)
            if my_mana >= 2:
                use = input("是否使用英雄技能（Y/N）：")
                if use == 'Y':
                    self.use_power(self.myhero)
                    my_mana -= 2

            print("$$$$我方场上卡牌$$$$$$$$$$$$$")
            for card in self.myworldcards:
                card.show()
            if len(self.myworldcards) == 0:
                print("场上没有卡牌！！！")

            self.myworldcards, self.enemyworldcards, self.enemyhero.health = self.battle(self.myworldcards,
                                                                                         self.enemyworldcards,
                                                                                         self.enemyhero.health, False)

            if self.hero_death(self.enemyhero.health):
                print("~~~~~~~~~~~~游戏结束，恭喜你获得胜利：敌方英雄被我方卡牌打死！！！~~~~~~~~~~~~")
            else:
                self.myturn = False
                print("敌方英雄血量：%s" % self.enemyhero.health)
                # self.enemyhero.health -= self.tired
                self.enemyhero.health_change(-self.tired)
                if self.hero_death(self.enemyhero.health):
                    print("~~~~~~~~~~~游戏结束，恭喜你获得胜利：敌方英雄疲劳死！！！~~~~~~~~~~~~~")
                else:
                    print("^^^^敌方手牌^^^^^^^^^^^^")
                    self.show_cards(self.enemyhandcards)
                    enemy_mana = self.mana
                    for i in range(len(self.enemyhandcards) - 1, -1, -1):
                        if self.enemyhandcards[i].mana <= enemy_mana:
                            self.enemyworldcards.append(self.enemyhandcards[i])
                            print(">>>>>>>>>>>>>>>>>>")
                            print(
                                "\t%s-%s(%s)上场！！！" % (i + 1, self.enemyhandcards[i].name, self.enemyhandcards[i].mana))
                            enemy_mana -= self.enemyhandcards[i].mana
                            del self.enemyhandcards[i]

                    if enemy_mana >= 2:
                        self.use_power(self.enemyhero)
                        enemy_mana -= 2

                    print("$$$$敌方场上卡牌$$$$$$$$$$$$$")
                    for card in self.enemyworldcards:
                        card.show()
                    if len(self.enemyworldcards) == 0:
                        print("场上没有卡牌！！！")

                    self.enemyworldcards, self.myworldcards, self.myhero.health = self.battle(self.enemyworldcards,
                                                                                              self.myworldcards,
                                                                                              self.myhero.health, True)

                    if self.hero_death(self.myhero.health):
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

    def goto_world(self, cards, mana):
        """
        选择我方卡牌上场
        :param cards: 
        :param mana: 
        :return: 
        """
        while self.enough_mana(cards, mana):
            print("^^^^我方手牌^^^^^^^^^^^^")
            self.show_cards(self.myhandcards)
            print("-----------------剩余水晶为:{0}".format(mana))
            goto_num = int(input("请选择你要上场的卡牌号码，不出牌输入0："))
            if goto_num == 0:
                break
            elif cards[goto_num - 1].mana <= mana:
                self.myworldcards.append(cards[goto_num - 1])
                print("\t%s-%s(%s)上场！！！" % (goto_num, cards[goto_num - 1].name, cards[goto_num - 1].mana))
                mana -= cards[goto_num - 1].mana
                del self.myhandcards[goto_num - 1]
        return mana

    def enough_mana(self, cards, mana):
        """
        判断是否剩余水晶足够：有卡牌的水晶小于剩余水晶
        :param cards: 
        :param mana: 
        :return: 
        """
        enough = False
        for card in cards:
            if card.mana <= mana:
                enough = True
                break
        return enough

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
                print("{0}-{1}({2}-{3})".format(i + 1, cards[i].name, cards[i].damage, cards[i].remain_health), end=' ')
            who = int(input("\n请选择你要攻击的卡牌："))
            if who < 1 or who >= len(cards) + 1:
                print("输入有误，请重新选择！！！")
                return self.attack_who(cards, auto)
            return who - 1

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
