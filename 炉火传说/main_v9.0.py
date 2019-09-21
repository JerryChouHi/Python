# encoding:utf-8
# @Time     : 2019/3/19 17:37
# @Author   : Jerry Chou
# @File     : main_v10.0.py
# @Function : 1.法力水晶从1开始每轮+1直到10
#             2.每轮敌我双方交替出牌，出的卡牌水晶总数不能超过本轮水晶数
#             3.上场的卡牌随机攻击对方场上卡牌，如果对方场上没有卡牌，则攻击对方英雄
#             4.一方英雄死亡，游戏结束
#             5.增加疲劳机制：抽完卡牌，每个回合扣血，扣血量每个回合+1
#             6.如果敌方场上卡牌>1,手动选择攻击的卡牌
#             7.我方回合选择上场的卡牌
#             8.增加战士英雄技能，先选择卡牌是否上场，后选择是否使用英雄技能
#             9.敌方有卡牌在场时，我方卡牌先选择是否攻击敌方英雄，如果不攻击敌方英雄则选择攻击敌方在场卡牌（>1）
#               使用英雄技能和卡牌上场由用户选择，每个回合只能用一次英雄技能
#               优化循环判断层次比较多的代码

from generate_cards import generate_cards
from fight import *
from random import randint

CARD_NUM = 10
INIT_HAND_COUNT = 3
HERO_HEALTH = 30


