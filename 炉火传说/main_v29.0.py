# encoding:utf-8
# @Time     : 2019/4/30 17:37
# @Author   : Jerry Chou
# @File     : main_v29.0.py
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
#             20.卡牌属性：剧毒Toxic--被攻击的卡牌受到剧毒伤害则死亡
#             21.卡牌属性：潜行Stealth--潜行状态下，不会受到普通攻击、指向性技能；潜行卡牌攻击后状态消失
#             22.叫嚣的中士：战吼Battlecry--本回合中，使一个随从获得+2攻击力
#             23.火羽精灵：战吼Battlecry--将一个1/2的元素牌置入你的手牌
#                增加卡牌的级别，一套卡牌构筑：同一张橙卡最多1张，其他级别卡牌最多2张
#             24.穆克拉：战吼Battlecry--使你的对手获得两个香蕉
#                卡牌属性：魔免--无法成为法术或者英雄技能的目标
#             25.石丘防御者：战吼Battlecry--发现一张具有嘲讽的随从牌
#                火车王里诺艾：战吼Battlecry--为你的对手召唤两只1/1的雏龙
#             26.王牌猎人：战吼Battlecry--消灭一个攻击力大于或者等于7的随从
#                狂奔的科多兽：战吼Battlecry--随机消灭一个攻击力小于等于2的敌方随从
#             27.黑骑士：战吼Battlecry--消灭一个具有嘲讽的敌方随从
#                龙骨卫士：战吼Battlecry--如果你的手牌中有龙牌，便获得+1攻击力和嘲讽
#                始生幼龙：战吼Battlecry--对所有其他随从造成2点伤害
#                阿莱克斯塔萨:战吼Battlecry--将一个英雄的剩余生命值变为15点
#                欧克哈特大师:战吼Battlecry--招募攻击力为1、2、3的随从各一个
#                死亡之翼：战吼Battlecry--消灭所有其他随从，并弃掉你的手牌
#             28.游荡恶鬼：战吼Battlecry--摧毁双方手牌中和牌库中所有法力值消耗为1点的法术牌
#                腐烂的苹果树：亡语Deathrattle--为你的英雄恢复4点生命值
#                火花钻机：亡语Deathrattle--将两个1/1并具有突袭的“火花”置入你的手牌
#                紫色岩虫：亡语Deathrattle--召唤7只1/1的肉虫
#             29.机械克苏恩：亡语Deathrattle--如果你的牌库、手牌和战场没有任何牌，消灭敌方英雄
#                夺灵者哈卡：亡语Deathrattle--将一张“堕落之血”分别洗入双方玩家的牌库
#                随从上场可以选择位置



from generate_cards import generate_cards
from parse import parse_card
from fight import *
from random import randint
import random
from card import Card

CARD_NUM = 30
INIT_HAND_COUNT = 3
HERO_HEALTH = 30
HANDCARDNUM = 10
WORLDCARDNUM = 7

Taunt_Followers = []
f = open('card_pool.txt', 'r', encoding='UTF-8')
cards_line = f.readlines()
for card_line in cards_line:
    card = parse_card(card_line)
    if card.property.find('Taunt') != -1:
        Taunt_Followers.append(card)


class Hero(Card):
    def __init__(self, hero):
        Card.__init__(self, '', hero[1], '', '', 0, 30, 0, '', 'Hero')
        self.hero_class = hero[0]
        self.say_hi = hero[2]
        self.surrender = hero[3]
        self.use_skill = False
        self.tired = 0
        self.weapon_durability = 0
        self.weapon_damage = 0
        self.hero_damage = 0
        if self.hero_class == 'Shaman':
            stone_totem = Card('', '石爪图腾', 'totem', 'Taunt', 0, 2, 1, '', 'Follower')
            airfury_totem = Card('', '空气之怒图腾', 'totem', '', 0, 2, 1, '', 'Follower')
            heal_totom = Card('', '治疗图腾', 'totem', 'round_begin', 0, 2, 1, '', 'Follower')
            hot_totem = Card('', '灼热图腾', 'totem', '', 1, 1, 1, '', 'Follower')
            self.totem = [stone_totem, airfury_totem, heal_totom, hot_totem]


def show_cards(cards):
    for i, card in enumerate(cards):
        print("\t{0}-{1}({2})".format(i + 1, card.name, card.mana), end='')
        if card.property != '':
            print("[{0}]".format(card.property))
        else:
            print("")


def input_int(desc):
    while True:
        try:
            user_input = int(input(desc))
            return user_input
        except:
            print('您输入的内容不规范，请重新输入！')


def choose_direct_num(direct_list, desc):
    """
    选择指向性目标
    :param direct_list: 
    :param desc: 
    :return: 
    """
    direct_num = input_int(desc)
    if direct_num == 0:
        return direct_num
    if direct_num < 0 or direct_num > len(direct_list):
        print("输入数字超出范围，请重新输入！")
        return choose_direct_num(direct_list, desc)
    if card_has_AntiMagic(direct_list):
        if direct_list[direct_num - 1].property.find('AntiMagic') != -1:
            print("魔免的卡牌无法被选中！")
            return choose_direct_num(direct_list, desc)
    return direct_num


def choose_object_num(object_list, desc):
    """
    选择目标
    :param object_list: 
    :param desc: 
    :return: 
    """
    object_num = input_int(desc)
    if object_num < 0 or object_num > len(object_list):
        print("输入数字超出范围，请重新输入！")
        return choose_object_num(object_list, desc)
    else:
        return object_num


def DamageEqualList(card_list, damage):
    """
    找到攻击力为damage的卡牌
    :param card_list: 
    :param damage: 
    :return: 
    """
    equal_list = []
    for card in card_list:
        if card.present_damage == damage:
            equal_list.append(card)
    return equal_list


def choose_attack_num(attack_list, desc):
    """
    选择物理攻击目标
    :param attack_list: 
    :param desc: 
    :return: 
    """
    attack_num = input_int(desc)
    if attack_num == 0:
        return attack_num
    elif attack_num < 0 or attack_num > len(attack_list):
        print("输入数字超出范围，请重新输入！")
        return choose_attack_num(attack_list, desc)
    if card_has_taunt(attack_list):
        if attack_list[attack_num - 1].property.find('Taunt') == -1:
            print("必须攻击具有嘲讽属性的卡牌！")
            return choose_attack_num(attack_list, desc)
    if card_has_stealth(attack_list):
        if attack_list[attack_num - 1].property.find('Stealth') != -1:
            print("潜行的卡牌无法被攻击！")
            return choose_attack_num(attack_list, desc)
    return attack_num


def card_has_taunt(cards):
    """
    是否有嘲讽随从
    :param cards: 
    :return: 
    """
    has_taunt = False
    for card in cards:
        if card.property.find('Taunt') != -1:
            has_taunt = True
            break
    return has_taunt


def card_has_dragon(cards):
    """
    是否有龙牌
    :param cards: 
    :return: 
    """
    has_dragon = False
    for card in cards:
        if card.race.find('Dragon') != -1:
            has_dragon = True
            break
    return has_dragon


def card_has_stealth(cards):
    """
    是否有潜行随从
    :param cards: 
    :return: 
    """
    has_stealth = False
    for card in cards:
        if card.property.find('Stealth') != -1:
            has_stealth = True
            break
    return has_stealth


def card_has_AntiMagic(cards):
    """
    是否有魔免随从
    :param cards: 
    :return: 
    """
    has_AntiMagic = False
    for card in cards:
        if card.property.find('AntiMagic') != -1:
            has_AntiMagic = True
            break
    return has_AntiMagic


