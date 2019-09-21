# encoding:utf-8
# @Time     : 2019/4/11 17:37
# @Author   : Jerry Chou
# @File     : main_v20.0.py
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
#             17.增加骑士英雄技能：1-1报告兵
#                增加萨满英雄技能：随机出场，不重复
#                   0-2 治疗图腾：回合开始前己方在场卡牌群体治疗+1
#                   1-1 灼热图腾
#                   0-2 石爪图腾
#                   0-2 空气之怒图腾 Todo
#             18.卡牌属性：嘲讽Taunt--优先承受物理攻击
#             19.卡牌属性：冲锋Charge--当回合即可攻击
#                卡牌拥有多种属性
#                卡牌属性：突袭Rush--当回合只能攻击对方场上卡牌
#                卡牌属性：圣盾DivineShield--承受一次伤害破盾
#                卡牌属性：吸血BloodSucking--本方英雄恢复攻击力数值的血量
#             20.卡牌属性：剧毒Toxic--攻击的卡牌受到剧毒伤害死亡


from generate_cards import generate_cards
from fight import *
from random import randint
from card import Card
import datetime

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
        if self.hero_class == 'Shaman':
            stone_totem = Card('石爪图腾', 'totem', 'Taunt', 0, 2, 1)
            airfury_totem = Card('空气之怒图腾', 'totem', '', 0, 2, 1)
            heal_totom = Card('治疗图腾', 'totem', 'round_begin', 0, 2, 1)
            hot_totem = Card('灼热图腾', 'totem', '', 1, 1, 1)
            self.totem = [stone_totem, airfury_totem, heal_totom, hot_totem]


def show_cards(cards):
    for i, card in enumerate(cards):
        print("\t{0}-{1}({2})".format(i + 1, card.name, card.mana), end='')
        if card.property != '':
            print("[{0}]".format(card.property))
        else:
            print("")


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


def choose_attack_num(attack_list, desc):
    attack_num = input_int(desc)
    if attack_num == 0:
        return attack_num
    elif card_has_taunt(attack_list):
        if attack_list[attack_num - 1].property.find('Taunt') != -1:
            return attack_num
        else:
            print("必须攻击具有嘲讽属性的卡牌！")
            return choose_attack_num(attack_list, desc)
    else:
        if attack_num < 0 or attack_num > len(attack_list):
            print("输入数字超出范围，请重新输入！")
            return choose_attack_num(attack_list, desc)
        else:
            return attack_num


def card_has_taunt(cards):
    has_taunt = False
    for card in cards:
        if card.property.find('Taunt') != -1:
            has_taunt = True
            break
    return has_taunt


