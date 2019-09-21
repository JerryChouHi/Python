# encoding:utf-8
# @Time     : 2019/4/3 17:37
# @Author   : Jerry Chou
# @File     : main_v16.0.py
# @Function : 1.法力水晶从1开始每轮+1直到10
#             2.每轮敌我双方交替出牌，出的卡牌水晶总数不能超过本轮水晶数
#             3.上场的卡牌随机攻击对方场上卡牌，如果对方场上没有卡牌，则攻击对方英雄
#             4.一方英雄死亡，游戏结束
#             5.增加疲劳机制：抽完卡牌，每个回合扣血，扣血量每个回合+1
#             6.如果敌方场上卡牌>1,手动选择攻击的卡牌
#             7.我方回合选择上场的卡牌
#             8.增加战士英雄技能：+2甲
#               先选择卡牌是否上场，后选择是否使用英雄技能
#             9.敌方有卡牌在场时，我方卡牌先选择是否攻击敌方英雄，如果不攻击敌方英雄则选择攻击敌方在场卡牌（数量>1）
#               使用英雄技能和卡牌上场由用户选择，每个回合只能用一次英雄技能
#               优化循环判断层次比较多的代码
#             10.解决异常输入导致的报错
#                增加投降功能
#                增加猎人英雄技能：敌方英雄-2血（优先减甲）
#                攻击力为0的卡牌不进行攻击
#                增加卡牌池，开场获得不重复的卡牌进入牌库
#             11.卡牌上场第一回合睡眠，下个回合可以战斗
#                场上有7个卡牌，手牌无法上场
#                抽牌时如果手牌有10张，抽的牌被摧毁
#             12.增加术士英雄技能：抽一张牌，英雄-2血（优先减甲）
#                增加英雄出场、投降台词
#                我方英雄自由选择，敌方英雄随机
#             13.增加牧师英雄技能：选择一个对象+2血（不超过初始血量）
#                Hero类继承Card类，整合需要选择的对象集合
#                增加护甲功能、展示护甲
#                卡牌攻击，优先减甲，无甲减血
#             14.增加法师英雄技能：选择一个对象-1血（优先减甲）
#             15.增加盗贼英雄技能：1-2的匕首
#             16.优化电脑出牌AI：优先出与当前Mana最接近的卡牌
#                如果敌方英雄是术士，优化抽牌逻辑：疲劳阶段和满手牌时不抽牌
#                增加德鲁伊英雄技能：1攻1甲，只有本回合可以攻击
#                Hero类区分：英雄攻击力、武器攻击力，总攻击力=英雄攻击力+武器攻击力（每次使用英雄技能和战斗后刷新）
#                如果敌方英雄是牧师：英雄技能优先己方受伤单位，否则不使用
#                如果敌方英雄是法师：英雄技能优先敌方1血单位，否则随机敌方单位
#                单位可以不选择不攻击

from generate_cards import generate_cards
from fight import *
from random import randint
from card import Card

CARD_NUM = 30
INIT_HAND_COUNT = 3
HERO_HEALTH = 30
HANDCARDNUM = 10
WORLDCARDNUM = 7


class Hero(Card):
    def __init__(self, hero):
        Card.__init__(self, hero[1], '', '', 0, 30, 0, True)
        self.hero_class = hero[0]
        self.say_hi = hero[2]
        self.surrender = hero[3]
        self.use_skill = False
        self.tired = 0
        self.cardcount = 0
        self.weapon_durability = 0
        self.weapon_damage = 0
        self.hero_damage = 0

    def health_change(self, change):
        self.remain_health += change


def show_cards(cards):
    for i, card in enumerate(cards):
        print("\t%s-%s(%s)" % (i + 1, card.name, card.mana))


def attack(attack_card, be_attacked_card, i, enemy_id):
    """
    攻击
    :param attack_card: 
    :param be_attacked_card: 
    :param i: 
    :param enemy_id: 
    :return: 
    """
    print("%s%s-%s attack %s%s-%s" % (
        attack_card[i].name, attack_card[i].damage,
        attack_card[i].remain_health,
        be_attacked_card[enemy_id].name, be_attacked_card[enemy_id].damage,
        be_attacked_card[enemy_id].remain_health))
    attack_card[i].attack(be_attacked_card[enemy_id])
    attack_card[i].show()
    be_attacked_card[enemy_id].show()
    if not attack_card[i].alive:
        del attack_card[i]
    if not be_attacked_card[enemy_id].alive:
        del be_attacked_card[enemy_id]
    return attack_card, be_attacked_card