def CardDamage(cards, type, value):
    """
    是否存在相应攻击力的卡牌
    :param cards: 
    :param type: 1-等于 2-大于 3-小于 4-大于等于 5-小于等于
    :param value: 
    :return: 
    """
    has = False
    if type == 1:
        for card in cards:
            if card.present_damage == value:
                has = True
                break
    elif type == 2:
        for card in cards:
            if card.present_damage > value:
                has = True
                break
    elif type == 3:
        for card in cards:
            if card.present_damage < value:
                has = True
                break
    elif type == 4:
        for card in cards:
            if card.present_damage >= value:
                has = True
                break
    elif type == 5:
        for card in cards:
            if card.present_damage <= value:
                has = True
                break
    return has


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
        print("**************我的卡牌**************")
        self.mycards = generate_cards(CARD_NUM)
        show_cards(self.mycards)
        self.myhandcards = self.mycards[:INIT_HAND_COUNT]
        for i in range(INIT_HAND_COUNT):
            self.mycards.remove(self.mycards[0])
        print("**************敌方卡牌**************")
        self.enemycards = generate_cards(CARD_NUM)
        show_cards(self.enemycards)
        self.enemyhandcards = self.enemycards[:INIT_HAND_COUNT]
        for i in range(INIT_HAND_COUNT):
            self.enemycards.remove(self.enemycards[0])
        self.round = 1
        self.myturn = False

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

    def enough_mana(self, cards):
        """
        判断是否剩余水晶足够：有卡牌的水晶小于剩余水晶
        :param cards: 
        :return: 
        """
        enough = False
        for card in cards:
            if card.mana <= self.current_mana:
                enough = True
                break
        return enough

    def do_action(self):
        self.use_mana_action()
        if not self.check_game_over():
            self.update_hero_damage()
            self.update_world()
            self.show_world_cards(False)
            self.battle()
            if not self.check_game_over():
                self.update_hero()

    def before_round(self):
        self.current_mana = self.mana
        self.update_rush_card()
        self.update_cards()
        self.update_world()
        self.myturn = not self.myturn
        self.round_begin()
        self.draw_card()

    def check_game_over(self):
        game_over = False
        if self.myhero.remain_health <= 0 or not self.myhero.alive:
            print(">>>{0} 死亡".format(self.myhero.name))
            game_over = True
        if self.enemyhero.remain_health <= 0 or not self.enemyhero.alive:
            print(">>>{0} 死亡".format(self.enemyhero.name))
            game_over = True
        return game_over

    # 回合制游戏
    def turn_round(self):
        self.show_world()
        self.before_round()
        if not self.check_game_over():
            surrender = input(">>>>>>>>>>>>>>是否投降(Y/N)？")
            if surrender == 'Y' or surrender == 'y':
                print("~~~~~~~~~~~{0}~~~~~~~~~~~~~".format(self.myhero.surrender))
            else:
                self.do_action()
                if not self.check_game_over():
                    self.before_round()
                    if not self.check_game_over():
                        self.do_action()
                        if not self.check_game_over():
                            self.round += 1
                            # 水晶达到10后不再增加
                            if self.mana < 10:
                                self.mana += 1
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
        """
        更新突袭后的随从属性
        :return: 
        """
        if self.myturn:
            for card in self.myworldcards:
                if card.property.find('Rush') != -1:
                    card.isRushed = True
        else:
            for card in self.enemyworldcards:
                if card.property.find('Rush') != -1:
                    card.isRushed = True

    def update_cards(self):
        """
        更新当回合的临时数据
        :return: 
        """
        if self.myturn:
            for card in self.myworldcards:
                if card.change_damage != 0:
                    card.back_to_present_damage()
        else:
            for card in self.enemyworldcards:
                if card.change_damage != 0:
                    card.back_to_present_damage()

    def update_hero(self):
        """
        更新德鲁伊的英雄伤害
        :return: 
        """
        if self.myhero.hero_class == 'Druid':
            self.myhero.hero_damage = 0
        if self.enemyhero.hero_class == 'Druid':
            self.enemyhero.hero_damage = 0
        self.update_hero_damage()

    def update_hero_damage(self):
        """
        更新英雄当前的伤害
        :return: 
        """
        self.myhero.present_damage = self.myhero.weapon_damage + self.myhero.hero_damage
        self.enemyhero.present_damage = self.enemyhero.weapon_damage + self.enemyhero.hero_damage

    def draw_card(self, BloodOfFallenNum=0):
        """
        有牌抽牌，无牌加疲劳值
        :return: 
        """
        if self.myturn:
            if len(self.mycards) > 0:
                draw_card = self.mycards[0]
                self.mycards.remove(self.mycards[0])
                # 手牌超过上限
                if len(self.myhandcards) >= HANDCARDNUM:
                    print("我方手牌已满，【{0}】被摧毁！".format(draw_card.name))
                else:
                    print("---------------我方抽牌---------------")
                    draw_card.show()
                    if draw_card.name == '堕落之血':
                        print("{0} 生命值 {1} -> ".format(self.myhero.name, self.myhero.remain_health), end='')
                        self.myhero.reduce_health(3)
                        print("{0}".format(self.myhero.remain_health))
                        BloodOfFallenNum += 1
                        self.draw_card(BloodOfFallenNum)
                    else:
                        self.myhandcards.append(draw_card)
                        while BloodOfFallenNum > 0:
                            randnum1 = randint(0, len(self.mycards))
                            self.mycards.insert(randnum1, Card('', '堕落之血', '', '', '', '', 1, '', 'Magic', False))
                            randnum2 = randint(0, len(self.mycards))
                            self.mycards.insert(randnum2, Card('', '堕落之血', '', '', '', '', 1, '', 'Magic', False))
                            BloodOfFallenNum -= 1
            else:
                self.myhero.tired += 1
                print("oooooooooooooooooooooooooo我方疲劳值为：{0}".format(self.myhero.tired))
                self.myhero.reduce_health(self.myhero.tired)
                while BloodOfFallenNum > 0:
                    randnum1 = randint(0, len(self.mycards))
                    self.mycards.insert(randnum1, Card('', '堕落之血', '', '', '', '', 1, '', 'Magic', False))
                    randnum2 = randint(0, len(self.mycards))
                    self.mycards.insert(randnum2, Card('', '堕落之血', '', '', '', '', 1, '', 'Magic', False))
                    BloodOfFallenNum -= 1
        else:
            if len(self.enemycards) > 0:
                draw_card = self.enemycards[0]
                self.enemycards.remove(self.enemycards[0])
                if len(self.enemyhandcards) >= HANDCARDNUM:
                    print("敌方手牌已满，【{0}】被摧毁！".format(draw_card.name))
                else:
                    print("---------------敌方抽牌---------------")
                    draw_card.show()
                    if draw_card.name == '堕落之血':
                        print("{0} 生命值 {1} -> ".format(self.enemyhero.name, self.enemyhero.remain_health), end='')
                        self.enemyhero.reduce_health(3)
                        print("{0}".format(self.enemyhero.remain_health))
                        BloodOfFallenNum += 1
                        self.draw_card(BloodOfFallenNum)
                    else:
                        self.enemyhandcards.append(draw_card)
                        while BloodOfFallenNum > 0:
                            randnum1 = randint(0, len(self.enemycards))
                            self.enemycards.insert(randnum1, Card('', '堕落之血', '', '', '', '', 1, '', 'Magic', False))
                            randnum2 = randint(0, len(self.enemycards))
                            self.enemycards.insert(randnum2, Card('', '堕落之血', '', '', '', '', 1, '', 'Magic', False))
                            BloodOfFallenNum -= 1
            else:
                self.enemyhero.tired += 1
                print("oooooooooooooooooooooooooo敌方疲劳值为：{0}".format(self.enemyhero.tired))
                self.enemyhero.reduce_health(self.enemyhero.tired)
                while BloodOfFallenNum > 0:
                    randnum1 = randint(0, len(self.enemycards))
                    self.enemycards.insert(randnum1, Card('', '堕落之血', '', '', '', '', 1, '', 'Magic', False))
                    randnum2 = randint(0, len(self.enemycards))
                    self.enemycards.insert(randnum2, Card('', '堕落之血', '', '', '', '', 1, '', 'Magic', False))
                    BloodOfFallenNum -= 1

    def skill_using(self, myhero, oppohero, myworldcards, oppoworldcards, myhandcards, oppohandcards):
        """
        使用技能
        :param myhero: 
        :param oppohero: 
        :param myworldcards: 
        :param oppoworldcards: 
        :param myhandcards: 
        :param oppohandcards: 
        :return: 是否使用了技能
        """
        is_use = True
        if myhero.hero_class == 'Warrior':
            myhero.armor += 2
            print("英雄技能：全副武装")
        elif myhero.hero_class == 'Hunter':
            oppohero.reduce_health(2)
            print("英雄技能：稳固射击")
        elif myhero.hero_class == 'Warlock':
            print("英雄技能：生命分流")
            self.draw_card()
            myhero.reduce_health(2)
        elif myhero.hero_class == 'Priest':
            if self.myturn:
                world = [self.enemyhero]
                for card in self.enemyworldcards:
                    if card.property.find('Stealth') == -1:
                        world.append(card)
                world += [self.myhero] + self.myworldcards
            else:
                world = [self.enemyhero]
                for card in self.enemyworldcards:
                    if card.property.find('AntiMagic') == -1:
                        world.append(card)
            for i in range(len(world)):
                print("{0}-{1}({2}-{3}".format(i + 1, world[i].name, world[i].present_damage,
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
                choose_num = choose_direct_num(world, "请选择加血对象序号：")
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
                                                    world[choose_num - 1].present_damage,
                                                    world[choose_num - 1].remain_health,
                                                    world[choose_num - 1].health))
        elif myhero.hero_class == 'Mage':
            if self.myturn:
                world = [self.enemyhero]
                for card in self.enemyworldcards:
                    if card.property.find('AntiMagic') == -1 and card.property.find('Stealth') == -1:
                        world.append(card)
                world += [self.myhero] + self.myworldcards
            else:
                world = [self.myhero]
                for card in self.myworldcards:
                    if card.property.find('AntiMagic') == -1 and card.property.find('Stealth') == -1:
                        world.append(card)
            for i in range(len(world)):
                print("{0}-{1}({2}-{3}".format(i + 1, world[i].name, world[i].present_damage,
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
                choose_num = choose_direct_num(world, "请选择火焰冲击对象序号：")
            else:
                choose_num = -1
                for i in range(len(world)):
                    if world[i].remain_health == 1:
                        choose_num = i + 1
                        break
                if choose_num == -1:
                    choose_num = randint(1, len(world))
                print(">>>>>>>目标序号：{0}".format(choose_num))
            world[choose_num - 1].reduce_health(1)
            print("英雄技能：火焰冲击->{0}".format(world[choose_num - 1].name))
            world[choose_num - 1].show()
            if world[choose_num - 1] in self.enemyworldcards:
                if not world[choose_num - 1].alive and world[choose_num - 1].property.find('Deathrattle') != -1:
                    self.death_rattle(world[choose_num - 1], self.enemyhero, self.myhero, self.enemyworldcards,
                                      self.myworldcards, self.enemyhandcards, self.myhandcards, self.enemycards,
                                      self.mycards)
            else:
                if not world[choose_num - 1].alive and world[choose_num - 1].property.find('Deathrattle') != -1:
                    self.death_rattle(world[choose_num - 1], self.myhero, self.enemyhero, self.myworldcards,
                                      self.enemyworldcards, self.myhandcards, self.enemyhandcards, self.mycards,
                                      self.enemycards)
        elif myhero.hero_class == 'Rogue':
            myhero.weapon_damage = 1
            myhero.weapon_durability = 2
            print("英雄技能：匕首精通")
        elif myhero.hero_class == 'Druid':
            myhero.hero_damage += 1
            myhero.armor += 1
            print("英雄技能：变形")
        elif myhero.hero_class == 'Paladin':
            soldier = Card('', '白银新兵', '', '', 1, 1, 1, '', 'Follower')
            if self.myturn:
                if len(self.myworldcards) < WORLDCARDNUM:
                    print("英雄技能：援军")
                    self.myworldcards.append(soldier)
                else:
                    is_use = False
                    print("场上随从已满，无法使用技能！")
            if not self.myturn:
                if len(self.enemyworldcards) < WORLDCARDNUM:
                    print("英雄技能：援军")
                    self.enemyworldcards.append(soldier)
                else:
                    is_use = False
                    print("场上随从已满，无法使用技能！")
        elif myhero.hero_class == 'Shaman':
            if self.myturn:
                if len(self.myworldcards) < WORLDCARDNUM and len(self.myhero.totem) > 0:
                    random_index = randint(0, len(self.myhero.totem) - 1)
                    self.myworldcards.append(self.myhero.totem[random_index])
                    print("英雄技能：{0}".format(self.myhero.totem[random_index].name))
                    self.myhero.totem.remove(self.myhero.totem[random_index])
                else:
                    is_use = False
                    print("场上随从已满或基础图腾已满！")
            if not self.myturn:
                if len(self.enemyworldcards) < WORLDCARDNUM and len(self.enemyhero.totem) > 0:
                    random_index = randint(0, len(self.enemyhero.totem) - 1)
                    self.enemyworldcards.append(self.enemyhero.totem[random_index])
                    print("英雄技能：{0}".format(self.enemyhero.totem[random_index].name))
                    self.enemyhero.totem.remove(self.enemyhero.totem[random_index])
                else:
                    is_use = False
                    print("场上随从已满或基础图腾已满！")
        return is_use

    def show_world(self):
        """
        显示棋局信息
        :return: 
        """
        print("++++++++++++++++++当前回合：{0},当前水晶：{1}".format(self.round, self.mana))
        print("{0}：{1}".format(self.enemyhero.name, self.enemyhero.remain_health), end='')
        if self.enemyhero.armor > 0:
            print("[{0}]".format(self.enemyhero.armor), end='')
        if self.enemyhero.present_damage > 0:
            print("({0}-{1})".format(self.enemyhero.present_damage, self.enemyhero.weapon_durability), end='')
        print(" 剩余卡牌：{0}".format(len(self.enemycards)))
        if len(self.enemyworldcards) > 0:
            for card in self.enemyworldcards:
                print(
                    "{0}({1}-{2}/{3})".format(card.name, card.present_damage, card.remain_health, card.present_health),
                    end='')
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
                print(
                    "{0}({1}-{2}/{3})".format(card.name, card.present_damage, card.remain_health, card.present_health),
                    end='')
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
        if self.myhero.present_damage > 0:
            print("({0}-{1})".format(self.myhero.present_damage, self.myhero.weapon_durability), end='')
        print(" 剩余卡牌：{0}".format(len(self.mycards)))

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
        """
        对战
        :return: 
        """
        if self.myturn:
            mysite = [self.myhero] + self.myworldcards
            for i in range(len(mysite) - 1, -1, -1):
                # 如果是我方英雄且攻击>0
                if i == 0 and self.myhero.present_damage > 0:
                    print("------------攻击----------------")
                    print("{0}({1}[{2}]-{3}".format(self.myhero.name, self.myhero.present_damage,
                                                    self.myhero.weapon_durability,
                                                    self.myhero.remain_health), end='')
                    if self.myhero.armor > 0:
                        print("[{0}]) 准备攻击：".format(self.myhero.armor))
                    else:
                        print(") 准备攻击：")
                    opposite = [self.enemyhero] + self.enemyworldcards
                    for j in range(len(opposite)):
                        print("{0}-{1}({2}-{3}".format(j + 1, opposite[j].name, opposite[j].present_damage,
                                                       opposite[j].remain_health),
                              end='')
                        if opposite[j].armor > 0:
                            print("[{0}]".format(opposite[j].armor), end='')
                        print("/{0})".format(opposite[j].present_health), end='')
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
                                    attack_num - 2].present_health
                                self.enemyworldcards[attack_num - 2].alive = True
                                self.enemyworldcards[attack_num - 2].sleep = True
                                self.enemyhero.totem.append(self.enemyworldcards[attack_num - 2])
                            if self.enemyworldcards[attack_num - 2].property.find('Deathrattle') != -1:
                                self.death_rattle(self.enemyworldcards[attack_num - 2], self.enemyhero, self.myhero,
                                                  self.enemyworldcards, self.myworldcards, self.enemyhandcards,
                                                  self.myhandcards, self.enemycards, self.mycards)
                            else:
                                self.enemyworldcards.remove(self.enemyworldcards[attack_num - 2])
                    if self.myhero.weapon_durability > 0:
                        self.myhero.weapon_durability -= 1
                    if self.myhero.weapon_durability == 0:
                        self.myhero.weapon_damage = 0
                else:
                    if mysite[i].present_damage > 0 and mysite[i].sleep == False:
                        if mysite[i].property.find('Rush') != -1 and not mysite[i].isRushed:
                            if len(self.enemyworldcards) > 0:
                                opposite = self.enemyworldcards
                            else:
                                continue
                        else:
                            opposite = [self.enemyhero] + self.enemyworldcards
                        print("------------攻击----------------")
                        print("{0}({1}-{2})".format(mysite[i].name, mysite[i].present_damage,
                                                    mysite[i].remain_health), end='')
                        if mysite[i].property != '':
                            print("[{0}] 准备攻击：".format(mysite[i].property))
                        else:
                            print(" 准备攻击：")
                        for j in range(len(opposite)):
                            print("{0}-{1}({2}-{3}".format(j + 1, opposite[j].name, opposite[j].present_damage,
                                                           opposite[j].remain_health),
                                  end='')
                            if opposite[j].armor > 0:
                                print("[{0}]".format(opposite[j].armor), end='')
                            print("/{0})".format(opposite[j].present_health), end='')
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
                                self.myworldcards[i - 1].remain_health = self.myworldcards[i - 1].present_health
                                self.myworldcards[i - 1].alive = True
                                self.myworldcards[i - 1].sleep = True
                                self.myhero.totem.append(self.myworldcards[i - 1])
                            if self.myworldcards[i - 1].property.find('Deathrattle') != -1:
                                self.death_rattle(self.myworldcards[i - 1], self.myhero, self.enemyhero,
                                                  self.myworldcards, self.enemyworldcards, self.myhandcards,
                                                  self.enemyhandcards, self.mycards, self.enemycards)
                            else:
                                self.myworldcards.remove(self.myworldcards[i - 1])
                        if mysite[i].property.find('Rush') != -1 and not mysite[i].isRushed:
                            if not self.enemyworldcards[attack_num - 1].alive:
                                if self.enemyworldcards[attack_num - 1].race == 'totem':
                                    self.enemyworldcards[attack_num - 1].remain_health = self.enemyworldcards[
                                        attack_num - 1].present_health
                                    self.enemyworldcards[attack_num - 1].alive = True
                                    self.enemyworldcards[attack_num - 1].sleep = True
                                    self.enemyhero.totem.append(self.enemyworldcards[attack_num - 1])
                                if self.enemyworldcards[attack_num - 1].property.find('Deathrattle') != -1:
                                    self.death_rattle(self.enemyworldcards[attack_num - 1], self.enemyhero, self.myhero,
                                                      self.enemyworldcards, self.myworldcards, self.enemyhandcards,
                                                      self.myhandcards, self.enemycards, self.mycards)
                                else:
                                    self.enemyworldcards.remove(self.enemyworldcards[attack_num - 1])
                        else:
                            if attack_num > 1 and not self.enemyworldcards[attack_num - 2].alive:
                                if self.enemyworldcards[attack_num - 2].race == 'totem':
                                    self.enemyworldcards[attack_num - 2].remain_health = self.enemyworldcards[
                                        attack_num - 2].present_health
                                    self.enemyworldcards[attack_num - 2].alive = True
                                    self.enemyworldcards[attack_num - 2].sleep = True
                                    self.enemyhero.totem.append(self.enemyworldcards[attack_num - 2])
                                if self.enemyworldcards[attack_num - 2].property.find('Deathrattle') != -1:
                                    self.death_rattle(self.enemyworldcards[attack_num - 2], self.enemyhero, self.myhero,
                                                      self.enemyworldcards, self.myworldcards, self.enemyhandcards,
                                                      self.myhandcards, self.enemycards, self.mycards)
                                else:
                                    self.enemyworldcards.remove(self.enemyworldcards[attack_num - 2])
        else:
            enemysite = [self.enemyhero] + self.enemyworldcards
            for i in range(len(enemysite) - 1, -1, -1):
                # 如果是敌方英雄且攻击>0
                if i == 0 and self.enemyhero.present_damage > 0:
                    opposite = [self.myhero] + self.myworldcards
                    print("------------攻击----------------")
                    rand_num = self.attack_who(opposite)
                    print("{0}{1}[{2}]-{3} ".format(self.enemyhero.name, self.enemyhero.present_damage,
                                                    self.enemyhero.weapon_durability,
                                                    self.enemyhero.remain_health), end='')
                    if self.enemyhero.armor > 0:
                        print("[{0}]".format(self.enemyhero.armor), end=' ')
                    if rand_num == 0:
                        print(
                            "attack {0}{1}[{2}]-{3}".format(opposite[rand_num].name, opposite[rand_num].present_damage,
                                                            opposite[rand_num].weapon_durability,
                                                            opposite[rand_num].remain_health), end='')
                    else:
                        print("attack {0}{1}-{2}".format(opposite[rand_num].name, opposite[rand_num].present_damage,
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
                            self.myworldcards[rand_num - 1].remain_health = self.myworldcards[
                                rand_num - 1].present_health
                            self.myworldcards[rand_num - 1].alive = True
                            self.myworldcards[rand_num - 1].sleep = True
                            self.myhero.totem.append(self.myworldcards[rand_num - 1])
                        if self.myworldcards[rand_num - 1].property.find('Deathrattle') != -1:
                            self.death_rattle(self.myworldcards[rand_num - 1], self.myhero, self.enemyhero,
                                              self.myworldcards, self.enemyworldcards, self.myhandcards,
                                              self.enemyhandcards, self.mycards, self.enemycards)
                        else:
                            self.myworldcards.remove(self.myworldcards[rand_num - 1])
                    if self.enemyhero.weapon_durability > 0:
                        self.enemyhero.weapon_durability -= 1
                    if self.enemyhero.weapon_durability == 0:
                        self.enemyhero.weapon_damage = 0
                else:
                    if enemysite[i].present_damage > 0 and enemysite[i].sleep == False:
                        if enemysite[i].property.find('Rush') != -1 and not enemysite[i].isRushed:
                            if len(self.myworldcards) > 0:
                                opposite = self.myworldcards
                            else:
                                continue
                        else:
                            opposite = [self.myhero] + self.myworldcards
                        print("------------攻击----------------")
                        rand_num = self.attack_who(opposite)
                        print("{0}{1}-{2} ".format(enemysite[i].name, enemysite[i].present_damage,
                                                   enemysite[i].remain_health), end='')
                        if enemysite[i].armor > 0:
                            print("[{0}]".format(enemysite[i].armor), end='')
                        if enemysite[i].property != '':
                            print("[{0}]".format(enemysite[i].property), end='')
                        else:
                            print(end='')
                        print(" attack {0}{1}-{2}".format(opposite[rand_num].name, opposite[rand_num].present_damage,
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
                                enemysite[i].attack(self.myhero, self.enemyhero)
                                self.myhero.show()
                            else:
                                enemysite[i].attack(self.myworldcards[rand_num - 1], self.enemyhero, self.myhero)
                                self.myworldcards[rand_num - 1].show()
                        if self.myhero.remain_health <= 0:
                            break
                        enemysite[i].show()
                        if not self.enemyworldcards[i - 1].alive:
                            if self.enemyworldcards[i - 1].race == 'totem':
                                self.enemyworldcards[i - 1].remain_health = self.enemyworldcards[i - 1].present_health
                                self.enemyworldcards[i - 1].alive = True
                                self.enemyworldcards[i - 1].sleep = True
                                self.enemyhero.totem.append(self.enemyworldcards[i - 1])
                            if self.enemyworldcards[i - 1].property.find('Deathrattle') != -1:
                                self.death_rattle(self.enemyworldcards[i - 1], self.enemyhero, self.myhero,
                                                  self.enemyworldcards, self.myworldcards, self.enemyhandcards,
                                                  self.myhandcards, self.enemycards, self.mycards)
                            else:
                                self.enemyworldcards.remove(self.enemyworldcards[i - 1])
                        if enemysite[i].property.find('Rush') != -1 and not enemysite[i].isRushed:
                            if not self.myworldcards[rand_num].alive:
                                if self.myworldcards[rand_num].race == 'totem':
                                    self.myworldcards[rand_num].remain_health = self.myworldcards[
                                        rand_num].present_health
                                    self.myworldcards[rand_num].alive = True
                                    self.myworldcards[rand_num].sleep = True
                                    self.myhero.totem.append(self.myworldcards[rand_num])
                                if self.myworldcards[rand_num].property.find('Deathrattle') != -1:
                                    self.death_rattle(self.myworldcards[rand_num], self.myhero, self.enemyhero,
                                                      self.myworldcards, self.enemyworldcards, self.myhandcards,
                                                      self.enemyhandcards, self.mycards, self.enemycards)
                                else:
                                    self.myworldcards.remove(self.myworldcards[rand_num])
                        else:
                            if rand_num > 0 and not self.myworldcards[rand_num - 1].alive:
                                if self.myworldcards[rand_num - 1].race == 'totem':
                                    self.myworldcards[rand_num - 1].remain_health = self.myworldcards[
                                        rand_num - 1].present_health
                                    self.myworldcards[rand_num - 1].alive = True
                                    self.myworldcards[rand_num - 1].sleep = True
                                    self.myhero.totem.append(self.myworldcards[rand_num - 1])
                                if self.myworldcards[rand_num - 1].property.find('Deathrattle') != -1:
                                    self.death_rattle(self.myworldcards[rand_num - 1], self.myhero, self.enemyhero,
                                                      self.myworldcards, self.enemyworldcards, self.myhandcards,
                                                      self.enemyhandcards, self.mycards, self.enemycards)
                                else:
                                    self.myworldcards.remove(self.myworldcards[rand_num - 1])

    def death_rattle(self, card, myhero, oppohero, myworldcards, oppoworldcards, myhandcards, oppohandcards,
                     mylibrarycards, oppolibrarycards):
        """
        亡语
        :param card: 
        :param myhero: 
        :param oppohero: 
        :param myworldcards: 
        :param oppoworldcards: 
        :param myhandcards: 
        :param oppohandcards: 
        :return: 
        """
        myworldcards.remove(card)
        if card.name == '腐烂的苹果树':
            print("{0} 血量：{1} -> ".format(myhero.name, myhero.remain_health), end='')
            myhero.add_health(4)
            print("{0}".format(myhero.remain_health))
        elif card.name == '火花钻机':
            if len(myhandcards) < HANDCARDNUM - 1:
                myhandcards.append(Card('', '火花', 'Element', 'Rush', 1, 1, 1, '', 'Follower'))
                myhandcards.append(Card('', '火花', 'Element', 'Rush', 1, 1, 1, '', 'Follower'))
            elif len(myhandcards) == HANDCARDNUM - 1:
                myhandcards.append(Card('', '火花', 'Element', 'Rush', 1, 1, 1, '', 'Follower'))
        elif card.name == '紫色岩虫':
            while len(myworldcards) < WORLDCARDNUM:
                myworldcards.append(Card('', '肉虫', 'Beast', '', 1, 1, 1, '', 'Follower'))
        elif card.name == '机械克苏恩':
            if len(myworldcards) == 0 and len(myhandcards) == 0 and len(mylibrarycards) == 0:
                oppohero.alive = False
        elif card.name == '夺灵者哈卡':
            myrandnum = randint(0, len(mylibrarycards) - 1)
            mylibrarycards.insert(myrandnum, Card('', '堕落之血', '', '', '', '', 1, '', 'Magic', False))
            opporandnum = randint(0, len(oppolibrarycards) - 1)
            oppolibrarycards.insert(opporandnum, Card('', '堕落之血', '', '', '', '', 1, '', 'Magic', False))

    def battle_cry(self, card, myhero, oppohero, myworldcards, oppoworldcards, myhandcards, oppohandcards,
                   mylibrarycards, oppolibrarycards):
        """
        战吼
        :param card: 
        :param myhero: 
        :param oppohero: 
        :param myworldcards: 
        :param oppoworldcards: 
        :param myhandcards: 
        :param oppohandcards: 
        :return: 
        """
        if card.name == '叫嚣的中士':
            world = []
            for worldcard in myworldcards:
                world.append(worldcard)
            if self.myturn:
                for worldcard in oppoworldcards:
                    if worldcard.property.find('Stealth') == -1:
                        world.append(worldcard)
            if len(world) == 0:
                pass
            else:
                for i in range(len(world)):
                    print("{0}-{1}({2}-{3}".format(i + 1, world[i].name, world[i].present_damage,
                                                   world[i].remain_health), end='')
                    if world[i].armor > 0:
                        print("[{0}]".format(world[i].armor), end='')
                    print("/{0})".format(world[i].present_health), end='')
                    if world[i].property != '':
                        print("[{0}]".format(world[i].property), end=' ')
                    else:
                        print(end=' ')
                print('')
                if self.myturn:
                    choose_num = choose_object_num(world, "请选择要+2攻的对象序号：")
                else:
                    choose_num = randint(1, len(world))
                print("{0}的攻击力{1}->".format(world[choose_num - 1].name, world[choose_num - 1].present_damage),
                      end='')
                world[choose_num - 1].change_damage = 2
                world[choose_num - 1].update_present_damage()
                print("{0}".format(world[choose_num - 1].present_damage))
            if self.myturn:
                if len(self.myworldcards) == 0:
                    self.myworldcards.append(card)
                else:
                    for index, worldcard in enumerate(self.myworldcards):
                        print(" <<{0}>> {1}".format(index + 1, worldcard.name), end='')
                    print(" <<{0}>>".format(len(self.myworldcards) + 1))
                    choose_num = choose_object_num(self.myworldcards, "请选择卡牌要上场位置的序号：")
                    self.myworldcards.insert(choose_num - 1, card)
            else:
                self.enemyworldcards.append(card)
            print(">>>>>>{0}({1})".format(card.name, card.mana), end='')
            if card.property != '':
                print("[{0}]".format(card.property), end='')
            print("上场！！！")
        elif card.name == '火羽精灵':
            if self.myturn:
                if len(self.myworldcards) == 0:
                    self.myworldcards.append(card)
                else:
                    for index, worldcard in enumerate(self.myworldcards):
                        print(" <<{0}>> {1}".format(index + 1, worldcard.name), end='')
                    print(" <<{0}>>".format(len(self.myworldcards) + 1))
                    choose_num = choose_object_num(self.myworldcards, "请选择卡牌要上场位置的序号：")
                    self.myworldcards.insert(choose_num - 1, card)
            else:
                self.enemyworldcards.append(card)
            print(">>>>>>{0}({1})".format(card.name, card.mana), end='')
            if card.property != '':
                print("[{0}]".format(card.property), end='')
            print("上场！！！")
            if len(myhandcards) < HANDCARDNUM:
                myhandcards.append(Card('', '烈焰元素', 'Element', '', 1, 2, 1, '', 'Follower'))
        elif card.name == '穆克拉':
            if self.myturn:
                if len(self.myworldcards) == 0:
                    self.myworldcards.append(card)
                else:
                    for index, worldcard in enumerate(self.myworldcards):
                        print(" <<{0}>> {1}".format(index + 1, worldcard.name), end='')
                    print(" <<{0}>>".format(len(self.myworldcards) + 1))
                    choose_num = choose_object_num(self.myworldcards, "请选择卡牌要上场位置的序号：")
                    self.myworldcards.insert(choose_num - 1, card)
            else:
                self.enemyworldcards.append(card)
            print(">>>>>>{0}({1})".format(card.name, card.mana), end='')
            if card.property != '':
                print("[{0}]".format(card.property), end='')
            print("上场！！！")
            banana = Card('', '香蕉', '', '', '', '', 1, '', 'Magic', True)
            if len(oppohandcards) < HANDCARDNUM - 1:
                oppohandcards.append(banana)
                oppohandcards.append(banana)
            elif len(oppohandcards) == HANDCARDNUM - 1:
                oppohandcards.append(banana)
        elif card.name == '石丘防御者':
            if self.myturn:
                if len(self.myworldcards) == 0:
                    self.myworldcards.append(card)
                else:
                    for index, worldcard in enumerate(self.myworldcards):
                        print(" <<{0}>> {1}".format(index + 1, worldcard.name), end='')
                    print(" <<{0}>>".format(len(self.myworldcards) + 1))
                    choose_num = choose_object_num(self.myworldcards, "请选择卡牌要上场位置的序号：")
                    self.myworldcards.insert(choose_num - 1, card)
            else:
                self.enemyworldcards.append(card)
            print(">>>>>>{0}({1})".format(card.name, card.mana), end='')
            if card.property != '':
                print("[{0}]".format(card.property), end='')
            print("上场！！！")
            choose_followers = random.sample(Taunt_Followers, 3)
            for i in range(len(choose_followers)):
                print("{0}-{1}({2}-{3}".format(i + 1, choose_followers[i].name, choose_followers[i].present_damage,
                                               choose_followers[i].remain_health), end='')
                if choose_followers[i].armor > 0:
                    print("[{0}]".format(choose_followers[i].armor), end='')
                print("/{0})".format(choose_followers[i].present_health), end='')
                if choose_followers[i].property != '':
                    print("[{0}]".format(choose_followers[i].property), end=' ')
                else:
                    print(end=' ')
            print('')
            if self.myturn:
                choose_num = choose_object_num(choose_followers, "请选择要发现的对象序号：")
            else:
                choose_num = randint(1, len(choose_followers))
            print("{0} 发现 {1}".format(card.name, choose_followers[choose_num - 1].name))
            if len(myhandcards) < HANDCARDNUM:
                myhandcards.append(choose_followers[choose_num - 1])
        elif card.name == '火车王里诺艾':
            if self.myturn:
                if len(self.myworldcards) == 0:
                    self.myworldcards.append(card)
                else:
                    for index, worldcard in enumerate(self.myworldcards):
                        print(" <<{0}>> {1}".format(index + 1, worldcard.name), end='')
                    print(" <<{0}>>".format(len(self.myworldcards) + 1))
                    choose_num = choose_object_num(self.myworldcards, "请选择卡牌要上场位置的序号：")
                    self.myworldcards.insert(choose_num - 1, card)
            else:
                self.enemyworldcards.append(card)
            print(">>>>>>{0}({1})".format(card.name, card.mana), end='')
            if card.property != '':
                print("[{0}]".format(card.property), end='')
            print("上场！！！")
            if len(oppoworldcards) < WORLDCARDNUM - 1:
                oppoworldcards.append(Card('', '雏龙', 'Dragon', '', 1, 1, 1, '', 'Follower'))
                oppoworldcards.append(Card('', '雏龙', 'Dragon', '', 1, 1, 1, '', 'Follower'))
            elif len(oppoworldcards) == WORLDCARDNUM - 1:
                oppoworldcards.append(Card('', '雏龙', 'Dragon', '', 1, 1, 1, '', 'Follower'))
        elif card.name == '王牌猎人':
            if self.myturn:
                if len(self.myworldcards) == 0:
                    self.myworldcards.append(card)
                else:
                    for index, worldcard in enumerate(self.myworldcards):
                        print(" <<{0}>> {1}".format(index + 1, worldcard.name), end='')
                    print(" <<{0}>>".format(len(self.myworldcards) + 1))
                    choose_num = choose_object_num(self.myworldcards, "请选择卡牌要上场位置的序号：")
                    self.myworldcards.insert(choose_num - 1, card)
            else:
                self.enemyworldcards.append(card)
            print(">>>>>>{0}({1})".format(card.name, card.mana), end='')
            if card.property != '':
                print("[{0}]".format(card.property), end='')
            print("上场！！！")
            if self.myturn:
                world = self.enemyworldcards
            else:
                world = self.myworldcards
            if CardDamage(world, 4, 7):
                for i in range(len(world)):
                    print("{0}-{1}({2}-{3}".format(i + 1, world[i].name, world[i].present_damage,
                                                   world[i].remain_health), end='')
                    if world[i].armor > 0:
                        print("[{0}]".format(world[i].armor), end='')
                    print("/{0})".format(world[i].present_health), end='')
                    if world[i].property != '':
                        print("[{0}]".format(world[i].property), end=' ')
                    else:
                        print(end=' ')
                print('')
                while True:
                    if self.myturn:
                        choose_num = choose_object_num(world, "请选择要消灭的对象（攻击力大于等于7）序号：")
                    else:
                        choose_num = randint(1, len(world))
                    if world[choose_num - 1].present_damage >= 7:
                        break
                print(">>>{0} 消灭了 {1}".format(card.name, world[choose_num - 1].name))
                if world[choose_num - 1].property.find('Deathrattle') != -1:
                    self.death_rattle(world[choose_num - 1], oppohero, myhero, oppoworldcards, myworldcards,
                                      oppohandcards, myhandcards, oppolibrarycards, mylibrarycards)
                else:
                    world.remove(world[choose_num - 1])
        elif card.name == '狂奔的科多兽':
            if self.myturn:
                if len(self.myworldcards) == 0:
                    self.myworldcards.append(card)
                else:
                    for index, worldcard in enumerate(self.myworldcards):
                        print(" <<{0}>> {1}".format(index + 1, worldcard.name), end='')
                    print(" <<{0}>>".format(len(self.myworldcards) + 1))
                    choose_num = choose_object_num(self.myworldcards, "请选择卡牌要上场位置的序号：")
                    self.myworldcards.insert(choose_num - 1, card)
            else:
                self.enemyworldcards.append(card)
            print(">>>>>>{0}({1})".format(card.name, card.mana), end='')
            if card.property != '':
                print("[{0}]".format(card.property), end='')
            print("上场！！！")
            if self.myturn:
                world = self.enemyworldcards
            else:
                world = self.myworldcards
            if CardDamage(world, 5, 2):
                for i in range(len(world)):
                    print("{0}-{1}({2}-{3}".format(i + 1, world[i].name, world[i].present_damage,
                                                   world[i].remain_health), end='')
                    if world[i].armor > 0:
                        print("[{0}]".format(world[i].armor), end='')
                    print("/{0})".format(world[i].present_health), end='')
                    if world[i].property != '':
                        print("[{0}]".format(world[i].property), end=' ')
                    else:
                        print(end=' ')
                print('')
                while True:
                    choose_num = randint(1, len(world))
                    if world[choose_num - 1].present_damage <= 2:
                        break
                print(">>>{0} 消灭了 {1}".format(card.name, world[choose_num - 1].name))
                if world[choose_num - 1].property.find('Deathrattle') != -1:
                    self.death_rattle(world[choose_num - 1], oppohero, myhero, oppoworldcards, myworldcards,
                                      oppohandcards, myhandcards, oppolibrarycards, mylibrarycards)
                else:
                    world.remove(world[choose_num - 1])
        elif card.name == '黑骑士':
            if self.myturn:
                if len(self.myworldcards) == 0:
                    self.myworldcards.append(card)
                else:
                    for index, worldcard in enumerate(self.myworldcards):
                        print(" <<{0}>> {1}".format(index + 1, worldcard.name), end='')
                    print(" <<{0}>>".format(len(self.myworldcards) + 1))
                    choose_num = choose_object_num(self.myworldcards, "请选择卡牌要上场位置的序号：")
                    self.myworldcards.insert(choose_num - 1, card)
            else:
                self.enemyworldcards.append(card)
            print(">>>>>>{0}({1})".format(card.name, card.mana), end='')
            if card.property != '':
                print("[{0}]".format(card.property), end='')
            print("上场！！！")
            if self.myturn:
                world = self.enemyworldcards
            else:
                world = self.myworldcards
            if card_has_taunt(world):
                for i in range(len(world)):
                    print("{0}-{1}({2}-{3}".format(i + 1, world[i].name, world[i].present_damage,
                                                   world[i].remain_health), end='')
                    if world[i].armor > 0:
                        print("[{0}]".format(world[i].armor), end='')
                    print("/{0})".format(world[i].present_health), end='')
                    if world[i].property != '':
                        print("[{0}]".format(world[i].property), end=' ')
                    else:
                        print(end=' ')
                print('')
                while True:
                    if self.myturn:
                        choose_num = choose_object_num(world, "请选择要消灭的对象（嘲讽）序号：")
                    else:
                        choose_num = randint(1, len(world))
                    if world[choose_num - 1].property.find('Taunt') != -1:
                        break
                print(">>>{0} 消灭了 {1}".format(card.name, world[choose_num - 1].name))
                if world[choose_num - 1].property.find('Deathrattle') != -1:
                    self.death_rattle(world[choose_num - 1], oppohero, myhero, oppoworldcards, myworldcards,
                                      oppohandcards, myhandcards, oppolibrarycards, mylibrarycards)
                else:
                    world.remove(world[choose_num - 1])
        elif card.name == '龙骨卫士':
            if self.myturn:
                if len(self.myworldcards) == 0:
                    self.myworldcards.append(card)
                else:
                    for index, worldcard in enumerate(self.myworldcards):
                        print(" <<{0}>> {1}".format(index + 1, worldcard.name), end='')
                    print(" <<{0}>>".format(len(self.myworldcards) + 1))
                    choose_num = choose_object_num(self.myworldcards, "请选择卡牌要上场位置的序号：")
                    self.myworldcards.insert(choose_num - 1, card)
            else:
                self.enemyworldcards.append(card)
            print(">>>>>>{0}({1})".format(card.name, card.mana), end='')
            if card.property != '':
                print("[{0}]".format(card.property), end='')
            print("上场！！！")
            if self.myturn:
                handcard = self.myhandcards
            else:
                handcard = self.enemyhandcards
            if card_has_dragon(handcard):
                card.present_damage += 1
                card.property = card.property + ' Taunt'
        elif card.name == '始生幼龙':
            for worldcard in myworldcards:
                print("{0} 血量：{1} -> ".format(worldcard.name, worldcard.remain_health), end='')
                worldcard.reduce_health(2)
                print("{0}".format(worldcard.remain_health))
                if not worldcard.alive and worldcard.property.find('Deathrattle') != -1:
                    self.death_rattle(worldcard, myhero, oppohero, myworldcards, oppoworldcards, myhandcards,
                                      oppohandcards, mylibrarycards, oppolibrarycards)
            for worldcard in oppoworldcards:
                print("{0} 血量：{1} -> ".format(worldcard.name, worldcard.remain_health), end='')
                worldcard.reduce_health(2)
                print("{0}".format(worldcard.remain_health))
                if not worldcard.alive and worldcard.property.find('Deathrattle') != -1:
                    self.death_rattle(worldcard, oppohero, myhero, oppoworldcards, myworldcards, oppohandcards,
                                      myhandcards, oppolibrarycards, mylibrarycards)
            if self.myturn:
                if len(self.myworldcards) == 0:
                    self.myworldcards.append(card)
                else:
                    for index, worldcard in enumerate(self.myworldcards):
                        print(" <<{0}>> {1}".format(index + 1, worldcard.name), end='')
                    print(" <<{0}>>".format(len(self.myworldcards) + 1))
                    choose_num = choose_object_num(self.myworldcards, "请选择卡牌要上场位置的序号：")
                    self.myworldcards.insert(choose_num - 1, card)
            else:
                self.enemyworldcards.append(card)
            print(">>>>>>{0}({1})".format(card.name, card.mana), end='')
            if card.property != '':
                print("[{0}]".format(card.property), end='')
            print("上场！！！")
        elif card.name == '阿莱克斯塔萨':
            if self.myturn:
                if len(self.myworldcards) == 0:
                    self.myworldcards.append(card)
                else:
                    for index, worldcard in enumerate(self.myworldcards):
                        print(" <<{0}>> {1}".format(index + 1, worldcard.name), end='')
                    print(" <<{0}>>".format(len(self.myworldcards) + 1))
                    choose_num = choose_object_num(self.myworldcards, "请选择卡牌要上场位置的序号：")
                    self.myworldcards.insert(choose_num - 1, card)
            else:
                self.enemyworldcards.append(card)
            print(">>>>>>{0}({1})".format(card.name, card.mana), end='')
            if card.property != '':
                print("[{0}]".format(card.property), end='')
            print("上场！！！")
            world = [self.myhero] + [self.enemyhero]
            print("1-{0}({1}-{2}".format(self.myhero.name, self.myhero.present_damage,
                                         self.myhero.remain_health), end='')
            if self.myhero.armor > 0:
                print("[{0}]".format(self.myhero.armor), end='')
            print("/{0})".format(self.myhero.present_health))
            print("2-{0}({1}-{2}".format(self.enemyhero.name, self.enemyhero.present_damage,
                                         self.enemyhero.remain_health), end='')
            if self.enemyhero.armor > 0:
                print("[{0}]".format(self.enemyhero.armor), end='')
            print("/{0})".format(self.enemyhero.present_health))
            if self.myturn:
                choose_num = choose_object_num(world, "请选择要使生命值变为15的对象的序号：")
            else:
                choose_num = randint(1, len(world))
            if choose_num == 1:
                print("{0} 血量：{1} -> ".format(self.myhero.name, self.myhero.remain_health), end='')
                self.myhero.remain_health = 15
                print("{0}".format(self.myhero.remain_health))
            else:
                print("{0} 血量：{1} -> ".format(self.enemyhero.name, self.enemyhero.remain_health), end='')
                self.enemyhero.remain_health = 15
                print("{0}".format(self.enemyhero.remain_health))
        elif card.name == '欧克哈特大师':
            if self.myturn:
                if len(self.myworldcards) == 0:
                    self.myworldcards.append(card)
                else:
                    for index, worldcard in enumerate(self.myworldcards):
                        print(" <<{0}>> {1}".format(index + 1, worldcard.name), end='')
                    print(" <<{0}>>".format(len(self.myworldcards) + 1))
                    choose_num = choose_object_num(self.myworldcards, "请选择卡牌要上场位置的序号：")
                    self.myworldcards.insert(choose_num - 1, card)
            else:
                self.enemyworldcards.append(card)
            print(">>>>>>{0}({1})".format(card.name, card.mana), end='')
            if card.property != '':
                print("[{0}]".format(card.property), end='')
            print("上场！！！")
            if self.myturn:
                DamageOne = DamageEqualList(self.mycards, 1)
                DamageTwo = DamageEqualList(self.mycards, 2)
                DamageThree = DamageEqualList(self.mycards, 3)
                if len(DamageOne) > 0 and len(self.myworldcards) < WORLDCARDNUM:
                    randnum = randint(0, len(DamageOne) - 1)
                    self.mycards.remove(DamageOne[randnum])
                    self.myworldcards.append(DamageOne[randnum])
                    print("招募>>>{0}({1})".format(DamageOne[randnum].name, DamageOne[randnum].mana), end='')
                    if DamageOne[randnum].property != '':
                        print("[{0}]".format(DamageOne[randnum].property), end='')
                    print("上场！！！")
                if len(DamageTwo) > 0 and len(self.myworldcards) < WORLDCARDNUM:
                    randnum = randint(0, len(DamageTwo) - 1)
                    self.mycards.remove(DamageTwo[randnum])
                    self.myworldcards.append(DamageTwo[randnum])
                    print("招募>>>{0}({1})".format(DamageTwo[randnum].name, DamageTwo[randnum].mana), end='')
                    if DamageTwo[randnum].property != '':
                        print("[{0}]".format(DamageTwo[randnum].property), end='')
                    print("上场！！！")
                if len(DamageThree) > 0 and len(self.myworldcards) < WORLDCARDNUM:
                    randnum = randint(0, len(DamageThree) - 1)
                    self.mycards.remove(DamageThree[randnum])
                    self.myworldcards.append(DamageThree[randnum])
                    print("招募>>>{0}({1})".format(DamageThree[randnum].name, DamageThree[randnum].mana), end='')
                    if DamageThree[randnum].property != '':
                        print("[{0}]".format(DamageThree[randnum].property), end='')
                    print("上场！！！")
            else:
                DamageOne = DamageEqualList(self.enemycards, 1)
                DamageTwo = DamageEqualList(self.enemycards, 2)
                DamageThree = DamageEqualList(self.enemycards, 3)
                if len(DamageOne) > 0 and len(self.enemyworldcards) < WORLDCARDNUM:
                    randnum = randint(0, len(DamageOne) - 1)
                    self.enemycards.remove(DamageOne[randnum])
                    self.enemyworldcards.append(DamageOne[randnum])
                    print(">>>>>>{0}({1})".format(DamageOne[randnum].name, DamageOne[randnum].mana), end='')
                    if DamageOne[randnum].property != '':
                        print("[{0}]".format(DamageOne[randnum].property), end='')
                    print("上场！！！")
                if len(DamageTwo) > 0 and len(self.enemyworldcards) < WORLDCARDNUM:
                    randnum = randint(0, len(DamageTwo) - 1)
                    self.enemycards.remove(DamageTwo[randnum])
                    self.enemyworldcards.append(DamageTwo[randnum])
                    print(">>>>>>{0}({1})".format(DamageTwo[randnum].name, DamageTwo[randnum].mana), end='')
                    if DamageTwo[randnum].property != '':
                        print("[{0}]".format(DamageTwo[randnum].property), end='')
                    print("上场！！！")
                if len(DamageThree) > 0 and len(self.enemyworldcards) < WORLDCARDNUM:
                    randnum = randint(0, len(DamageThree) - 1)
                    self.enemycards.remove(DamageThree[randnum])
                    self.enemyworldcards.append(DamageThree[randnum])
                    print(">>>>>>{0}({1})".format(DamageThree[randnum].name, DamageThree[randnum].mana), end='')
                    if DamageThree[randnum].property != '':
                        print("[{0}]".format(DamageThree[randnum].property), end='')
                    print("上场！！！")
        elif card.name == '死亡之翼':
            print("我就是力量的化身！！！")
            for worldcard in myworldcards:
                if worldcard.property.find('Deathrattle') != -1:
                    self.death_rattle(worldcard, myhero, oppohero, myworldcards, oppoworldcards, myhandcards,
                                      oppohandcards, mylibrarycards, oppolibrarycards)
            self.myworldcards.clear()
            for worldcard in oppoworldcards:
                if worldcard.property.find('Deathrattle') != -1:
                    self.death_rattle(worldcard, oppohero, myhero, oppoworldcards, myworldcards, oppohandcards,
                                      myhandcards, oppolibrarycards, mylibrarycards)
            self.enemyworldcards.clear()
            if self.myturn:
                self.myworldcards.append(card)
            else:
                self.enemyworldcards.append(card)
            print(">>>>>>{0}({1})".format(card.name, card.mana), end='')
            if card.property != '':
                print("[{0}]".format(card.property), end='')
            print("上场！！！")

            if self.myturn:
                self.myhandcards.clear()
            else:
                self.enemyhandcards.clear()
        elif card.name == '游荡恶鬼':
            if self.myturn:
                if len(self.myworldcards) == 0:
                    self.myworldcards.append(card)
                else:
                    for index, worldcard in enumerate(self.myworldcards):
                        print(" <<{0}>> {1}".format(index + 1, worldcard.name), end='')
                    print(" <<{0}>>".format(len(self.myworldcards) + 1))
                    choose_num = choose_object_num(self.myworldcards, "请选择卡牌要上场位置的序号：")
                    self.myworldcards.insert(choose_num - 1, card)
            else:
                self.enemyworldcards.append(card)
            for handcard in self.myhandcards:
                if handcard.mana == 1 and handcard.type == 'Magic':
                    self.myhandcards.remove(handcard)
            for handcard in self.enemyhandcards:
                if handcard.mana == 1 and handcard.type == 'Magic':
                    self.enemyhandcards.remove(handcard)
            for librarycard in self.mycards:
                if librarycard.mana == 1 and librarycard.type == 'Magic':
                    self.mycards.remove(librarycard)
            for librarycard in self.enemycards:
                if librarycard.mana == 1 and librarycard.type == 'Magic':
                    self.enemycards.remove(librarycard)

    def cast(self, card, myhero, oppohero, myworldcards, oppoworldcards, myhandcards, oppohandcards,
             mylibrarycards, oppolibrarycards):
        """
        释放法术
        :param card: 
        :param myhero: 
        :param oppohero: 
        :param myworldcards: 
        :param oppoworldcards: 
        :param myhandcards: 
        :param oppohandcards: 
        :return: 
        """
        if card.name == '香蕉':
            world = []
            for card in myworldcards:
                world.append(card)
            if self.myturn:
                for card in oppoworldcards:
                    if card.property.find('Stealth') == -1:
                        world.append(card)
            if len(world) == 0:
                return False
            else:
                for i in range(len(world)):
                    print("{0}-{1}({2}-{3}".format(i + 1, world[i].name, world[i].present_damage,
                                                   world[i].remain_health), end='')
                    if world[i].armor > 0:
                        print("[{0}]".format(world[i].armor), end='')
                    print("/{0})".format(world[i].present_health), end='')
                    if world[i].property != '':
                        print("[{0}]".format(world[i].property), end=' ')
                    else:
                        print(end=' ')
                print('')
                if self.myturn:
                    choose_num = choose_direct_num(world, "请选择对象序号：")
                else:
                    while True:
                        choose_num = randint(1, len(world))
                        if world[choose_num - 1].property.find('AntiMagic') == -1:
                            break
                print("{0} {1}-{2} >>> ".format(world[choose_num - 1].name, world[choose_num - 1].present_damage,
                                                world[choose_num - 1].remain_health),
                      end='')
                world[choose_num - 1].present_damage += 1
                world[choose_num - 1].remain_health += 1
                world[choose_num - 1].present_health += 1
                print("{0}-{1}".format(world[choose_num - 1].present_damage, world[choose_num - 1].remain_health))
                return True

    def use_mana_action(self):
        """
        使用英雄技能、卡牌上场
        :return: 
        """
        if self.myturn:
            while self.can_use_skill() or self.enough_mana(self.myhandcards):
                print("-----------------剩余水晶为:{0}".format(self.current_mana))
                print("^^^^我方手牌^^^^^^^^^^^^")
                show_cards(self.myhandcards)
                if self.can_use_skill():
                    use = input(">>>>>>>>>>>>>>是否使用英雄技能(Y/N)，不再使用水晶(Q)：")
                    if use == 'Q' or use == 'q':
                        break
                    elif use == 'Y' or use == 'y':
                        if self.skill_using(self.myhero, self.enemyhero, self.myworldcards, self.enemyworldcards,
                                            self.myhandcards, self.enemyhandcards):
                            self.current_mana -= 2
                            self.myhero.use_skill = True
                            print("-----------------剩余水晶为:{0}".format(self.current_mana))
                            if self.myturn:
                                show_cards(self.myhandcards)
                            else:
                                show_cards(self.enemyhandcards)
                    elif use == 'N':
                        break
                if self.enough_mana(self.myhandcards):
                    goto_num = choose_object_num(self.myhandcards, ">>>>>>>>>>>>>>请选择你要使用的卡牌号码，不再使用水晶请输入0：")
                    if goto_num == 0:
                        break
                    elif self.myhandcards[goto_num - 1].mana <= self.current_mana:
                        self.current_mana -= self.myhandcards[goto_num - 1].mana
                        if self.myhandcards[goto_num - 1].type == 'Follower':
                            if len(self.myworldcards) < WORLDCARDNUM:
                                if self.myhandcards[goto_num - 1].property.find('Battlecry') != -1:
                                    self.battle_cry(self.myhandcards[goto_num - 1], self.myhero, self.enemyhero,
                                                    self.myworldcards, self.enemyworldcards, self.myhandcards,
                                                    self.enemyhandcards, self.mycards, self.enemycards)
                                else:
                                    if len(self.myworldcards)==0:
                                        self.myworldcards.append(self.myhandcards[goto_num - 1])
                                    else:
                                        for index, worldcard in enumerate(self.myworldcards):
                                            print(" <<{0}>> {1}".format(index + 1, worldcard.name), end='')
                                        print(" <<{0}>>".format(len(self.myworldcards) + 1))
                                        choose_num = choose_object_num(self.myworldcards, "请选择卡牌要上场位置的序号：")
                                        self.myworldcards.insert(choose_num-1,self.myhandcards[goto_num - 1])
                                    print(">>>>>>{0}-{1}({2})".format(
                                        goto_num, self.myhandcards[goto_num - 1].name,
                                        self.myhandcards[goto_num - 1].mana),
                                        end='')
                                    if self.myhandcards[goto_num - 1].property != '':
                                        print("[{0}]".format(self.myhandcards[goto_num - 1].property), end='')
                                    print("上场！！！")
                            else:
                                print("场上随从已满，随从无法上场！")
                                continue
                        elif self.myhandcards[goto_num - 1].type == 'Magic':
                            if not self.cast(self.myhandcards[goto_num - 1], self.myhero, self.enemyhero,
                                             self.myworldcards, self.enemyworldcards, self.myhandcards,
                                             self.enemyhandcards, self.mycards, self.enemycards):
                                break
                        try:
                            if self.myhandcards[goto_num - 1] in self.myhandcards:
                                self.myhandcards.remove(self.myhandcards[goto_num - 1])
                        except Exception as e:
                            print(e)
                    else:
                        print("输入卡牌的水晶({0})大于剩余水晶({1})，请重新输入！".format(self.myhandcards[goto_num - 1].mana,
                                                                      self.current_mana))
        else:
            self.auto_goto_world()

            if self.current_mana >= 2 and self.enemyhero.tired == 0 and len(self.enemyhandcards) < HANDCARDNUM:
                if self.skill_using(self.enemyhero, self.myhero, self.enemyworldcards, self.myworldcards,
                                    self.enemyhandcards, self.myhandcards):
                    self.current_mana -= 2
                    print("-----------------剩余水晶为:{0}".format(self.current_mana))
                    if self.myturn:
                        show_cards(self.myhandcards)
                    else:
                        show_cards(self.enemyhandcards)
            if self.enemyhero.hero_class == 'Warlock':
                self.auto_goto_world()

    def auto_goto_world(self):
        """
        敌方动作
        :return: 
        """
        index = -1
        select = -1
        while index != -2:
            for i in range(len(self.enemyhandcards)):
                if self.enemyhandcards[i].mana <= self.current_mana:
                    select = self.current_mana - self.enemyhandcards[i].mana
                    index = i
                    break
                else:
                    index = -2
            if select > 0 and -1 < index < len(self.enemyhandcards) - 1:
                for j in range(index + 1, len(self.enemyhandcards)):
                    if self.enemyhandcards[j].mana <= self.current_mana:
                        select2 = self.current_mana - self.enemyhandcards[j].mana
                        if select > select2:
                            select = select2
                            index = j
            if len(self.enemyhandcards) == 0:
                index = -2
            if index != -2:
                print("^^^^敌方手牌^^^^^^^^^^^^")
                show_cards(self.enemyhandcards)
                self.current_mana -= self.enemyhandcards[index].mana
                if self.enemyhandcards[index].type == 'Follower':
                    if len(self.enemyworldcards) < WORLDCARDNUM:
                        if self.enemyhandcards[index].property.find('Battlecry') != -1:
                            self.battle_cry(self.enemyhandcards[index], self.enemyhero, self.myhero,
                                            self.enemyworldcards, self.myworldcards, self.enemyhandcards,
                                            self.myhandcards, self.enemycards, self.mycards)
                        else:
                            self.enemyworldcards.append(self.enemyhandcards[index])
                            print(">>>>>>{0}-{1}({2})".format(
                                index + 1, self.enemyhandcards[index].name,
                                self.enemyhandcards[index].mana),
                                end='')
                            if self.enemyhandcards[index].property != '':
                                print("[{0}]".format(self.enemyhandcards[index].property), end='')
                            print("上场！！！")
                    else:
                        print("场上随从已满，随从无法上场！")
                        break
                elif self.enemyhandcards[index].type == 'Magic':
                    if not self.cast(self.enemyhandcards[index], self.enemyhero, self.myhero,
                                     self.enemyworldcards, self.myworldcards, self.enemyhandcards, self.myhandcards,
                                     self.enemycards, self.mycards):
                        break
                try:
                    if self.enemyhandcards[index] in self.enemyhandcards:
                        self.enemyhandcards.remove(self.enemyhandcards[index])
                except Exception as e:
                    print(e)
                index = -1
                select = -1

    def can_use_skill(self):
        """
        判断是否可以使用英雄技能
        :return: 
        """
        can_use = False
        if self.myhero.use_skill == False and self.current_mana >= 2:
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
        elif not self.myturn:
            card_id = randint(0, len(cards) - 1)
            if card_has_taunt(cards):
                if cards[card_id].property.find('Taunt') != -1:
                    return card_id
                else:
                    return self.attack_who(cards)
            elif card_has_stealth(cards):
                if cards[card_id].property.find('Stealth') == -1:
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