class World:
    def __init__(self):
        self.mana = 1
        self.myworldcards = []
        self.enemyworldcards = []
        hero_list = [('Warlock', '古尔丹', '我会夺取你的灵魂！', '这次是你赢了！'),
                     ('Warrior', '加尔鲁什·地狱咆哮', '不胜利，毋宁死！', '我选择死亡！'),
                     ('Hunter', '雷克萨', '狩猎开始了！', '打得好，我认输！'),
                     ('Priest', '安度因·乌瑞恩', '圣光会赐予我胜利！', '你击败了我！'),
                     ('Mage', '吉安娜·普鲁德摩尔', '这可是你自找的！', '你赢了！'),
                     ('Rogue', '瓦莉拉·萨古纳尔', '当心你的背后！', '我输了！'),
                     ('Druid', '玛法里奥·怒风', '我是大自然的守护者！', '我承认，你赢了！'),
                     ('Paladin', '乌瑟尔·光明骑士', '荣耀将赐予我力量！', '胜利属于你！'),
                     ('Shaman', '萨尔', '为了毁灭之锤！', '这局你赢了朋友！')
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

    def round_begin(self):
        if self.myturn:
            self.myhero.use_skill = False
            for card in self.myworldcards:
                if card.property == 'round_begin':
                    print("------> 回合开始触发 <------")
                    if card.name == '治疗图腾':
                        print("{0}：己方在场卡牌群体治疗+1".format(card.name))
                        for card in self.myworldcards:
                            card.add_health(1)
        else:
            self.enemyhero.use_skill = False
            for card in self.enemyworldcards:
                if card.property == 'round_begin':
                    print("------> 回合开始触发 <------")
                    if card.name == '治疗图腾':
                        print("{0}：己方在场卡牌群体治疗+1".format(card.name))
                        for card in self.enemyworldcards:
                            card.add_health(1)
        self.update_world_card()

    def turn_round(self):
        self.show_world()
        self.round_begin()
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
                self.update_hero()
                if hero_death(self.enemyhero.remain_health):
                    print("~~~~~~~~~~~~游戏结束，恭喜你获得胜利：敌方英雄被我方打死！！！~~~~~~~~~~~~")
                elif hero_death(self.myhero.remain_health):
                    print("~~~~~~~~~~~~游戏结束，你输了游戏：我方英雄爆炸！！！~~~~~~~~~~~~")
                else:
                    self.update_rush_card()
                    self.update_world()
                    self.myturn = False
                    self.round_begin()
                    self.draw_card()
                    if hero_death(self.enemyhero.remain_health):
                        print("~~~~~~~~~~~游戏结束，恭喜你获得胜利：敌方英雄疲劳死！！！~~~~~~~~~~~~~")
                    else:
                        self.use_mana_action(self.mana)
                        self.update_damage()
                        self.update_world()
                        self.show_world_cards(False)
                        self.battle()
                        self.update_hero()
                        if hero_death(self.myhero.remain_health):
                            print("~~~~~~~~~~~游戏结束，你输了游戏：我方英雄被敌方打死！！！~~~~~~~~~~~~~")
                        elif hero_death(self.enemyhero.remain_health):
                            print("~~~~~~~~~~~~游戏结束，恭喜你获得胜利：敌方英雄爆炸！！！~~~~~~~~~~~~")
                        else:
                            self.update_rush_card()
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
                if card.race == 'totem':
                    card.remain_health = card.health
                    card.alive = True
                    card.sleep = True
                    self.myhero.totem.append(card)
            if card.property.find('Charge') != -1 or card.property.find('Rush') != -1:
                card.sleep = False
        for card in self.enemyworldcards:
            if card.remain_health <= 0:
                self.enemyworldcards.remove(card)
                if card.race == 'totem':
                    card.remain_health = card.health
                    card.alive = True
                    card.sleep = True
                    self.enemyhero.totem.append(card)
            if card.property.find('Charge') != -1 or card.property.find('Rush') != -1:
                card.sleep = False

    def update_rush_card(self):
        if self.myturn:
            for card in self.myworldcards:
                if card.property.find('Rush') != -1:
                    card.isRushed = True
        else:
            for card in self.enemyworldcards:
                if card.property.find('Rush') != -1:
                    card.isRushed = True

    def update_hero(self):
        if self.myhero.hero_class == 'Druid':
            self.myhero.hero_damage = 0
        if self.enemyhero.hero_class == 'Druid':
            self.enemyhero.hero_damage = 0
        self.update_damage()

    def update_damage(self):
        self.myhero.damage = self.myhero.weapon_damage + self.myhero.hero_damage
        self.enemyhero.damage = self.enemyhero.weapon_damage + self.enemyhero.hero_damage

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
            self.myhero.reduce_health(self.myhero.tired)
        elif not self.myturn and self.enemyhero.cardcount == CARD_NUM:
            self.enemyhero.tired += 1
            print("oooooooooooooooooooooooooo敌方疲劳值为：%s" % self.enemyhero.tired)
            self.enemyhero.reduce_health(self.enemyhero.tired)

    def skill_using(self, hero, enemy_hero=None):
        is_use = True
        if hero.hero_class == 'Warrior':
            hero.armor += 2
            print("英雄技能：全副武装")
        elif hero.hero_class == 'Hunter':
            if enemy_hero.armor > 2:
                enemy_hero.armor -= 2
            elif enemy_hero.armor <= 2:
                enemy_hero.remain_health -= (2 - enemy_hero.armor)
                enemy_hero.armor = 0
            print("英雄技能：稳固射击")
        elif hero.hero_class == 'Warlock':
            self.draw_card()
            if hero.armor > 2:
                hero.armor -= 2
            elif hero.armor <= 2:
                hero.remain_health -= (2 - hero.armor)
                hero.armor = 0
            print("英雄技能：生命分流")
        elif hero.hero_class == 'Priest':
            if self.myturn:
                world = [self.enemyhero] + self.enemyworldcards + [self.myhero] + self.myworldcards
            else:
                world = [self.enemyhero] + self.enemyworldcards
            for i in range(len(world)):
                print("{0}-{1}({2}-{3}".format(i + 1, world[i].name, world[i].damage,
                                               world[i].remain_health), end='')
                if world[i].armor > 0:
                    print("[{0}]".format(world[i].armor), end='')
                print("/{0})".format(world[i].health), end='')
                if world[i].property != '':
                    print("[{0}]".format(world[i].property), end=' ')
                else:
                    print(end=' ')
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
                is_use = False
            else:
                if not self.myturn:
                    print(">>>>>>>目标序号：{0}".format(choose_num))
                world[choose_num - 1].add_health(2)
                print("英雄技能：次级治疗术->{0}".format(world[choose_num - 1].name))
                print("{0}-{1}({2}-{3}/{4})".format(choose_num, world[choose_num - 1].name,
                                                    world[choose_num - 1].damage,
                                                    world[choose_num - 1].remain_health,
                                                    world[choose_num - 1].health))
        elif hero.hero_class == 'Mage':
            if self.myturn:
                world = [self.enemyhero] + self.enemyworldcards + [self.myhero] + self.myworldcards
            else:
                world = [self.myhero] + self.myworldcards
            for i in range(len(world)):
                print("{0}-{1}({2}-{3}".format(i + 1, world[i].name, world[i].damage,
                                               world[i].remain_health), end='')
                if world[i].armor > 0:
                    print("[{0}]".format(world[i].armor), end='')
                print("/{0})".format(world[i].health), end='')
                if world[i].property != '':
                    print("[{0}]".format(world[i].property), end=' ')
                else:
                    print(end=' ')
            print('')
            if self.myturn:
                choose_num = choose_object_num(world, "请选择火焰冲击对象序号：")
            else:
                choose_num = -1
                for i in range(len(world)):
                    if world[i].remain_health == 1 and world[i].property.find('DivineShield') != -1:
                        choose_num = i + 1
                        break
                if choose_num == -1:
                    choose_num = randint(1, len(world))
                print(">>>>>>>目标序号：{0}".format(choose_num))
            if world[choose_num - 1].property.find('DivineShield') != -1:
                world[choose_num - 1].property = world[choose_num - 1].property.replace('DivineShield', '').strip()
            else:
                world[choose_num - 1].reduce_health(1)
            print("英雄技能：火焰冲击->{0}".format(world[choose_num - 1].name))
            world[choose_num - 1].show()
        elif hero.hero_class == 'Rogue':
            hero.weapon_damage = 1
            hero.weapon_durability = 2
            print("英雄技能：匕首精通")
        elif hero.hero_class == 'Druid':
            hero.hero_damage += 1
            hero.armor += 1
            print("英雄技能：变形")
        elif hero.hero_class == 'Paladin':
            soldier = Card('白银新兵', '', '', 1, 1, 1)
            if self.myturn:
                if len(self.myworldcards) < 7:
                    print("英雄技能：援军")
                    self.myworldcards.append(soldier)
                else:
                    is_use = False
            if not self.myturn:
                if len(self.enemyworldcards) < 7:
                    print("英雄技能：援军")
                    self.enemyworldcards.append(soldier)
                else:
                    is_use = False
        elif hero.hero_class == 'Shaman':
            if self.myturn:
                if len(self.myworldcards) < 7 and len(self.myhero.totem) > 0:
                    random_index = randint(0, len(self.myhero.totem) - 1)
                    self.myworldcards.append(self.myhero.totem[random_index])
                    print("英雄技能：{0}".format(self.myhero.totem[random_index].name))
                    self.myhero.totem.remove(self.myhero.totem[random_index])
                else:
                    is_use = False
            if not self.myturn:
                if len(self.enemyworldcards) < 7 and len(self.enemyhero.totem) > 0:
                    random_index = randint(0, len(self.enemyhero.totem) - 1)
                    self.enemyworldcards.append(self.enemyhero.totem[random_index])
                    print("英雄技能：{0}".format(self.enemyhero.totem[random_index].name))
                    self.enemyhero.totem.remove(self.enemyhero.totem[random_index])
                else:
                    is_use = False
        return is_use

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
                print("{0}({1}-{2}/{3})".format(card.name, card.damage, card.remain_health, card.health), end='')
                if card.property != '':
                    print("[{0}]".format(card.property), end=' ')
                else:
                    print(end=' ')
            print('')
        else:
            print("场上无卡牌")
        print("----------------------------------")
        if len(self.myworldcards) > 0:
            for card in self.myworldcards:
                print("{0}({1}-{2}/{3})".format(card.name, card.damage, card.remain_health, card.health), end='')
                if card.property != '':
                    print("[{0}]".format(card.property), end=' ')
                else:
                    print(end=' ')
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
                                                    self.enemyworldcards[i].remain_health), end='')
                    if self.enemyworldcards[i].property != '':
                        print("[{0}]".format(self.enemyworldcards[i].property), end=' ')
                    else:
                        print(end=' ')
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
                    for j in range(len(opposite)):
                        print("{0}-{1}({2}-{3}".format(j + 1, opposite[j].name, opposite[j].damage,
                                                       opposite[j].remain_health),
                              end='')
                        if opposite[j].armor > 0:
                            print("[{0}]".format(opposite[j].armor), end='')
                        print("/{0})".format(opposite[j].health), end='')
                        if opposite[j].property != '':
                            print("[{0}]".format(opposite[j].property), end=' ')
                        else:
                            print(end=' ')
                    print('')
                    attack_num = choose_attack_num(opposite, "请选择攻击对象序号，不攻击输入0：")
                    if attack_num == 0:
                        continue
                    self.myhero.attack(opposite[attack_num - 1], self.myhero, self.enemyhero)
                    if self.enemyhero.remain_health <= 0 or self.myhero.remain_health <= 0:
                        break
                    self.myhero.show()
                    opposite[attack_num - 1].show()
                    if attack_num > 1:
                        if not self.enemyworldcards[attack_num - 2].alive:
                            if self.enemyworldcards[attack_num - 2].race == 'totem':
                                self.enemyworldcards[attack_num - 2].remain_health = self.enemyworldcards[
                                    attack_num - 2].health
                                self.enemyworldcards[attack_num - 2].alive = True
                                self.enemyworldcards[attack_num - 2].sleep = True
                                self.enemyhero.totem.append(self.enemyworldcards[attack_num - 2])
                            del self.enemyworldcards[attack_num - 2]
                    if self.myhero.weapon_durability > 0:
                        self.myhero.weapon_durability -= 1
                    if self.myhero.weapon_durability == 0:
                        self.myhero.weapon_damage = 0
                else:
                    if mysite[i].damage > 0 and mysite[i].sleep == False:
                        if mysite[i].property.find('Rush') != -1 and not mysite[i].isRushed:
                            if len(self.enemyworldcards) > 0:
                                opposite = self.enemyworldcards
                            else:
                                continue
                        else:
                            opposite = [self.enemyhero] + self.enemyworldcards
                        print("------------攻击----------------")
                        print("{0}({1}-{2})".format(mysite[i].name, mysite[i].damage,
                                                    mysite[i].remain_health), end='')
                        if mysite[i].property != '':
                            print("[{0}] 准备攻击：".format(mysite[i].property))
                        else:
                            print(" 准备攻击：")
                        for j in range(len(opposite)):
                            print("{0}-{1}({2}-{3}".format(j + 1, opposite[j].name, opposite[j].damage,
                                                           opposite[j].remain_health),
                                  end='')
                            if opposite[j].armor > 0:
                                print("[{0}]".format(opposite[j].armor), end='')
                            print("/{0})".format(opposite[j].health), end='')
                            if opposite[j].property != '':
                                print("[{0}]".format(opposite[j].property), end=' ')
                            else:
                                print(end=' ')
                        print('')
                        attack_num = choose_attack_num(opposite, "请选择攻击对象序号，不攻击输入0：")
                        if attack_num == 0:
                            continue
                        mysite[i].attack(opposite[attack_num - 1], self.myhero, self.enemyhero)
                        if self.enemyhero.remain_health <= 0:
                            break
                        mysite[i].show()
                        opposite[attack_num - 1].show()
                        if not self.myworldcards[i - 1].alive:
                            if self.myworldcards[i - 1].race == 'totem':
                                self.myworldcards[i - 1].remain_health = self.myworldcards[i - 1].health
                                self.myworldcards[i - 1].alive = True
                                self.myworldcards[i - 1].sleep = True
                                self.myhero.totem.append(self.myworldcards[i - 1])
                            del self.myworldcards[i - 1]
                        if mysite[i].property.find('Rush') != -1 and not mysite[i].isRushed:
                            if not self.enemyworldcards[attack_num - 1].alive:
                                if self.enemyworldcards[attack_num - 1].race == 'totem':
                                    self.enemyworldcards[attack_num - 1].remain_health = self.enemyworldcards[
                                        attack_num - 1].health
                                    self.enemyworldcards[attack_num - 1].alive = True
                                    self.enemyworldcards[attack_num - 1].sleep = True
                                    self.enemyhero.totem.append(self.enemyworldcards[attack_num - 1])
                                del self.enemyworldcards[attack_num - 1]
                        else:
                            if attack_num > 1 and not self.enemyworldcards[attack_num - 2].alive:
                                if self.enemyworldcards[attack_num - 2].race == 'totem':
                                    self.enemyworldcards[attack_num - 2].remain_health = self.enemyworldcards[
                                        attack_num - 2].health
                                    self.enemyworldcards[attack_num - 2].alive = True
                                    self.enemyworldcards[attack_num - 2].sleep = True
                                    self.enemyhero.totem.append(self.enemyworldcards[attack_num - 2])
                                del self.enemyworldcards[attack_num - 2]
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
                        self.enemyhero.attack(self.myworldcards[rand_num - 1], self.enemyhero, self.myhero)
                        self.myworldcards[rand_num - 1].show()
                    if self.myhero.remain_health <= 0 or self.enemyhero.remain_health <= 0:
                        break
                    self.enemyhero.show()
                    if rand_num > 0 and not self.myworldcards[rand_num - 1].alive:
                        if self.myworldcards[rand_num - 1].race == 'totem':
                            self.myworldcards[rand_num - 1].remain_health = self.myworldcards[rand_num - 1].health
                            self.myworldcards[rand_num - 1].alive = True
                            self.myworldcards[rand_num - 1].sleep = True
                            self.myhero.totem.append(self.myworldcards[rand_num - 1])
                        del self.myworldcards[rand_num - 1]
                    if self.enemyhero.weapon_durability > 0:
                        self.enemyhero.weapon_durability -= 1
                    if self.enemyhero.weapon_durability == 0:
                        self.enemyhero.weapon_damage = 0
                else:
                    if enemysite[i].damage > 0 and enemysite[i].sleep == False:
                        if enemysite[i].property.find('Rush') != -1 and not enemysite[i].isRushed:
                            if len(self.myworldcards) > 0:
                                opposite = self.myworldcards
                            else:
                                continue
                        else:
                            opposite = [self.myhero] + self.myworldcards
                        print("------------攻击----------------")
                        rand_num = self.attack_who(opposite)
                        print("{0}{1}-{2} ".format(enemysite[i].name, enemysite[i].damage,
                                                   enemysite[i].remain_health), end='')
                        if enemysite[i].armor > 0:
                            print("[{0}]".format(enemysite[i].armor), end='')
                        if enemysite[i].property != '':
                            print("[{0}]".format(enemysite[i].property), end='')
                        else:
                            print(end='')
                        print(" attack {0}{1}-{2}".format(opposite[rand_num].name, opposite[rand_num].damage,
                                                          opposite[rand_num].remain_health), end='')
                        if opposite[rand_num].armor > 0:
                            print("[{0}]".format(opposite[rand_num].armor), end='')
                        if opposite[rand_num].property != '':
                            print("[{0}]".format(opposite[rand_num].property))
                        else:
                            print('')
                        if enemysite[i].property.find('Rush') != -1 and not enemysite[i].isRushed:
                            enemysite[i].attack(self.myworldcards[rand_num], self.enemyhero, self.myhero)
                            self.myworldcards[rand_num].show()
                        else:
                            if rand_num == 0:
                                enemysite[i].attack(self.myhero,self.enemyhero)
                                self.myhero.show()
                            else:
                                enemysite[i].attack(self.myworldcards[rand_num - 1], self.enemyhero, self.myhero)
                                self.myworldcards[rand_num-1].show()
                        if self.myhero.remain_health <= 0:
                            break
                        enemysite[i].show()
                        if not self.enemyworldcards[i - 1].alive:
                            if self.enemyworldcards[i - 1].race == 'totem':
                                self.enemyworldcards[i - 1].remain_health = self.enemyworldcards[i - 1].health
                                self.enemyworldcards[i - 1].alive = True
                                self.enemyworldcards[i - 1].sleep = True
                                self.enemyhero.totem.append(self.enemyworldcards[i - 1])
                            del self.enemyworldcards[i - 1]
                        if enemysite[i].property.find('Rush') != -1 and not enemysite[i].isRushed:
                            if not self.myworldcards[rand_num].alive:
                                if self.myworldcards[rand_num].race == 'totem':
                                    self.myworldcards[rand_num].remain_health = self.myworldcards[rand_num].health
                                    self.myworldcards[rand_num].alive = True
                                    self.myworldcards[rand_num].sleep = True
                                    self.myhero.totem.append(self.myworldcards[rand_num])
                                del self.myworldcards[rand_num]
                        else:
                            if rand_num > 0 and not self.myworldcards[rand_num - 1].alive:
                                if self.myworldcards[rand_num - 1].race == 'totem':
                                    self.myworldcards[rand_num - 1].remain_health = self.myworldcards[
                                        rand_num - 1].health
                                    self.myworldcards[rand_num - 1].alive = True
                                    self.myworldcards[rand_num - 1].sleep = True
                                    self.myhero.totem.append(self.myworldcards[rand_num - 1])
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
                        if self.skill_using(self.myhero, self.enemyhero):
                            mana -= 2
                            self.myhero.use_skill = True
                    elif use == 'N':
                        break
                if enough_mana(self.myhandcards, mana) and len(self.myworldcards) < WORLDCARDNUM:
                    goto_num = choose_object_num(self.myhandcards, ">>>>>>>>>>>>>>请选择你要上场的卡牌号码，不再使用水晶请输入0：")
                    if goto_num == 0:
                        break
                    elif self.myhandcards[goto_num - 1].mana <= mana:
                        self.myworldcards.append(self.myhandcards[goto_num - 1])
                        print("\t%s-%s(%s)" % (
                            goto_num, self.myhandcards[goto_num - 1].name, self.myhandcards[goto_num - 1].mana),
                              end='')
                        if self.myhandcards[goto_num - 1].property != '':
                            print("[{0}]".format(self.myhandcards[goto_num - 1].property), end='')
                        print("上场！！！")
                        mana -= self.myhandcards[goto_num - 1].mana
                        del self.myhandcards[goto_num - 1]
                    else:
                        print("输入卡牌的水晶({0})大于剩余水晶({1})，请重新输入！".format(self.myhandcards[goto_num - 1].mana, mana))
        else:
            mana = self.auto_goto_world(mana)

            if mana >= 2 and self.enemyhero.tired == 0 and len(self.enemyhandcards) < 10:
                if self.skill_using(self.enemyhero, self.myhero):
                    mana -= 2

            if self.enemyhero.hero_class == 'Warlock':
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
                    "\t%s-%s(%s)" % (
                        index + 1, self.enemyhandcards[index].name, self.enemyhandcards[index].mana), end='')
                if self.enemyhandcards[index].property != '':
                    print("[{0}]".format(self.enemyhandcards[index].property), end='')
                print("上场！！！")
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
            if card_has_taunt(cards):
                if cards[card_id].property.find('Taunt') != -1:
                    return card_id
                else:
                    return self.attack_who(cards)
            else:
                return card_id


def main():
    game = World()
    game.say_hi()
    game.turn_round()


if __name__ == '__main__':
    main()