def input_int(desc):
    while True:
        try:
            user_input = int(input(desc))
            return user_input
        except:
            print('您输入的内容不规范，请重新输入！')


def enough_mana(cards, mana):
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


def hero_death(hero):
    """
    英雄是否死亡
    :param hero: 
    :return: 
    """
    if hero <= 0:
        return True


def choose_object_num(object_list, desc):
    object_num = input_int(desc)
    if object_num < 0 or object_num > len(object_list):
        print("输入数字超出范围，请重新输入！")
        return choose_object_num(object_list, desc)
    else:
        return object_num


class World:
    def __init__(self):
        self.mana = 1
        self.myworldcards = []
        self.enemyworldcards = []
        hero_list = [('warlock', '古尔丹', '我会夺取你的灵魂！', '这次是你赢了！'),
                     ('warrior', '加尔鲁什·地狱咆哮', '不胜利，毋宁死！', '我选择死亡！'),
                     ('hunter', '雷克萨', '狩猎开始了！', '打得好，我认输！'),
                     ('pastor', '安度因·乌瑞恩', '圣光会赐予我胜利！', '你击败了我！'),
                     ('mage', '吉安娜·普鲁德摩尔', '这可是你自找的！', '你赢了！'),
                     ('roguer', '瓦莉拉·萨古纳尔', '当心你的背后！', '我输了！'),
                     ('druid', '玛法里奥·怒风', '我是大自然的守护者！', '我承认，你赢了！'),
                     ('knight', '乌瑟尔·光明骑士', '荣耀将赐予我力量！', '胜利属于你！'),
                     ('shaman', '萨尔', '为了毁灭之锤！', '这局你赢了朋友！')
                     ]
        for i in range(len(hero_list)):
            print("{0}-{1} ".format(i + 1, hero_list[i][1]), end='')
        print('')
        choose_num = choose_object_num(hero_list, "请选择英雄序号：")
        self.myhero = Hero(hero_list[choose_num - 1])
        enemyhero_num = randint(0, len(hero_list)) - 1
        self.enemyhero = Hero(hero_list[enemyhero_num])
        self.myhero.cardcount = INIT_HAND_COUNT
        print("**************我的卡牌**************")
        self.mycards = generate_cards(CARD_NUM)
        show_cards(self.mycards)
        self.myhandcards = self.mycards[:self.myhero.cardcount]
        print("**************敌方卡牌**************")
        self.enemycards = generate_cards(CARD_NUM)
        show_cards(self.enemycards)
        self.enemyhero.cardcount = INIT_HAND_COUNT
        self.enemyhandcards = self.enemycards[:self.enemyhero.cardcount]
        self.round = 1
        self.myturn = True

    def say_hi(self):
        print('+++++++++++++++++开场+++++++++++++++++++++')
        print('我方英雄 {0}:{1}'.format(self.myhero.name, self.myhero.say_hi))
        print('敌方英雄 {0}:{1}'.format(self.enemyhero.name, self.enemyhero.say_hi))

    def turn_round(self):

        self.myhero.use_skill = False
        self.update_world_card()
        self.show_world()
        self.draw_card()

        if hero_death(self.myhero.remain_health):
            print("~~~~~~~~~~~游戏结束，你输了游戏：我方英雄疲劳死！！！~~~~~~~~~~~~~")
        else:
            surrender = input(">>>>>>>>>>>>>>是否投降(Y/N)？")
            if surrender == 'Y' or surrender == 'y':
                print("~~~~~~~~~~~{0}~~~~~~~~~~~~~".format(self.myhero.surrender))
            else:
                self.use_mana_action(self.mana)
                self.update_damage()
                self.update_world()
                self.show_world_cards(False)
                self.battle()
                self.update_damage()
                if hero_death(self.enemyhero.remain_health):
                    print("~~~~~~~~~~~~游戏结束，恭喜你获得胜利：敌方英雄被我方打死！！！~~~~~~~~~~~~")
                elif hero_death(self.myhero.remain_health):
                    print("~~~~~~~~~~~~游戏结束，你输了游戏：我方英雄爆炸！！！~~~~~~~~~~~~")
                else:
                    self.update_world()
                    self.myturn = False
                    self.update_world_card()
                    self.draw_card()

                    if hero_death(self.enemyhero.remain_health):
                        print("~~~~~~~~~~~游戏结束，恭喜你获得胜利：敌方英雄疲劳死！！！~~~~~~~~~~~~~")
                    else:
                        self.use_mana_action(self.mana)
                        self.update_damage()
                        self.update_world()
                        self.show_world_cards(False)
                        self.battle()
                        self.update_damage()
                        if hero_death(self.myhero.remain_health):
                            print("~~~~~~~~~~~游戏结束，你输了游戏：我方英雄被敌方打死！！！~~~~~~~~~~~~~")
                        elif hero_death(self.enemyhero.remain_health):
                            print("~~~~~~~~~~~~游戏结束，恭喜你获得胜利：敌方英雄爆炸！！！~~~~~~~~~~~~")
                        else:
                            self.update_world()

                            self.round += 1

                            # 水晶达到10后不再增加
                            if self.mana < 10:
                                self.mana += 1

                            self.myturn = True

                            self.turn_round()

    def update_world(self):
        """
        删除血量<=0的卡牌
        :return: 
        """
        for card in self.myworldcards:
            if card.remain_health <= 0:
                self.myworldcards.remove(card)
        for card in self.enemyworldcards:
            if card.remain_health <= 0:
                self.enemyworldcards.remove(card)
        self.update_hero()

    def update_hero(self):
        if self.myhero.hero_class == 'druid':
            self.myhero.hero_damage = 0
        if self.myhero.hero_class == 'druid':
            self.enemyhero.hero_damage = 0

    def update_damage(self):
        self.myhero.damage = self.myhero.weapon_damage + self.myhero.hero_damage
        self.enemyhero.damage = self.enemyhero.weapon_damage + self.enemyhero.hero_damage

    def update_world_card(self):
        """
        更新英雄和卡牌睡眠状态
        :return: 
        """
        if self.myturn:
            self.myhero.sleep = False
            self.enemyhero.sleep = True
            for card in self.myworldcards:
                card.sleep = False
        else:
            self.myhero.sleep = True
            self.enemyhero.sleep = False
            for card in self.enemyworldcards:
                card.sleep = False

    def draw_card(self):
        """
        有牌抽牌，无牌加疲劳值
        :return: 
        """
        if self.myturn and self.myhero.cardcount < CARD_NUM:
            if len(self.myhandcards) < HANDCARDNUM:
                print("---------------我方抽牌---------------")
                self.mycards[self.myhero.cardcount].show()
                self.myhandcards.append(self.mycards[self.myhero.cardcount])
            else:
                print("我方手牌已满，【{0}】被摧毁！".format(self.mycards[self.myhero.cardcount].name))
            self.myhero.cardcount += 1
        elif not self.myturn and self.enemyhero.cardcount < CARD_NUM:
            if len(self.enemyhandcards) < HANDCARDNUM:
                print("---------------敌方抽牌---------------")
                self.enemycards[self.enemyhero.cardcount].show()
                self.enemyhandcards.append(self.enemycards[self.enemyhero.cardcount])
            else:
                print("敌方手牌已满，【{0}】被摧毁！".format(self.mycards[self.enemyhero.cardcount].name))
            self.enemyhero.cardcount += 1
        elif self.myturn and self.myhero.cardcount == CARD_NUM:
            self.myhero.tired += 1
            print("oooooooooooooooooooooooooo我方疲劳值为：%s" % self.myhero.tired)
            self.myhero.health_change(-self.myhero.tired)
        elif not self.myturn and self.enemyhero.cardcount == CARD_NUM:
            self.enemyhero.tired += 1
            print("oooooooooooooooooooooooooo敌方疲劳值为：%s" % self.enemyhero.tired)
            self.enemyhero.health_change(-self.enemyhero.tired)

    def skill_using(self, hero, enemy_hero=None):
        if hero.hero_class == 'warrior':
            hero.armor += 2
        elif hero.hero_class == 'hunter':
            if enemy_hero.armor > 2:
                enemy_hero.armor -= 2
            elif enemy_hero.armor <= 2:
                enemy_hero.remain_health -= (2 - enemy_hero.armor)
                enemy_hero.armor = 0
        elif hero.hero_class == 'warlock':
            self.draw_card()
            if hero.armor > 2:
                hero.armor -= 2
            elif hero.armor <= 2:
                hero.remain_health -= (2 - hero.armor)
                hero.armor = 0
        elif hero.hero_class == 'pastor':
            if self.myturn:
                world = [self.enemyhero] + self.enemyworldcards + [self.myhero] + self.myworldcards
            else:
                world = [self.enemyhero] + self.enemyworldcards
                print("==========使用技能==========")
            for i in range(len(world)):
                print("{0}-{1}({2}-{3}".format(i + 1, world[i].name, world[i].damage,
                                               world[i].remain_health), end='')
                if world[i].armor > 0:
                    print("[{0}]".format(world[i].armor), end='')
                print("/{0})".format(world[i].health), end=' ')
            print('')
            if self.myturn:
                choose_num = choose_object_num(world, "请选择加血对象序号：")
            else:
                choose_num = -1
                for i in range(len(world)):
                    if world[i].remain_health != world[i].health:
                        choose_num = i + 1
                        break
            if choose_num == -1:
                print("己方没有受伤单位！")
            else:
                if not self.myturn:
                    print(">>>>>>>目标序号：{0}".format(choose_num))
                if world[choose_num - 1].remain_health < world[choose_num - 1].health - 1:
                    world[choose_num - 1].remain_health += 2
                else:
                    world[choose_num - 1].remain_health = world[choose_num - 1].health
                print("{0}-{1}({2}-{3}/{4})".format(choose_num, world[choose_num - 1].name,
                                                    world[choose_num - 1].damage,
                                                    world[choose_num - 1].remain_health,
                                                    world[choose_num - 1].health))

        elif hero.hero_class == 'mage':
            if self.myturn:
                world = [self.enemyhero] + self.enemyworldcards + [self.myhero] + self.myworldcards
            else:
                world = [self.myhero] + self.myworldcards
                print("==========使用技能==========")
            for i in range(len(world)):
                print("{0}-{1}({2}-{3}".format(i + 1, world[i].name, world[i].damage,
                                               world[i].remain_health), end='')
                if world[i].armor > 0:
                    print("[{0}]".format(world[i].armor), end='')
                print("/{0})".format(world[i].health), end=' ')
            print('')
            if self.myturn:
                choose_num = choose_object_num(world, "请选择火焰冲击对象序号：")
            else:
                choose_num = -1
                for i in range(len(world)):
                    if world[i].remain_health == 1:
                        choose_num = i + 1
                        break
                if choose_num == -1:
                    choose_num = randint(1, len(world))
                print(">>>>>>>目标序号：{0}".format(choose_num))
            if world[choose_num - 1].armor > 0:
                world[choose_num - 1].armor -= 1
            elif world[choose_num - 1].armor == 0:
                world[choose_num - 1].remain_health -= 1
            world[choose_num - 1].update()
            world[choose_num - 1].show()
        elif hero.hero_class == 'roguer':
            hero.weapon_damage = 1
            hero.weapon_durability = 2
        elif hero.hero_class == 'druid':
            hero.hero_damage += 1
            hero.armor += 1
        else:
            print("Todo")

    def show_world(self):
        print("++++++++++++++++++当前回合：%s,当前水晶：%s" % (self.round, self.mana))
        print("{0}：{1}".format(self.enemyhero.name, self.enemyhero.remain_health), end='')
        if self.enemyhero.armor > 0:
            print("[{0}]".format(self.enemyhero.armor), end='')
        if self.enemyhero.damage > 0:
            print("({0}-{1})".format(self.enemyhero.damage, self.enemyhero.weapon_durability))
        else:
            print("")
        if len(self.enemyworldcards) > 0:
            for card in self.enemyworldcards:
                print("{0}({1}-{2}/{3})".format(card.name, card.damage, card.remain_health, card.health), end=' ')
            print('')
        else:
            print("场上无卡牌")
        print("----------------------------------")
        if len(self.myworldcards) > 0:
            for card in self.myworldcards:
                print("{0}({1}-{2}/{3})".format(card.name, card.damage, card.remain_health, card.health), end=' ')
            print('')
        else:
            print("场上无卡牌")
        print("{0}：{1}".format(self.myhero.name, self.myhero.remain_health), end='')
        if self.myhero.armor > 0:
            print("[{0}]".format(self.myhero.armor), end='')
        if self.myhero.damage > 0:
            print("({0}-{1})".format(self.myhero.damage, self.myhero.weapon_durability))
        else:
            print("")

    def show_world_cards(self, order):
        """
        显示场上卡牌
        :param order: 
        :return: 
        """
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

    def battle(self):
        if self.myturn:
            mysite = [self.myhero] + self.myworldcards
            for i in range(len(mysite) - 1, -1, -1):
                # 如果是我方英雄且攻击>0
                if i == 0 and self.myhero.damage > 0:
                    print("------------攻击----------------")
                    print("{0}({1}[{2}]-{3}".format(self.myhero.name, self.myhero.damage,
                                                    self.myhero.weapon_durability,
                                                    self.myhero.remain_health), end='')
                    if self.myhero.armor > 0:
                        print("[{0}]) 准备攻击：".format(self.myhero.armor))
                    else:
                        print(") 准备攻击：")
                    opposite = [self.enemyhero] + self.enemyworldcards
                    if len(opposite) == 1:
                        print("{0}{1}[{2}]-{3}".format(self.myhero.name, self.myhero.damage,
                                                       self.myhero.weapon_durability,
                                                       self.myhero.remain_health), end='')
                        if self.myhero.armor > 0:
                            print("[{0}]".format(self.myhero.armor), end=' ')
                        else:
                            print(end=' ')
                        print("attack {0}{1}[{2}]-{3}".format(opposite[0].name, opposite[0].damage,
                                                              opposite[0].weapon_durability,
                                                              opposite[0].remain_health), end='')
                        if opposite[0].armor > 0:
                            print("[{0}]".format(opposite[0].armor), end='')
                        print('')
                        self.myhero.attack(opposite[0])
                        if opposite[0].remain_health <= 0:
                            break
                        self.myhero.show()
                        opposite[0].show()
                    else:
                        for j in range(len(opposite)):
                            print("{0}-{1}({2}-{3}".format(j + 1, opposite[j].name, opposite[j].damage,
                                                           opposite[j].remain_health),
                                  end='')
                            if opposite[j].armor > 0:
                                print("[{0}]".format(opposite[j].armor), end='')
                            print("/{0})".format(opposite[j].health), end=' ')
                        print('')
                        choose_num = choose_object_num(opposite, "请选择攻击对象序号，不攻击输入0：")
                        if choose_num == 0:
                            break
                        self.myhero.attack(opposite[choose_num - 1])
                        if opposite[0].remain_health <= 0 or self.myhero.remain_health <= 0:
                            break
                        self.myhero.show()
                        opposite[choose_num - 1].show()
                        if not self.enemyworldcards[choose_num - 2].alive:
                            del self.enemyworldcards[choose_num - 2]
                    if self.myhero.weapon_durability > 0:
                        self.myhero.weapon_durability -= 1
                    if self.myhero.weapon_durability == 0:
                        self.myhero.weapon_damage = 0
                else:
                    if mysite[i].damage > 0 and mysite[i].sleep == False:
                        print("------------攻击----------------")
                        print("{0}({1}-{2}) 准备攻击：".format(mysite[i].name, mysite[i].damage,
                                                          mysite[i].remain_health))
                        opposite = [self.enemyhero] + self.enemyworldcards
                        if len(opposite) == 1:
                            print("{0}{1}-{2} ".format(mysite[i].name, mysite[i].damage,
                                                       mysite[i].remain_health), end='')
                            if mysite[i].armor > 0:
                                print("[{0}]".format(mysite[i].armor), end=' ')
                            print("attack {0}{1}-{2}".format(opposite[0].name, opposite[0].damage,
                                                             opposite[0].remain_health), end='')
                            if opposite[0].armor > 0:
                                print("[{0}]".format(opposite[0].armor), end='')
                            print('')
                            mysite[i].attack(opposite[0])
                            if opposite[0].remain_health <= 0:
                                break
                            mysite[i].show()
                            opposite[0].show()
                        else:
                            for j in range(len(opposite)):
                                print("{0}-{1}({2}-{3}".format(j + 1, opposite[j].name, opposite[j].damage,
                                                               opposite[j].remain_health),
                                      end='')
                                if opposite[j].armor > 0:
                                    print("[{0}]".format(opposite[j].armor), end='')
                                print("/{0})".format(opposite[j].health), end=' ')
                            print('')
                            choose_num = choose_object_num(opposite, "请选择攻击对象序号，不攻击输入0：")
                            if choose_num==0:
                                break
                            mysite[i].attack(opposite[choose_num - 1])
                            if opposite[0].remain_health <= 0:
                                break
                            mysite[i].show()
                            opposite[choose_num - 1].show()
                            if not self.myworldcards[i - 1].alive:
                                del self.myworldcards[i - 1]
                            if not self.enemyworldcards[choose_num - 2].alive:
                                del self.enemyworldcards[choose_num - 2]
        else:
            enemysite = [self.enemyhero] + self.enemyworldcards
            for i in range(len(enemysite) - 1, -1, -1):
                # 如果是敌方英雄且攻击>0
                if i == 0 and self.enemyhero.damage > 0:
                    opposite = [self.myhero] + self.myworldcards
                    print("------------攻击----------------")
                    rand_num = self.attack_who(opposite)
                    print("{0}{1}[{2}]-{3} ".format(self.enemyhero.name, self.enemyhero.damage,
                                                    self.enemyhero.weapon_durability,
                                                    self.enemyhero.remain_health), end='')
                    if self.enemyhero.armor > 0:
                        print("[{0}]".format(self.enemyhero.armor), end=' ')
                    if rand_num == 0:
                        print("attack {0}{1}[{2}]-{3}".format(opposite[rand_num].name, opposite[rand_num].damage,
                                                              opposite[rand_num].weapon_durability,
                                                              opposite[rand_num].remain_health), end='')
                    else:
                        print("attack {0}{1}-{2}".format(opposite[rand_num].name, opposite[rand_num].damage,
                                                         opposite[rand_num].remain_health), end='')
                    if opposite[rand_num].armor > 0:
                        print("[{0}]".format(opposite[rand_num].armor), end='')
                    print('')
                    if rand_num == 0:
                        self.enemyhero.attack(self.myhero)
                        self.myhero.show()
                    else:
                        self.enemyhero.attack(self.myworldcards[rand_num - 1])
                        self.myworldcards[rand_num - 1].show()
                    if self.myhero.remain_health <= 0 or self.enemyhero.remain_health <= 0:
                        break
                    self.enemyhero.show()
                    if rand_num > 0 and not self.myworldcards[rand_num - 1].alive:
                        del self.myworldcards[rand_num - 1]
                    if self.enemyhero.weapon_durability > 0:
                        self.enemyhero.weapon_durability -= 1
                    if self.enemyhero.weapon_durability == 0:
                        self.enemyhero.weapon_damage = 0
                else:
                    if enemysite[i].damage > 0 and enemysite[i].sleep == False:
                        opposite = [self.myhero] + self.myworldcards
                        print("------------攻击----------------")
                        rand_num = self.attack_who(opposite)
                        print("{0}{1}-{2} ".format(enemysite[i].name, enemysite[i].damage,
                                                   enemysite[i].remain_health), end='')
                        if enemysite[i].armor > 0:
                            print("[{0}]".format(enemysite[i].armor), end=' ')
                        print("attack {0}{1}-{2}".format(opposite[rand_num].name, opposite[rand_num].damage,
                                                         opposite[rand_num].remain_health), end='')
                        if opposite[rand_num].armor > 0:
                            print("[{0}]".format(opposite[rand_num].armor), end='')
                        print('')
                        if rand_num == 0:
                            enemysite[i].attack(self.myhero)
                            self.myhero.show()
                        else:
                            enemysite[i].attack(self.myworldcards[rand_num - 1])
                            self.myworldcards[rand_num - 1].show()
                        if self.myhero.remain_health <= 0:
                            break
                        enemysite[i].show()
                        if not self.enemyworldcards[i - 1].alive:
                            del self.enemyworldcards[i - 1]
                        if rand_num > 0 and not self.myworldcards[rand_num - 1].alive:
                            del self.myworldcards[rand_num - 1]

    def use_mana_action(self, mana):
        """
        使用英雄技能、卡牌上场
        :param mana: 
        :return: 
        """
        if self.myturn:
            while self.can_use_skill(mana) or (
                        enough_mana(self.myhandcards, mana) and len(self.myworldcards) < WORLDCARDNUM):
                print("-----------------剩余水晶为:{0}".format(mana))
                print("^^^^我方手牌^^^^^^^^^^^^")
                show_cards(self.myhandcards)
                if self.can_use_skill(mana):
                    use = input(">>>>>>>>>>>>>>是否使用英雄技能(Y/N)，不再使用水晶(Q)：")
                    if use == 'Q' or use == 'q':
                        break
                    elif use == 'Y' or use == 'y':
                        self.skill_using(self.myhero, self.enemyhero)
                        mana -= 2
                        self.myhero.use_skill = True
                    elif enough_mana(self.myhandcards, mana) and len(self.myworldcards) < WORLDCARDNUM:
                        goto_num = choose_object_num(self.myhandcards, ">>>>>>>>>>>>>>请选择你要上场的卡牌号码，不再使用水晶请输入0：")
                        if goto_num == 0:
                            break
                        elif self.myhandcards[goto_num - 1].mana <= mana:
                            self.myworldcards.append(self.myhandcards[goto_num - 1])
                            print("\t%s-%s(%s)上场！！！" % (
                                goto_num, self.myhandcards[goto_num - 1].name, self.myhandcards[goto_num - 1].mana))
                            mana -= self.myhandcards[goto_num - 1].mana
                            del self.myhandcards[goto_num - 1]
                        else:
                            print("输入卡牌的水晶({0})大于剩余水晶({1})，请重新输入！".format(self.myhandcards[goto_num - 1].mana, mana))
                    elif use == 'N':
                        break

                elif enough_mana(self.myhandcards, mana) and len(self.myworldcards) < WORLDCARDNUM:
                    goto_num = choose_object_num(self.myhandcards, ">>>>>>>>>>>>>>请选择你要上场的卡牌序号，不再使用水晶请输入0：")
                    if goto_num == 0:
                        break
                    elif self.myhandcards[goto_num - 1].mana <= mana:
                        self.myworldcards.append(self.myhandcards[goto_num - 1])
                        print("\t%s-%s(%s)上场！！！" % (
                            goto_num, self.myhandcards[goto_num - 1].name, self.myhandcards[goto_num - 1].mana))
                        mana -= self.myhandcards[goto_num - 1].mana
                        del self.myhandcards[goto_num - 1]
                    else:
                        print("输入卡牌的水晶({0})大于剩余水晶({1})，请重新输入！".format(self.myhandcards[goto_num - 1].mana, mana))
        else:
            mana = self.auto_goto_world(mana)

            if mana >= 2 and self.enemyhero.tired == 0 and len(self.enemyhandcards) < 10:
                self.skill_using(self.enemyhero, self.myhero)
                mana -= 2

            if self.enemyhero.hero_class == 'warlock':
                self.auto_goto_world(mana)

    def auto_goto_world(self, mana):
        index = -1
        select = -1
        while index != -2:
            for i in range(len(self.enemyhandcards)):
                if self.enemyhandcards[i].mana <= mana:
                    select = mana - self.enemyhandcards[i].mana
                    index = i
                    break
                else:
                    index = -2
            if select > 0 and -1 < index < len(self.enemyhandcards) - 1:
                for j in range(index + 1, len(self.enemyhandcards)):
                    if self.enemyhandcards[j].mana <= mana:
                        select2 = mana - self.enemyhandcards[j].mana
                        if select > select2:
                            select = select2
                            index = j
            if len(self.enemyhandcards) == 0:
                index = -2
            if index != -2:
                print("^^^^敌方手牌^^^^^^^^^^^^")
                show_cards(self.enemyhandcards)
                self.enemyworldcards.append(self.enemyhandcards[index])
                print(">>>>>>>>>>>>>>>>>>")
                print(
                    "\t%s-%s(%s)上场！！！" % (
                        index + 1, self.enemyhandcards[index].name, self.enemyhandcards[index].mana))
                mana -= self.enemyhandcards[index].mana
                del self.enemyhandcards[index]
                index = -1
                select = -1
        return mana

    def can_use_skill(self, mana):
        """
        判断是否可以使用英雄技能
        :param mana: 
        :return: 
        """
        can_use = False
        if self.myhero.use_skill == False and mana >= 2:
            can_use = True
        return can_use

    def attack_who(self, cards):
        """
        敌方场上卡牌数量>1,我方回合手动选择攻击对象，敌方回合自动攻击
        :param cards: 
        :return: 
        """
        if len(cards) == 1:
            return 0
        elif self.myturn:
            who = input_int(">>>>>>>>>>>>>>请选择你要攻击的卡牌：")
            if who < 1 or who >= len(cards) + 1:
                print("输入有误，请重新选择！！！")
                return self.attack_who(cards)
            return who - 1
        else:
            card_id = randint(0, len(cards) - 1)
            return card_id


def main():
    game = World()
    game.say_hi()
    game.turn_round()


if __name__ == '__main__':
    main()