class Hero:
    def __init__(self, hero_class, hero_name):
        self.health = 30
        self.hero_class = hero_class
        self.hero_name = hero_name
        self.use_power = False

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

        self.myhero.use_power = False

        self.show_world()
        self.draw_card()

        if self.hero_death(self.myhero.health):
            print("~~~~~~~~~~~游戏结束，你输了游戏：我方英雄疲劳死！！！~~~~~~~~~~~~~")
        else:
            self.use_mana_action(self.mana)
            self.show_world_cards(False)
            self.myworldcards, self.enemyworldcards, self.enemyhero = self.battle(self.myworldcards,
                                                                                  self.enemyworldcards, self.enemyhero)

            if self.hero_death(self.enemyhero.health):
                print("~~~~~~~~~~~~游戏结束，恭喜你获得胜利：敌方英雄被我方卡牌打死！！！~~~~~~~~~~~~")
            else:
                self.myturn = False

                self.draw_card()

                if self.hero_death(self.enemyhero.health):
                    print("~~~~~~~~~~~游戏结束，恭喜你获得胜利：敌方英雄疲劳死！！！~~~~~~~~~~~~~")
                else:

                    self.use_mana_action(self.mana)
                    self.show_world_cards(False)
                    self.enemyworldcards, self.myworldcards, self.myhero = self.battle(self.enemyworldcards,
                                                                                       self.myworldcards, self.myhero)

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

    def draw_card(self):
        '''
        有牌抽牌，无牌加疲劳值
        :return: 
        '''
        if self.init_hand_count < CARD_NUM:
            self.myhandcards.append(self.mycards[self.init_hand_count])
            self.enemyhandcards.append(self.enemycards[self.init_hand_count])
        else:
            self.tired += 1
            print("oooooooooooooooooooooooooo本回合疲劳值为：%s" % self.tired)
        if self.myturn:
            self.myhero.health_change(-self.tired)
        else:
            self.enemyhero.health_change(-self.tired)

    def show_world(self):
        print("++++++++++++++++++当前回合：%s,当前水晶：%s" % (self.round, self.mana))

    def show_world_cards(self, order):
        '''
        显示场上卡牌
        :return: 
        '''
        if self.myturn:
            if order:
                print("$$$$敌方场上卡牌$$$$$$$$$$$$$")
                for i in range(len(self.enemyworldcards)):
                    print("{0}-{1}({2}-{3})".format(i + 1, self.enemyworldcards[i].name, self.enemyworldcards[i].damage,
                                                    self.enemyworldcards[i].remain_health), end=' ')
            else:
                print("$$$$我方场上卡牌$$$$$$$$$$$$$")
                if len(self.myworldcards) == 0:
                    print("场上没有卡牌！！！")
                else:
                    for card in self.myworldcards:
                        card.show()
        else:
            print("$$$$敌方场上卡牌$$$$$$$$$$$$$")
            if len(self.enemyworldcards) == 0:
                print("场上没有卡牌！！！")
            else:
                for card in self.enemyworldcards:
                    card.show()

    def show_cards(self, cards):
        for i, card in enumerate(cards):
            print("\t%s-%s(%s)" % (i + 1, card.name, card.mana))

    def battle(self, mycards, enemycards, enemyhero):
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
                if len(enemycards) > 0:
                    if self.myturn:
                        print("------------攻击----------------")
                        print("{0}({1}-{2}) 准备攻击：".format(mycards[i].name, mycards[i].damage,
                                                          mycards[i].remain_health))
                        print("敌方英雄血量={0}".format(enemyhero.health))
                        self.show_world_cards(True)
                        attack_hero = input("\n>>>>>>>>>>>>>>是否攻击敌方英雄(Y/N)，结束回合(Q)？")
                        if attack_hero == 'Q':
                            break
                        elif attack_hero == 'Y':
                            self.enemyhero.health_change(-self.myworldcards[i].damage)
                        else:
                            enemy_id = self.attack_who(enemycards)
                            print("%s%s-%s attack %s%s-%s" % (
                                mycards[i].name, mycards[i].damage, mycards[i].remain_health,
                                enemycards[enemy_id].name, enemycards[enemy_id].damage,
                                enemycards[enemy_id].remain_health))
                            mycards[i].attack(enemycards[enemy_id])
                            mycards[i].show()
                            enemycards[enemy_id].show()
                            if mycards[i].alive == False:
                                del mycards[i]
                            if enemycards[enemy_id].alive == False:
                                del enemycards[enemy_id]
                    else:
                        print("------------攻击----------------")
                        print("{0}({1}-{2}) 准备攻击：".format(mycards[i].name, mycards[i].damage,
                                                          mycards[i].remain_health))
                        print("敌方英雄血量={0}".format(enemyhero.health))
                        self.show_world_cards(True)
                        enemy_id = self.attack_who(enemycards)
                        print("%s%s-%s attack %s%s-%s" % (
                            mycards[i].name, mycards[i].damage, mycards[i].remain_health,
                            enemycards[enemy_id].name, enemycards[enemy_id].damage,
                            enemycards[enemy_id].remain_health))
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
                        enemyhero.health -= mycards[i].damage
                        print("%%%%%%%%%%%敌方英雄生命：", enemyhero.health)
                    else:
                        print("%s-%s攻击我方英雄" % (mycards[i].name, mycards[i].damage))
                        enemyhero.health -= mycards[i].damage
                        print("%%%%%%%%%%%我方英雄生命：", enemyhero.health)
        return mycards, enemycards, enemyhero

    def attack(self, attack_card, be_attacked_card, i, enemy_id):
        '''

        :param attack_card: 
        :param be_attacked_card: 
        :param i: 
        :param enemy_id: 
        :return: 
        '''
        print("%s%s-%s attack %s%s-%s" % (
            attack_card[i].name, attack_card[i].damage,
            attack_card[i].remain_health,
            be_attacked_card[enemy_id].name, be_attacked_card[enemy_id].damage,
            be_attacked_card[enemy_id].remain_health))
        attack_card[i].attack(be_attacked_card[enemy_id])
        attack_card[i].show()
        be_attacked_card[enemy_id].show()
        if attack_card[i].alive == False:
            del attack_card[i]
        if be_attacked_card[enemy_id].alive == False:
            del be_attacked_card[enemy_id]
        return attack_card, be_attacked_card

    def use_mana_action(self, mana):
        """
        使用英雄技能、卡牌上场
        :param cards: 
        :param mana: 
        :return: 
        """
        if self.myturn:
            while self.can_use_power(mana) or self.enough_mana(self.myhandcards, mana):
                print("^^^^我方手牌^^^^^^^^^^^^")
                self.show_cards(self.myhandcards)
                print("-----------------剩余水晶为:{0}".format(mana))
                if self.can_use_power(mana):
                    use = input(">>>>>>>>>>>>>>是否使用英雄技能(Y/N)，不再使用水晶(Q)：")
                    if use == 'Q':
                        break
                    elif use == 'Y':
                        self.use_power(self.myhero)
                        mana -= 2
                        self.myhero.use_power = True
                    elif self.enough_mana(self.myhandcards, mana):
                        goto_num = int(input(">>>>>>>>>>>>>>请选择你要上场的卡牌号码，不再使用水晶(0)："))
                        if goto_num == 0:
                            break
                        elif self.myhandcards[goto_num - 1].mana <= mana:
                            self.myworldcards.append(self.myhandcards[goto_num - 1])
                            print("\t%s-%s(%s)上场！！！" % (
                                goto_num, self.myhandcards[goto_num - 1].name, self.myhandcards[goto_num - 1].mana))
                            mana -= self.myhandcards[goto_num - 1].mana
                            del self.myhandcards[goto_num - 1]
                        else:
                            print("输入卡牌的水晶({0})大于剩余水晶({1})！".format(self.myhandcards[goto_num - 1].mana, mana))
                    elif use == 'N':
                        break

                else:
                    goto_num = int(input(">>>>>>>>>>>>>>请选择你要上场的卡牌号码，不再使用水晶(0)："))
                    if goto_num == 0:
                        break
                    elif self.myhandcards[goto_num - 1].mana <= mana:
                        self.myworldcards.append(self.myhandcards[goto_num - 1])
                        print("\t%s-%s(%s)上场！！！" % (
                            goto_num, self.myhandcards[goto_num - 1].name, self.myhandcards[goto_num - 1].mana))
                        mana -= self.myhandcards[goto_num - 1].mana
                        del self.myhandcards[goto_num - 1]
                    else:
                        print("输入卡牌的水晶({0})大于剩余水晶({1})！".format(self.myhandcards[goto_num - 1].mana, mana))
        else:
            print("^^^^敌方手牌^^^^^^^^^^^^")
            self.show_cards(self.enemyhandcards)

            for i in range(len(self.enemyhandcards) - 1, -1, -1):
                if self.enemyhandcards[i].mana <= mana:
                    self.enemyworldcards.append(self.enemyhandcards[i])
                    print(">>>>>>>>>>>>>>>>>>")
                    print(
                        "\t%s-%s(%s)上场！！！" % (i + 1, self.enemyhandcards[i].name, self.enemyhandcards[i].mana))
                    mana -= self.enemyhandcards[i].mana
                    del self.enemyhandcards[i]

            if mana >= 2:
                self.use_power(self.enemyhero)
                mana -= 2

    def can_use_power(self, mana):
        '''
        判断是否可以使用英雄技能
        :param mana: 
        :return: 
        '''
        can_use = False
        if self.myhero.use_power == False and mana >= 2:
            can_use = True
        return can_use

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

    def attack_who(self, cards):
        """
        敌方场上卡牌数量>1,我方回合手动选择攻击对象，敌方回合自动攻击
        :param cards: 
        :return: 
        """
        if len(cards) == 1:
            return 0
        elif self.myturn:
            who = int(input(">>>>>>>>>>>>>>请选择你要攻击的卡牌："))
            if who < 1 or who >= len(cards) + 1:
                print("输入有误，请重新选择！！！")
                return self.attack_who(cards)
            return who - 1
        else:
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
