# encoding:utf-8
# @Time     : 2019/5/15 18:00
# @Author   : Jerry Chou
# @File     : main_v34.0.py
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
#             30.英雄攻击、随从攻击、出牌和英雄技能可以交错进行
#                恐狼先锋：相邻的随从获得+1攻击力
#             31.凶恶的雏龙：在该随从攻击过英雄后，获得进化（+3攻、+3血、+1攻+1血、风怒、潜行、嘲讽）3选1
#                卡牌属性：风怒WindAngry--一个拥有风怒的角色可以在一个回合内攻击两次
#             32.卡牌属性：Revert--如果这张牌在你的手牌中，每个回合使其攻击力和生命值互换
#                卡牌属性：磁力Magnetic--放机械随从的左边，把磁力随从融合到该机械随从上
#             33.梦魇之龙：在你的回合开始时，该随从的攻击力翻倍
#                通道爬行者：如果该牌在你的手牌中，每当一个随从死亡，法力值消耗就减少1点
#                迦顿男爵：在你的回合结束时，对所有其他角色造成2点伤害
#             34.卡牌属性：超杀OverKill--如果造成过量的伤害，则会产生额外的效果
#                阵线破坏者：超杀--该随从的攻击力翻倍
#                巫妖王：在你的回合结束时,随机将一张死亡骑士牌置入你的手牌
#                增加武器属性



from generate_cards import generate_cards
from parse import parse_card
from fight import *
from random import randint
import random
from card import Card
from hero import Hero
from common import *
from card_collection import *

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
        self.myweapon = None
        enemyhero_num = randint(0, len(hero_list)) - 1
        self.enemyhero = Hero(hero_list[enemyhero_num])
        self.enemyweapon = None
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

    def round_end(self):
        """
        回合结束触发效果
        :return: 
        """
        if self.myturn:
            for card in self.myworldcards:
                if card.present_property.find('RoundEnd') != -1:
                    print("------> 回合结束触发 <------")
                    if card.name == '迦顿男爵':
                        for worldcard in self.myworldcards:
                            if worldcard.name != '迦顿男爵':
                                print(
                                    ">>>{0}->{1} 生命值 {2}->".format(card.name, worldcard.name, worldcard.remain_health),
                                    end='')
                                worldcard.reduce_health(2)
                                print("{0}".format(worldcard.remain_health))
                        for worldcard in self.enemyworldcards:
                            print(">>>{0}->{1} 生命值 {2}->".format(card.name, worldcard.name, worldcard.remain_health),
                                  end='')
                            worldcard.reduce_health(2)
                            print("{0}".format(worldcard.remain_health))
                        print(">>>{0}->{1} 生命值 {2}".format(card.name, self.myhero.name, self.myhero.remain_health),
                              end='')
                        if self.myhero.armor > 0:
                            print("[{0}]".format(self.enemyhero.armor), end='')
                        self.myhero.reduce_health(2)
                        print("->{0}".format(self.myhero.remain_health), end='')
                        if self.myhero.armor > 0:
                            print("[{0}]".format(self.enemyhero.armor), end='')
                        print("")
                        print(
                            ">>>{0}->{1} 生命值 {2}".format(card.name, self.enemyhero.name, self.enemyhero.remain_health),
                            end='')
                        if self.enemyhero.armor > 0:
                            print("[{0}]".format(self.enemyhero.armor), end='')
                        self.enemyhero.reduce_health(2)
                        print("->{0}".format(self.enemyhero.remain_health), end='')
                        if self.enemyhero.armor > 0:
                            print("[{0}]".format(self.enemyhero.armor), end='')
                        print("")
                    elif card.name == '巫妖王':
                        if len(self.myhandcards) < HANDCARDNUM:
                            lich_king_card = lich_king_cards()
                            self.myhandcards.append(lich_king_card)
                            print(">>>{0}->{1}".format(card.name, lich_king_card.name))
        else:
            for card in self.enemyworldcards:
                if card.present_property.find('RoundEnd') != -1:
                    print("------> 回合结束触发 <------")
                    if card.name == '迦顿男爵':
                        for worldcard in self.enemyworldcards:
                            if worldcard.name != '迦顿男爵':
                                print(
                                    ">>>{0}->{1} 生命值 {2}->".format(card.name, worldcard.name, worldcard.remain_health),
                                    end='')
                                worldcard.reduce_health(2)
                                print("{0}".format(worldcard.remain_health))
                        for worldcard in self.myworldcards:
                            print(">>>{0}->{1} 生命值 {2}->".format(card.name, worldcard.name, worldcard.remain_health),
                                  end='')
                            worldcard.reduce_health(2)
                            print("{0}".format(worldcard.remain_health))
                        print(">>>{0}->{1} 生命值 {2}".format(card.name, self.myhero.name, self.myhero.remain_health),
                              end='')
                        if self.myhero.armor > 0:
                            print("[{0}]".format(self.enemyhero.armor), end='')
                        self.myhero.reduce_health(2)
                        print("->{0}".format(self.myhero.remain_health), end='')
                        if self.myhero.armor > 0:
                            print("[{0}]".format(self.myhero.armor), end='')
                        print("")
                        print(
                            ">>>{0}->{1} 生命值 {2}".format(card.name, self.enemyhero.name, self.enemyhero.remain_health),
                            end='')
                        if self.enemyhero.armor > 0:
                            print("[{0}]".format(self.enemyhero.armor), end='')
                        self.enemyhero.reduce_health(2)
                        print("->{0}".format(self.enemyhero.remain_health), end='')
                        if self.enemyhero.armor > 0:
                            print("[{0}]".format(self.enemyhero.armor), end='')
                        print("")
                    elif card.name == '巫妖王':
                        if len(self.enemyhandcards) < HANDCARDNUM:
                            lich_king_card = lich_king_cards()
                            self.enemyhandcards.append(lich_king_card)
                            print(">>>{0} -> {1}".format(card.name, lich_king_card.name))

    def round_begin(self):
        """
        回合开始触发效果
        :return: 
        """
        if self.myturn:
            self.myhero.use_skill = False
            for card in self.myworldcards:
                if card.present_property == 'RoundBegin':
                    print("------> 回合开始触发 <------")
                    if card.name == '治疗图腾':
                        print("{0}：己方在场卡牌群体治疗+1".format(card.name))
                        for card in self.myworldcards:
                            card.add_health(1)
                    elif card.name == '梦魇之龙':
                        card.present_damage *= 2
        else:
            self.enemyhero.use_skill = False
            for card in self.enemyworldcards:
                if card.present_property == 'RoundBegin':
                    print("------> 回合开始触发 <------")
                    if card.name == '治疗图腾':
                        print("{0}：己方在场卡牌群体治疗+1".format(card.name))
                        for card in self.enemyworldcards:
                            card.add_health(1)
                    elif card.name == '梦魇之龙':
                        card.present_damage *= 2
        self.update_world_card()

    def can_use_skill(self):
        """
        判断是否可以使用英雄技能
        :return: 
        """
        can_use = False
        if self.myturn:
            if self.myhero.hero_class == 'Paladin':
                if len(self.myworldcards) < WORLDCARDNUM and self.myhero.use_skill == False and self.current_mana >= 2:
                    can_use = True
            elif self.myhero.hero_class == 'Shaman':
                if len(self.myworldcards) < WORLDCARDNUM and len(
                        self.myhero.totem) > 0 and self.myhero.use_skill == False and self.current_mana >= 2:
                    can_use = True
            else:
                if self.myhero.use_skill == False and self.current_mana >= 2:
                    can_use = True
        else:
            if self.enemyhero.hero_class == 'Paladin':
                if len(
                        self.enemyworldcards) < WORLDCARDNUM and self.enemyhero.use_skill == False and self.current_mana >= 2:
                    can_use = True
            elif self.enemyhero.hero_class == 'Shaman':
                if len(self.enemyworldcards) < WORLDCARDNUM and len(
                        self.enemyhero.totem) > 0 and self.enemyhero.use_skill == False and self.current_mana >= 2:
                    can_use = True

            elif self.enemyhero.hero_class == 'Priest':
                world = [self.enemyhero] + self.enemyworldcards
                choose_num = -1
                for i in range(len(world)):
                    if world[i].remain_health != world[i].present_health:
                        choose_num = i + 1
                        break
                if choose_num != -1 and self.enemyhero.use_skill == False and self.current_mana >= 2:
                    can_use = True
            else:
                if self.enemyhero.use_skill == False and self.current_mana >= 2:
                    can_use = True
        return can_use

    def can_use_handcard(self):
        """
        判断是否剩余水晶足够：有卡牌的水晶小于剩余水晶
        :return: 
        """
        # can_use = False
        can_use_list = []
        if self.myturn:
            for card in self.myhandcards:
                if card.type == 'Follower':
                    if card.mana <= self.current_mana and len(self.myworldcards) < WORLDCARDNUM:
                        can_use_list.append(card)
                else:
                    if card.mana <= self.current_mana:
                        can_use_list.append(card)
        else:
            for card in self.enemyhandcards:
                if card.type == 'Follower':
                    if card.mana <= self.current_mana and len(self.enemyworldcards) < WORLDCARDNUM:
                        can_use_list.append(card)
                else:
                    if card.mana <= self.current_mana:
                        can_use_list.append(card)
        return can_use_list

    def hero_can_attack(self):
        """
        英雄是否可以攻击
        :return: 
        """
        can_attack = False
        if self.myturn:
            if self.myhero.present_attack_count > 0 and self.myhero.present_damage > 0:
                can_attack = True
        else:
            if self.enemyhero.present_attack_count > 0 and self.enemyhero.present_damage > 0:
                can_attack = True
        return can_attack

    def follower_can_attack(self):
        """
        随从是否可以攻击
        :return: 
        """
        can_attack_list = []
        if self.myturn:
            for card in self.myworldcards:
                if card.present_property.find('Rush') != -1 and card.present_attack_count > 0:
                    if card_has_notstealth(self.enemyworldcards):
                        can_attack_list.append(card)
                else:
                    if card.present_attack_count > 0 and card.sleep == False and card.present_damage > 0:
                        can_attack_list.append(card)
        else:
            for card in self.enemyworldcards:
                if card.present_property.find('Rush') != -1 and card.present_attack_count > 0:
                    if card_has_notstealth(self.myworldcards):
                        can_attack_list.append(card)
                else:
                    if card.present_attack_count > 0 and card.sleep == False and card.present_damage > 0:
                        can_attack_list.append(card)
        return can_attack_list

    def do_action(self):
        while self.can_use_skill() or self.hero_can_attack() or len(self.follower_can_attack()) != 0 or len(
                self.can_use_handcard()) != 0:
            if self.myturn:
                if len(self.can_use_handcard()) != 0:
                    print("1-使用手牌", end=' ')
                if self.can_use_skill():
                    print("2-使用技能", end=' ')
                if self.hero_can_attack():
                    print("3-英雄攻击", end=' ')
                if len(self.follower_can_attack()) != 0:
                    print("4-随从攻击", end=' ')
                print("5-结束回合")
                choose = input_int("请选择操作的序号：")
                if choose == 2:
                    if self.can_use_skill():
                        self.skill_using()
                elif choose == 3:
                    if self.hero_can_attack():
                        self.hero_battle()
                elif choose == 4:
                    if len(self.follower_can_attack()) != 0:
                        self.follower_battle()
                elif choose == 1:
                    if len(self.can_use_handcard()) != 0:
                        self.use_handcard()
                elif choose == 5:
                    break
                else:
                    continue
            else:
                if len(self.can_use_handcard()) != 0:
                    self.use_handcard()
                elif self.can_use_skill():
                    self.skill_using()
                elif self.hero_can_attack():
                    self.hero_battle()
                elif len(self.follower_can_attack()) != 0:
                    self.follower_battle()
            if not self.check_game_over():
                self.update_hero_damage()
                self.update_world()
                self.update_thisround_cards()
            else:
                break

    def before_round(self):
        """
        回合开始前的动作
        :return: 
        """
        self.current_mana = self.mana
        self.update_hero()
        self.update_previousround_cards()
        self.update_world()
        self.update_thisround_cards()
        self.myturn = not self.myturn
        self.round_begin()
        self.draw_card()

    def check_game_over(self):
        """
        英雄是否死亡
        :return: 
        """
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
        self.before_round()
        self.show_world()
        if not self.check_game_over():
            surrender = input(">>>>>>>>>>>>>>是否投降(Y/N)？")
            if surrender == 'Y' or surrender == 'y':
                print("~~~~~~~~~~~{0}~~~~~~~~~~~~~".format(self.myhero.surrender))
            else:
                self.do_action()
                self.round_end()
                if not self.check_game_over():
                    self.before_round()
                    if not self.check_game_over():
                        self.do_action()
                        self.round_end()
                        if not self.check_game_over():
                            self.round += 1
                            # 水晶达到10后不再增加
                            if self.mana < 10:
                                self.mana += 1
                            self.turn_round()

    def update_weapon(self):
        """
        更新武器耐久度用完的效果
        :return: 
        """
        if self.myweapon is not None:
            if not self.myweapon.alive:
                if self.myweapon.name == '霜之哀伤':
                    self.death_rattle(self.myweapon, self.myhero, self.enemyhero, self.myworldcards,
                                      self.enemyworldcards, self.myhandcards, self.enemyhandcards, self.mycards,
                                      self.enemycards)
                self.myweapon = None
        if self.enemyweapon is not None:
            if not self.enemyweapon.alive:
                if self.enemyweapon.name == '霜之哀伤':
                    self.death_rattle(self.enemyweapon, self.enemyhero, self.myhero, self.enemyworldcards,
                                      self.myworldcards, self.enemyhandcards, self.myhandcards, self.enemycards,
                                      self.mycards)
                self.enemyweapon = None

    def update_world(self):
        """
        删除血量<=0的卡牌
        :return: 
        """
        for i in range(len(self.myworldcards) - 1, -1, -1):
            card = self.myworldcards[i]
            if card.remain_health <= 0 or not card.alive:
                for handcard in self.myhandcards:
                    if handcard.name == '通道爬行者' and handcard.mana > 0:
                        handcard.mana -= 1
                for handcard in self.enemyhandcards:
                    if handcard.name == '通道爬行者' and handcard.mana > 0:
                        handcard.mana -= 1
                if card.present_property.find('Deathrattle') != -1:
                    self.death_rattle(card, self.myhero, self.enemyhero, self.myworldcards, self.enemyworldcards,
                                      self.myhandcards, self.enemyhandcards, self.mycards, self.enemycards)
                self.myworldcards.remove(card)
                if card.race == 'totem':
                    card.reset()
                    self.myhero.totem.append(card)
        for i in range(len(self.enemyworldcards) - 1, -1, -1):
            card = self.enemyworldcards[i]
            if card.remain_health <= 0 or not card.alive:
                for handcard in self.myhandcards:
                    if handcard.name == '通道爬行者' and handcard.mana > 0:
                        handcard.mana -= 1
                for handcard in self.enemyhandcards:
                    if handcard.name == '通道爬行者' and handcard.mana > 0:
                        handcard.mana -= 1
                if card.present_property.find('Deathrattle') != -1:
                    self.death_rattle(card, self.enemyhero, self.myhero, self.enemyworldcards, self.myworldcards,
                                      self.enemyhandcards, self.myhandcards, self.enemycards, self.mycards)
                self.enemyworldcards.remove(card)
                if card.race == 'totem':
                    card.reset()
                    self.enemyhero.totem.append(card)

    def update_thisround_cards(self):
        """
        更新光环伤害
        :return: 
        """
        # 重置光环伤害为0
        for card in self.myworldcards:
            card.reset_halo_damage()
        for card in self.enemyworldcards:
            card.reset_halo_damage()
        # 重新计算光环伤害
        for index, card in enumerate(self.myworldcards):
            if card.name == '恐狼先锋':
                if index > 0:
                    self.myworldcards[index - 1].halo_damage += 1
                if index < len(self.myworldcards) - 1:
                    self.myworldcards[index + 1].halo_damage += 1
        for index, card in enumerate(self.enemyworldcards):
            if card.name == '恐狼先锋':
                if index > 0:
                    self.enemyworldcards[index - 1].halo_damage += 1
                if index < len(self.enemyworldcards) - 1:
                    self.enemyworldcards[index + 1].halo_damage += 1
        # 更新当前伤害
        for card in self.myworldcards:
            card.update_halo_damage()
        for card in self.enemyworldcards:
            card.update_halo_damage()

    def update_previousround_cards(self):
        """
        更新上回合的临时数据
        :return: 
        """
        if self.myturn:
            for card in self.myworldcards:
                if card.change_damage != 0:
                    card.reset_change_damage()
                card.present_attack_count = card.attack_count
            self.myhero.present_attack_count = self.myhero.attack_count
            for card in self.myhandcards:
                if card.present_property.find('Revert') != -1:
                    temp = card.health
                    card.health = card.damage
                    card.remain_health = card.health
                    card.present_health = card.health
                    card.damage = temp
                    card.present_damage = card.damage
        else:
            for card in self.enemyworldcards:
                if card.change_damage != 0:
                    card.reset_change_damage()
                card.present_attack_count = card.attack_count
            self.enemyhero.present_attack_count = self.enemyhero.attack_count
            for card in self.enemyhandcards:
                if card.present_property.find('Revert') != -1:
                    temp = card.health
                    card.health = card.damage
                    card.remain_health = card.health
                    card.present_health = card.health
                    card.damage = temp
                    card.present_damage = card.damage

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
        self.myhero.present_damage = self.myhero.hero_damage
        if self.myweapon is not None:
            self.myhero.present_damage += self.myweapon.present_damage
        self.enemyhero.present_damage = self.enemyhero.hero_damage
        if self.enemyweapon is not None:
            self.enemyhero.present_damage += self.enemyweapon.present_damage

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
                        print(">>>{0}->{1} 生命值 {2}".format(draw_card.name, self.myhero.name, self.myhero.remain_health),
                              end='')
                        if self.myhero.armor > 0:
                            print("[{0}]".format(self.myhero.armor), end='')
                        self.myhero.reduce_health(3)
                        print("->{0}".format(self.myhero.remain_health), end='')
                        if self.myhero.armor > 0:
                            print("[{0}]".format(self.myhero.armor), end='')
                        print("")
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
                print(">>>疲劳{0}->{1} 生命值 {2}".format(self.myhero.tired, self.myhero.name, self.myhero.remain_health),
                      end='')
                if self.myhero.armor > 0:
                    print("[{0}]".format(self.myhero.armor), end='')
                self.myhero.reduce_health(self.myhero.tired)
                print("->{0}".format(self.myhero.remain_health), end='')
                if self.myhero.armor > 0:
                    print("[{0}]".format(self.myhero.armor), end='')
                print("")
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
                        print(">>>{0}->{1} 生命值 {2}".format(draw_card.name, self.enemyhero.name,
                                                           self.enemyhero.remain_health), end='')
                        if self.enemyhero.armor > 0:
                            print("[{0}]".format(self.enemyhero.armor), end='')
                        self.enemyhero.reduce_health(3)
                        print("->{0}".format(self.enemyhero.remain_health), end='')
                        if self.enemyhero.armor > 0:
                            print("[{0}]".format(self.enemyhero.armor), end='')
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
                print(">>>疲劳{0}->{1} 生命值 {2}".format(self.enemyhero.tired, self.enemyhero.name,
                                                     self.enemyhero.remain_health), end='')
                if self.enemyhero.armor > 0:
                    print("[{0}]".format(self.enemyhero.armor), end='')
                self.enemyhero.reduce_health(self.enemyhero.tired)
                print("->{0}".format(self.enemyhero.remain_health), end='')
                if self.enemyhero.armor > 0:
                    print("[{0}]".format(self.enemyhero.armor), end='')
                print("")
                while BloodOfFallenNum > 0:
                    randnum1 = randint(0, len(self.enemycards))
                    self.enemycards.insert(randnum1, Card('', '堕落之血', '', '', '', '', 1, '', 'Magic', False))
                    randnum2 = randint(0, len(self.enemycards))
                    self.enemycards.insert(randnum2, Card('', '堕落之血', '', '', '', '', 1, '', 'Magic', False))
                    BloodOfFallenNum -= 1

    def skill_using(self):
        """
        使用技能
        """
        self.current_mana -= 2
        if self.myturn:
            self.myhero.use_skill = True
            if self.myhero.hero_class == 'Warrior':
                self.myhero.armor += 2
                print("英雄技能：全副武装")
            elif self.myhero.hero_class == 'Hunter':
                print("英雄技能：稳固射击")
                print(">>>稳固射击->{0} 生命值 {1}".format(self.enemyhero.name, self.enemyhero.remain_health), end='')
                if self.enemyhero.armor > 0:
                    print("[{0}]".format(self.enemyhero.armor), end='')
                self.enemyhero.reduce_health(2)
                print("->{0}".format(self.enemyhero.remain_health), end='')
                if self.enemyhero.armor > 0:
                    print("[{0}]".format(self.enemyhero.armor), end='')
                print("")
            elif self.myhero.hero_class == 'Warlock':
                print("英雄技能：生命分流")
                self.draw_card()
                print(">>>生命分流->{0} 生命值 {1}".format(self.myhero.name, self.myhero.remain_health), end='')
                if self.myhero.armor > 0:
                    print("[{0}]".format(self.myhero.armor), end='')
                self.myhero.reduce_health(2)
                print("->{0}".format(self.myhero.remain_health), end='')
                if self.myhero.armor > 0:
                    print("[{0}]".format(self.myhero.armor), end='')
                print("")
            elif self.myhero.hero_class == 'Priest':
                world = [self.enemyhero]
                for card in self.enemyworldcards:
                    if card.present_property.find('Stealth') == -1:
                        world.append(card)
                world += [self.myhero] + self.myworldcards
                for i in range(len(world)):
                    print("{0}-{1}({2}-{3}".format(i + 1, world[i].name, world[i].present_damage,
                                                   world[i].remain_health), end='')
                    if world[i].armor > 0:
                        print("[{0}]".format(world[i].armor), end='')
                    print("/{0})".format(world[i].present_health), end='')
                    if world[i].present_property != '':
                        print("[{0}]".format(world[i].present_property), end=' ')
                    else:
                        print(end=' ')
                print('')
                choose_num = choose_direct_num(world, "请选择加血对象序号：")
                world[choose_num - 1].add_health(2)
                print("英雄技能：次级治疗术->{0}".format(world[choose_num - 1].name))
                print("{0}-{1}({2}-{3}/{4})".format(choose_num, world[choose_num - 1].name,
                                                    world[choose_num - 1].present_damage,
                                                    world[choose_num - 1].remain_health,
                                                    world[choose_num - 1].present_health))
            elif self.myhero.hero_class == 'Mage':
                world = [self.enemyhero]
                for card in self.enemyworldcards:
                    if card.present_property.find('AntiMagic') == -1 and card.present_property.find('Stealth') == -1:
                        world.append(card)
                world += [self.myhero] + self.myworldcards
                for i in range(len(world)):
                    print("{0}-{1}({2}-{3}".format(i + 1, world[i].name, world[i].present_damage,
                                                   world[i].remain_health), end='')
                    if world[i].armor > 0:
                        print("[{0}]".format(world[i].armor), end='')
                    print("/{0})".format(world[i].present_health), end='')
                    if world[i].present_property != '':
                        print("[{0}]".format(world[i].present_property), end=' ')
                    else:
                        print(end=' ')
                print('')
                choose_num = choose_direct_num(world, "请选择火焰冲击对象序号：")
                print("英雄技能：火焰冲击->{0} 生命值 {1}".format(world[choose_num - 1].name, world[choose_num - 1].remain_health),
                      end='')
                if world[choose_num - 1].armor > 0:
                    print("[{0}]".format(world[choose_num - 1].armor), end='')
                world[choose_num - 1].reduce_health(1)
                print("->{0}".format(world[choose_num - 1].remain_health), end='')
                if world[choose_num - 1].armor > 0:
                    print("[{0}]".format(world[choose_num - 1].armor), end='')
                print("")
            elif self.myhero.hero_class == 'Rogue':
                print("英雄技能：匕首精通")
                sword = Card('', '匕首', '', '', 1, 2, 1, '', 'Weapon', False)
                if self.myweapon is not None:
                    self.myweapon.alive = False
                    self.update_weapon()
                self.myweapon = sword
                print(">>>装备 {0}".format(self.myweapon.name))
            elif self.myhero.hero_class == 'Druid':
                self.myhero.hero_damage += 1
                self.myhero.armor += 1
                print("英雄技能：变形")
            elif self.myhero.hero_class == 'Paladin':
                soldier = Card('', '白银新兵', '', '', 1, 1, 1, '', 'Follower')
                print("英雄技能：援军")
                self.myworldcards.append(soldier)
            elif self.myhero.hero_class == 'Shaman':
                random_index = randint(0, len(self.myhero.totem) - 1)
                self.myworldcards.append(self.myhero.totem[random_index])
                print("英雄技能：{0}".format(self.myhero.totem[random_index].name))
                self.myhero.totem.remove(self.myhero.totem[random_index])

        else:
            self.enemyhero.use_skill = True
            if self.enemyhero.hero_class == 'Warrior':
                self.enemyhero.armor += 2
                print("英雄技能：全副武装")
            elif self.enemyhero.hero_class == 'Hunter':
                print("英雄技能：稳固射击")
                print(">>>稳固射击->{0} 生命值 {1}".format(self.myhero.name, self.myhero.remain_health), end='')
                if self.myhero.armor > 0:
                    print("[{0}]".format(self.myhero.armor), end='')
                self.myhero.reduce_health(2)
                print("->{0}".format(self.myhero.remain_health), end='')
                if self.myhero.armor > 0:
                    print("[{0}]".format(self.myhero.armor), end='')
                print("")
            elif self.enemyhero.hero_class == 'Warlock':
                print("英雄技能：生命分流")
                self.draw_card()
                print(">>>生命分流->{0} 生命值 {1}".format(self.enemyhero.name, self.enemyhero.remain_health), end='')
                if self.enemyhero.armor > 0:
                    print("[{0}]".format(self.enemyhero.armor), end='')
                self.enemyhero.reduce_health(2)
                print("->{0}".format(self.enemyhero.remain_health), end='')
                if self.enemyhero.armor > 0:
                    print("[{0}]".format(self.enemyhero.armor), end='')
                print("")
            elif self.enemyhero.hero_class == 'Priest':
                world = [self.enemyhero]
                for card in self.enemyworldcards:
                    if card.present_property.find('AntiMagic') == -1:
                        world.append(card)
                for i in range(len(world)):
                    print("{0}-{1}({2}-{3}".format(i + 1, world[i].name, world[i].present_damage,
                                                   world[i].remain_health), end='')
                    if world[i].armor > 0:
                        print("[{0}]".format(world[i].armor), end='')
                    print("/{0})".format(world[i].present_health), end='')
                    if world[i].present_property != '':
                        print("[{0}]".format(world[i].present_property), end=' ')
                    else:
                        print(end=' ')
                print('')
                for i in range(len(world)):
                    if world[i].remain_health != world[i].present_health:
                        choose_num = i + 1
                        break
                else:
                    choose_num = randint(1, len(world))
                print(">>>>>>>目标序号：{0}".format(choose_num))
                world[choose_num - 1].add_health(2)
                print("英雄技能：次级治疗术->{0}".format(world[choose_num - 1].name))
                print("{0}-{1}({2}-{3}/{4})".format(choose_num, world[choose_num - 1].name,
                                                    world[choose_num - 1].present_damage,
                                                    world[choose_num - 1].remain_health,
                                                    world[choose_num - 1].present_health))
            elif self.enemyhero.hero_class == 'Mage':
                world = [self.myhero]
                for card in self.myworldcards:
                    if card.present_property.find('AntiMagic') == -1 and card.present_property.find('Stealth') == -1:
                        world.append(card)
                for i in range(len(world)):
                    print("{0}-{1}({2}-{3}".format(i + 1, world[i].name, world[i].present_damage,
                                                   world[i].remain_health), end='')
                    if world[i].armor > 0:
                        print("[{0}]".format(world[i].armor), end='')
                    print("/{0})".format(world[i].present_health), end='')
                    if world[i].present_property != '':
                        print("[{0}]".format(world[i].present_property), end=' ')
                    else:
                        print(end=' ')
                print('')
                choose_num = -1
                for i in range(len(world)):
                    if world[i].remain_health == 1:
                        choose_num = i + 1
                        break
                if choose_num == -1:
                    choose_num = randint(1, len(world))
                print(">>>>>>>目标序号：{0}".format(choose_num))
                print("英雄技能：火焰冲击->{0} 生命值 {1}".format(world[choose_num - 1].name, world[choose_num - 1].remain_health),
                      end='')
                if world[choose_num - 1].armor > 0:
                    print("[{0}]".format(world[choose_num - 1].armor), end='')
                world[choose_num - 1].reduce_health(1)
                print("->{0}".format(world[choose_num - 1].remain_health), end='')
                if world[choose_num - 1].armor > 0:
                    print("[{0}]".format(world[choose_num - 1].armor), end='')
                print("")
            elif self.enemyhero.hero_class == 'Rogue':
                print("英雄技能：匕首精通")
                sword = Card('', '匕首', '', '', 1, 2, 1, '', 'Weapon', False)
                if self.enemyweapon is not None:
                    self.enemyweapon.alive = False
                    self.update_weapon()
                self.enemyweapon = sword
                print(">>>装备 {0}".format(self.enemyweapon.name))
            elif self.enemyhero.hero_class == 'Druid':
                self.enemyhero.hero_damage += 1
                self.enemyhero.armor += 1
                print("英雄技能：变形")
            elif self.enemyhero.hero_class == 'Paladin':
                soldier = Card('', '白银新兵', '', '', 1, 1, 1, '', 'Follower')
                print("英雄技能：援军")
                self.enemyworldcards.append(soldier)
            elif self.enemyhero.hero_class == 'Shaman':
                random_index = randint(0, len(self.enemyhero.totem) - 1)
                self.enemyworldcards.append(self.enemyhero.totem[random_index])
                print("英雄技能：{0}".format(self.enemyhero.totem[random_index].name))
                self.enemyhero.totem.remove(self.enemyhero.totem[random_index])

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
            print("({0}-{1})".format(self.enemyhero.present_damage, self.enemyweapon.remain_health), end='')
        print(" 剩余卡牌：{0}".format(len(self.enemycards)))
        if len(self.enemyworldcards) > 0:
            for card in self.enemyworldcards:
                print(
                    "{0}({1}-{2}/{3})".format(card.name, card.present_damage, card.remain_health, card.present_health),
                    end='')
                if card.present_property != '':
                    print("[{0}]".format(card.present_property), end=' ')
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
                if card.present_property != '':
                    print("[{0}]".format(card.present_property), end=' ')
                else:
                    print(end=' ')
            print('')
        else:
            print("场上无卡牌")
        print("{0}：{1}".format(self.myhero.name, self.myhero.remain_health), end='')
        if self.myhero.armor > 0:
            print("[{0}]".format(self.myhero.armor), end='')
        if self.myhero.present_damage > 0:
            print("({0}-{1})".format(self.myhero.present_damage, self.myweapon.remain_health), end='')
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
                    if self.enemyworldcards[i].present_property != '':
                        print("[{0}]".format(self.enemyworldcards[i].present_property), end=' ')
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

    def use_handcard(self):
        """
        使用手牌
        :return: 
        """
        if self.myturn:
            print("-----------------剩余水晶为:{0}".format(self.current_mana))
            print("^^^^我方手牌^^^^^^^^^^^^")
            show_cards(self.myhandcards)
            goto_num = choose_object_num(self.myhandcards, ">>>>>>>>>>>>>>请选择你要使用的卡牌号码，不再使用水晶请输入0：")
            if goto_num == 0:
                return
            elif self.myhandcards[goto_num - 1].mana <= self.current_mana:
                if self.myhandcards[goto_num - 1].type == 'Follower':
                    if len(self.myworldcards) < WORLDCARDNUM:
                        if self.myhandcards[goto_num - 1].present_property.find('Battlecry') != -1:
                            self.battle_cry(self.myhandcards[goto_num - 1], self.myhero, self.enemyhero,
                                            self.myworldcards, self.enemyworldcards, self.myhandcards,
                                            self.enemyhandcards, self.mycards, self.enemycards)
                        else:
                            if len(self.myworldcards) == 0:
                                self.myworldcards.append(self.myhandcards[goto_num - 1])
                            else:
                                for index, worldcard in enumerate(self.myworldcards):
                                    print(" <<{0}>> {1}".format(index, worldcard.name), end='')
                                print(" <<{0}>>".format(len(self.myworldcards)))
                                choose_num = choose_object_num(self.myworldcards, "请选择卡牌要上场位置的序号：")
                                if choose_num < len(self.myworldcards):
                                    if self.myworldcards[choose_num].race.find('Machine') != -1 and self.myhandcards[
                                                goto_num - 1].present_property.find('Magnetic') != -1:
                                        self.myworldcards[choose_num].present_health += self.myhandcards[
                                            goto_num - 1].health
                                        self.myworldcards[choose_num].remain_health += self.myhandcards[
                                            goto_num - 1].health
                                        self.myworldcards[choose_num].buff_damage += self.myhandcards[
                                            goto_num - 1].damage
                                        property_list = self.myhandcards[goto_num - 1].property.split(' ')
                                        for property in property_list:
                                            if self.myworldcards[choose_num].present_property.find(property) == -1:
                                                self.myworldcards[choose_num].present_property += (' ' + property)
                                    else:
                                        self.myworldcards.insert(choose_num, self.myhandcards[goto_num - 1])
                                else:
                                    self.myworldcards.insert(choose_num, self.myhandcards[goto_num - 1])
                            print(">>>>>>{0}-{1}({2})".format(
                                goto_num, self.myhandcards[goto_num - 1].name,
                                self.myhandcards[goto_num - 1].mana),
                                end='')
                            if self.myhandcards[goto_num - 1].present_property != '':
                                print("[{0}]".format(self.myhandcards[goto_num - 1].present_property), end='')
                            print("上场！！！")
                            self.current_mana -= self.myhandcards[goto_num - 1].mana
                    else:
                        print("场上随从已满，随从无法上场！")
                elif self.myhandcards[goto_num - 1].type == 'Magic':
                    if self.cast(self.myhandcards[goto_num - 1], self.myhero, self.enemyhero,
                                 self.myworldcards, self.enemyworldcards, self.myhandcards,
                                 self.enemyhandcards, self.mycards, self.enemycards):
                        self.current_mana -= self.myhandcards[goto_num - 1].mana
                    else:
                        return
                elif self.myhandcards[goto_num - 1].type == 'Weapon':
                    if self.myweapon is not None:
                        self.myweapon.alive = False
                        self.update_weapon()
                    self.myweapon = self.myhandcards[goto_num - 1]
                    print(">>>装备 {0}".format(self.myweapon.name))
                    # self.myhero.equip(self.myhandcards[goto_num - 1])
                    self.current_mana -= self.myhandcards[goto_num - 1].mana
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
                if self.skill_using():
                    self.current_mana -= 2
                    print("-----------------剩余水晶为:{0}".format(self.current_mana))
                    if self.myturn:
                        show_cards(self.myhandcards)
                    else:
                        show_cards(self.enemyhandcards)
            if self.enemyhero.hero_class == 'Warlock':
                self.auto_goto_world()

    def hero_battle(self):
        """
        英雄攻击
        :return: 
        """
        if self.myturn:
            print("------------攻击----------------")
            print("{0}({1}-{2}".format(self.myhero.name, self.myhero.present_damage, self.myhero.remain_health), end='')
            if self.myhero.armor > 0:
                print("[{0}]) 准备攻击：".format(self.myhero.armor))
            else:
                print(") 准备攻击：")
            opposite = [self.enemyhero] + self.enemyworldcards
            for j in range(len(opposite)):
                print("{0}-{1}({2}-{3}".format(j + 1, opposite[j].name, opposite[j].present_damage,
                                               opposite[j].remain_health), end='')
                if opposite[j].armor > 0:
                    print("[{0}]".format(opposite[j].armor), end='')
                print("/{0})".format(opposite[j].present_health), end='')
                if opposite[j].present_property != '':
                    print("[{0}]".format(opposite[j].present_property), end=' ')
                else:
                    print(end=' ')
            print('')
            attack_num = choose_attack_num(opposite, "请选择攻击对象序号，不攻击输入0：")
            if attack_num == 0:
                return
            self.myhero.attack(opposite[attack_num - 1], self.myhero, self.enemyhero)
            if self.enemyhero.remain_health <= 0 or self.myhero.remain_health <= 0:
                return
            if self.myweapon is not None:
                if self.myweapon.name == '霜之哀伤' and opposite[attack_num - 1].type == 'Follower' and not opposite[
                            attack_num - 1].alive:
                    self.myhero.add_kill(opposite[attack_num - 1])
            self.myhero.show()
            opposite[attack_num - 1].show()
            if self.myweapon is not None:
                if self.myweapon.remain_health > 0:
                    self.myweapon.reduce_health(1)
        else:
            opposite = [self.myhero] + self.myworldcards
            print("------------攻击----------------")
            rand_num = self.attack_who(opposite)
            print(
                "{0}{1}-{3} ".format(self.enemyhero.name, self.enemyhero.present_damage, self.enemyhero.remain_health),
                end='')
            if self.enemyhero.armor > 0:
                print("[{0}]".format(self.enemyhero.armor), end=' ')
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
                if self.myweapon is not None:
                    if self.enemyweapon.name == '霜之哀伤' and self.myworldcards[rand_num - 1].type == 'Follower' and not \
                            self.myworldcards[rand_num - 1].alive:
                        self.enemyhero.add_kill(self.myworldcards[rand_num - 1])
            if self.myhero.remain_health <= 0 or self.enemyhero.remain_health <= 0:
                return
            self.enemyhero.show()
            if self.enemyweapon is not None:
                if self.enemyweapon.remain_health > 0:
                    self.enemyweapon.reduce_health(1)
        self.update_weapon()

    def follower_battle(self):
        """
        随从对战
        :return: 
        """
        if self.myturn:
            can_attack_list = self.follower_can_attack()
            for i in range(len(can_attack_list)):
                print("{0}-{1}({2}-{3}".format(i + 1, can_attack_list[i].name, can_attack_list[i].present_damage,
                                               can_attack_list[i].remain_health), end='')
                if can_attack_list[i].armor > 0:
                    print("[{0}]".format(can_attack_list[i].armor), end='')
                print("/{0})".format(can_attack_list[i].present_health), end='')
                if can_attack_list[i].present_property != '':
                    print("[{0}]".format(can_attack_list[i].present_property), end=' ')
                else:
                    print(end=' ')
            print('')
            ready_attack_num = choose_object_num(can_attack_list, "请选择进行攻击的对象序号，不攻击输入0：")
            if ready_attack_num == 0:
                return
            if can_attack_list[ready_attack_num - 1].present_property.find('Rush') != -1:
                opposite = self.enemyworldcards
            else:
                opposite = [self.enemyhero] + self.enemyworldcards
            print("------------攻击----------------")
            print("{0}({1}-{2})".format(can_attack_list[ready_attack_num - 1].name,
                                        can_attack_list[ready_attack_num - 1].present_damage,
                                        can_attack_list[ready_attack_num - 1].remain_health), end='')
            if can_attack_list[ready_attack_num - 1].present_property != '':
                print("[{0}] 准备攻击：".format(can_attack_list[ready_attack_num - 1].present_property))
            else:
                print(" 准备攻击：")
            for j in range(len(opposite)):
                print("{0}-{1}({2}-{3}".format(j + 1, opposite[j].name, opposite[j].present_damage,
                                               opposite[j].remain_health),
                      end='')
                if opposite[j].armor > 0:
                    print("[{0}]".format(opposite[j].armor), end='')
                print("/{0})".format(opposite[j].present_health), end='')
                if opposite[j].present_property != '':
                    print("[{0}]".format(opposite[j].present_property), end=' ')
                else:
                    print(end=' ')
            print('')
            attack_num = choose_attack_num(opposite, "请选择攻击对象序号，不攻击输入0：")
            if attack_num == 0:
                return
            if can_attack_list[ready_attack_num - 1].attack(opposite[attack_num - 1], self.myhero, self.enemyhero) and \
                            can_attack_list[ready_attack_num - 1].present_property.find('OverKill') != -1:
                self.over_kill(can_attack_list[ready_attack_num - 1], self.myhero, self.enemyhero, self.myworldcards,
                               self.enemyworldcards, self.myhandcards, self.enemyhandcards, self.mycards,
                               self.enemycards)
            if self.enemyhero.remain_health <= 0:
                return
            if can_attack_list[ready_attack_num - 1].name == '凶恶的雏龙' and opposite[attack_num - 1].type == 'Hero':
                evolution = ['+3攻', '+3血', '+1攻+1血', '风怒', '潜行', '嘲讽']
                choose_list = random.sample(evolution, 3)
                for index, item in enumerate(choose_list):
                    print("{0}.{1}".format(index + 1, item), end=' ')
                print("")
                choose = input_int("请选择进化的序号：")
                if choose_list[choose - 1] == '+3攻':
                    print("{0} 的攻击力 {1} >>>".format(can_attack_list[ready_attack_num - 1].name,
                                                    can_attack_list[ready_attack_num - 1].present_damage), end='')
                    can_attack_list[ready_attack_num - 1].buff_damage += 3
                    can_attack_list[ready_attack_num - 1].update_buff_damage()
                    print("{0}".format(can_attack_list[ready_attack_num - 1].present_damage))
                elif choose_list[choose - 1] == '+3血':
                    print("{0} 生命值 {1}/{2} >>>".format(can_attack_list[ready_attack_num - 1].name,
                                                       can_attack_list[ready_attack_num - 1].remain_health,
                                                       can_attack_list[ready_attack_num - 1].present_health), end='')
                    can_attack_list[ready_attack_num - 1].remain_health += 3
                    can_attack_list[ready_attack_num - 1].present_health += 3
                    print("{0}/{1}".format(can_attack_list[ready_attack_num - 1].remain_health,
                                           can_attack_list[ready_attack_num - 1].present_health))
                elif choose_list[choose - 1] == '+1攻+1血':
                    print("{0} {1}-{2}/{3} >>>".format(can_attack_list[ready_attack_num - 1].name,
                                                       can_attack_list[ready_attack_num - 1].present_damage,
                                                       can_attack_list[ready_attack_num - 1].remain_health,
                                                       can_attack_list[ready_attack_num - 1].present_health), end='')
                    can_attack_list[ready_attack_num - 1].buff_damage += 1
                    can_attack_list[ready_attack_num - 1].update_buff_damage()
                    can_attack_list[ready_attack_num - 1].remain_health += 1
                    can_attack_list[ready_attack_num - 1].present_health += 1
                    print("{0}-{1}/{2}".format(can_attack_list[ready_attack_num - 1].present_damage,
                                               can_attack_list[ready_attack_num - 1].remain_health,
                                               can_attack_list[ready_attack_num - 1].present_health))
                elif choose_list[choose - 1] == '风怒':
                    if can_attack_list[ready_attack_num - 1].present_property.find('WindAngry') == -1:
                        print("{0} 获得 风怒".format(can_attack_list[ready_attack_num - 1].name))
                        can_attack_list[ready_attack_num - 1].present_property += ' WindAngry'
                        can_attack_list[ready_attack_num - 1].present_attack_count += 1
                        can_attack_list[ready_attack_num - 1].attack_count = 2
                elif choose_list[choose - 1] == '潜行':
                    if can_attack_list[ready_attack_num - 1].present_property.find('Stealth') == -1:
                        print("{0} 获得 潜行".format(can_attack_list[ready_attack_num - 1].name))
                        can_attack_list[ready_attack_num - 1].present_property += ' Stealth'
                elif choose_list[choose - 1] == '嘲讽':
                    if can_attack_list[ready_attack_num - 1].present_property.find('Taunt') == -1:
                        print("{0} 获得 嘲讽".format(can_attack_list[ready_attack_num - 1].name))
                        can_attack_list[ready_attack_num - 1].present_property += ' Taunt'

            can_attack_list[ready_attack_num - 1].show()
            opposite[attack_num - 1].show()
        else:
            for i in range(len(self.enemyworldcards) - 1, -1, -1):
                self.update_world()
                self.update_thisround_cards()
                if self.enemyworldcards[i].present_damage > 0 and self.enemyworldcards[i].sleep == False:
                    if self.enemyworldcards[i].present_property.find('Rush') != -1:
                        opposite = self.myworldcards
                    else:
                        opposite = [self.myhero] + self.myworldcards
                    print("------------攻击----------------")
                    rand_num = self.attack_who(opposite)
                    print("{0}{1}-{2} ".format(self.enemyworldcards[i].name, self.enemyworldcards[i].present_damage,
                                               self.enemyworldcards[i].remain_health), end='')
                    if self.enemyworldcards[i].armor > 0:
                        print("[{0}]".format(self.enemyworldcards[i].armor), end='')
                    if self.enemyworldcards[i].present_property != '':
                        print("[{0}]".format(self.enemyworldcards[i].present_property), end='')
                    else:
                        print(end='')
                    print(" attack {0}{1}-{2}".format(opposite[rand_num].name, opposite[rand_num].present_damage,
                                                      opposite[rand_num].remain_health), end='')
                    if opposite[rand_num].armor > 0:
                        print("[{0}]".format(opposite[rand_num].armor), end='')
                    if opposite[rand_num].present_property != '':
                        print("[{0}]".format(opposite[rand_num].present_property))
                    else:
                        print('')
                    if self.enemyworldcards[i].attack(opposite[rand_num], self.enemyhero, self.myhero) and \
                                    self.enemyworldcards[i].present_property.find('OverKill') != -1:
                        self.over_kill(self.enemyworldcards[i], self.enemyhero, self.myhero,
                                       self.enemyworldcards,
                                       self.myworldcards, self.enemyhandcards, self.myhandcards, self.enemycards,
                                       self.mycards)
                    opposite[rand_num].show()
                    if self.myhero.remain_health <= 0:
                        break
                    if self.enemyworldcards[i].name == '凶恶的雏龙' and opposite[rand_num].type == 'Hero':
                        choose = randint(1, 6)
                        print(choose)
                        if choose == 1:
                            print("{0} 的攻击力 {1} >>>".format(self.enemyworldcards[i].name,
                                                            self.enemyworldcards[i].present_damage),
                                  end='')
                            self.enemyworldcards[i].buff_damage += 3
                            self.enemyworldcards[i].update_buff_damage()
                            print("{0}".format(self.enemyworldcards[i].present_damage))
                        elif choose == 2:
                            print("{0} 生命值 {1}/{2} >>>".format(self.enemyworldcards[i].name,
                                                               self.enemyworldcards[i].remain_health,
                                                               self.enemyworldcards[i].present_health),
                                  end='')
                            self.enemyworldcards[i].remain_health += 3
                            self.enemyworldcards[i].present_health += 3
                            print("{0}/{1}".format(self.enemyworldcards[i].remain_health,
                                                   self.enemyworldcards[i].present_health))
                        elif choose == 3:
                            print("{0} {1}-{2}/{3} >>>".format(self.enemyworldcards[i].name,
                                                               self.enemyworldcards[i].present_damage,
                                                               self.enemyworldcards[i].remain_health,
                                                               self.enemyworldcards[i].present_health),
                                  end='')
                            self.enemyworldcards[i].buff_damage += 1
                            self.enemyworldcards[i].update_buff_damage()
                            self.enemyworldcards[i].remain_health += 1
                            self.enemyworldcards[i].present_health += 1
                            print("{0}-{1}/{2}".format(self.enemyworldcards[i].present_damage,
                                                       self.enemyworldcards[i].remain_health,
                                                       self.enemyworldcards[i].present_health))
                        elif choose == 4:
                            if self.enemyworldcards[i].present_property.find('WindAngry') == -1:
                                print("{0} 获得 风怒".format(self.enemyworldcards[i].name))
                                self.enemyworldcards[i].present_property += ' WindAngry'
                                self.enemyworldcards[i].present_attack_count += 1
                                self.enemyworldcards[i].attack_count = 2
                        elif choose == 5:
                            if self.enemyworldcards[i].present_property.find('Stealth') == -1:
                                print("{0} 获得 潜行".format(self.enemyworldcards[i].name))
                                self.enemyworldcards[i].present_property += ' Stealth'
                        elif choose == 6:
                            if self.enemyworldcards[i].present_property.find('Taunt') == -1:
                                print("{0} 获得 嘲讽".format(self.enemyworldcards[i].name))
                                self.enemyworldcards[i].present_property += ' Taunt'
                    self.enemyworldcards[i].show()

    def over_kill(self, card, myhero, oppohero, myworldcards, oppoworldcards, myhandcards, oppohandcards,
                  mylibrarycards, oppolibrarycards):
        """
        超杀
        :param card: 
        :param myhero: 
        :param oppohero: 
        :param myworldcards: 
        :param oppoworldcards: 
        :param myhandcards: 
        :param oppohandcards: 
        :param mylibrarycards: 
        :param oppolibrarycards: 
        :return: 
        """
        if card.name == '阵线破坏者':
            card.present_damage *= 2

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
        if card.name == '腐烂的苹果树':
            print(">>>{0}->{1} 生命值 {2} -> ".format(card.name, myhero.name, myhero.remain_health), end='')
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
        elif card.name == '霜之哀伤':
            if self.myturn:
                for kill in self.myhero.frostmourne_kill_list:
                    if len(self.myworldcards) < WORLDCARDNUM:
                        kill.reset()
                        print(">>>{0}->{1}".format(card.name, kill.name))
                        self.myworldcards.append(kill)
                self.myhero.frostmourne_kill_list.clear()
            else:
                for kill in self.enemyhero.frostmourne_kill_list:
                    if len(self.enemyworldcards) < WORLDCARDNUM:
                        kill.reset()
                        print(">>>{0}->{1}".format(card.name, kill.name))
                        self.enemyworldcards.append(kill)
                self.enemyhero.frostmourne_kill_list.clear()

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
        self.current_mana -= card.mana
        if card.name == '死亡之翼':
            print("我就是力量的化身！！！")
            for worldcard in self.myworldcards:
                print(">>>{0} 消灭 {1}(我方随从)".format(card.name, worldcard.name))
                worldcard.alive = False
            for worldcard in self.enemyworldcards:
                print(">>>{0} 消灭 {1}(敌方随从)".format(card.name, worldcard.name))
                worldcard.alive = False
            if self.myturn:
                self.myworldcards.append(card)
                self.myhandcards.remove(card)
            else:
                self.enemyworldcards.append(card)
                self.enemyhandcards.remove(card)
            print(">>>>>>{0}({1})".format(card.name, card.mana), end='')
            if card.present_property != '':
                print("[{0}]".format(card.present_property), end='')
            print("上场！！！")
            if self.myturn:
                for handcard in self.myhandcards:
                    print(">>>{0} 弃掉 {1}(我方手牌)".format(card.name, handcard.name))
                self.myhandcards.clear()
            else:
                for handcard in self.enemyhandcards:
                    print(">>>{0} 弃掉 {1}(敌方手牌)".format(card.name, handcard.name))
                self.enemyhandcards.clear()
        elif card.name == '叫嚣的中士':
            world = []
            for worldcard in myworldcards:
                world.append(worldcard)
            if self.myturn:
                for worldcard in oppoworldcards:
                    if worldcard.present_property.find('Stealth') == -1:
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
                    if world[i].present_property != '':
                        print("[{0}]".format(world[i].present_property), end=' ')
                    else:
                        print(end=' ')
                print('')
                if self.myturn:
                    choose_num = choose_object_num(world, "请选择要+2攻的对象序号：")
                else:
                    choose_num = randint(1, len(world))
                print(">>>{0}->{1} 攻击力 {2}->".format(card.name, world[choose_num - 1].name,
                                                     world[choose_num - 1].present_damage),
                      end='')
                world[choose_num - 1].change_damage += 2
                world[choose_num - 1].present_damage += 2
                print("{0}".format(world[choose_num - 1].present_damage))
            if self.myturn:
                if len(self.myworldcards) == 0:
                    self.myworldcards.append(card)
                else:
                    for index, worldcard in enumerate(self.myworldcards):
                        print(" <<{0}>> {1}".format(index, worldcard.name), end='')
                    print(" <<{0}>>".format(len(self.myworldcards)))
                    choose_num = choose_object_num(self.myworldcards, "请选择卡牌要上场位置的序号：")
                    self.myworldcards.insert(choose_num, card)
            else:
                self.enemyworldcards.append(card)
            print(">>>>>>{0}({1})".format(card.name, card.mana), end='')
            if card.present_property != '':
                print("[{0}]".format(card.present_property), end='')
            print("上场！！！")
        elif card.name == '龙骨卫士':
            if self.myturn:
                handcard = self.myhandcards
            else:
                handcard = self.enemyhandcards
            if card_has_dragon(handcard):
                card.buff_damage += 1
                card.update_buff_damage()
                card.present_property = card.present_property + ' Taunt'
            if self.myturn:
                if len(self.myworldcards) == 0:
                    self.myworldcards.append(card)
                else:
                    for index, worldcard in enumerate(self.myworldcards):
                        print(" <<{0}>> {1}".format(index, worldcard.name), end='')
                    print(" <<{0}>>".format(len(self.myworldcards)))
                    choose_num = choose_object_num(self.myworldcards, "请选择卡牌要上场位置的序号：")
                    self.myworldcards.insert(choose_num, card)
            else:
                self.enemyworldcards.append(card)
            print(">>>>>>{0}({1})".format(card.name, card.mana), end='')
            if card.present_property != '':
                print("[{0}]".format(card.present_property), end='')
            print("上场！！！")
        elif card.name == '始生幼龙':
            for worldcard in myworldcards:
                print(">>>{0}->{1}(我方随从) 血量：{2} -> ".format(card.name, worldcard.name, worldcard.remain_health), end='')
                worldcard.reduce_health(2)
                print("{0}".format(worldcard.remain_health))
            for worldcard in oppoworldcards:
                print(">>>{0}->{1}(敌方随从) 血量：{2} -> ".format(card.name, worldcard.name, worldcard.remain_health), end='')
                worldcard.reduce_health(2)
                print("{0}".format(worldcard.remain_health))
            if self.myturn:
                if len(self.myworldcards) == 0:
                    self.myworldcards.append(card)
                else:
                    for index, worldcard in enumerate(self.myworldcards):
                        print(" <<{0}>> {1}".format(index, worldcard.name), end='')
                    print(" <<{0}>>".format(len(self.myworldcards)))
                    choose_num = choose_object_num(self.myworldcards, "请选择卡牌要上场位置的序号：")
                    self.myworldcards.insert(choose_num, card)
            else:
                self.enemyworldcards.append(card)
            print(">>>>>>{0}({1})".format(card.name, card.mana), end='')
            if card.present_property != '':
                print("[{0}]".format(card.present_property), end='')
            print("上场！！！")
        else:
            if self.myturn:
                if len(self.myworldcards) == 0:
                    self.myworldcards.append(card)
                else:
                    for index, worldcard in enumerate(self.myworldcards):
                        print(" <<{0}>> {1}".format(index, worldcard.name), end='')
                    print(" <<{0}>>".format(len(self.myworldcards)))
                    choose_num = choose_object_num(self.myworldcards, "请选择卡牌要上场位置的序号：")
                    self.myworldcards.insert(choose_num, card)
            else:
                self.enemyworldcards.append(card)
            print(">>>>>>{0}({1})".format(card.name, card.mana), end='')
            if card.present_property != '':
                print("[{0}]".format(card.present_property), end='')
            print("上场！！！")
            if card.name == '火羽精灵':
                if len(myhandcards) < HANDCARDNUM:
                    myhandcards.append(Card('', '烈焰元素', 'Element', '', 1, 2, 1, '', 'Follower'))
            elif card.name == '穆克拉':
                banana = Card('', '香蕉', '', '', '', '', 1, '', 'Magic', True)
                if len(oppohandcards) < HANDCARDNUM - 1:
                    oppohandcards.append(banana)
                    oppohandcards.append(banana)
                elif len(oppohandcards) == HANDCARDNUM - 1:
                    oppohandcards.append(banana)
            elif card.name == '石丘防御者':
                choose_followers = random.sample(taunt_cards(), 3)
                for i in range(len(choose_followers)):
                    print("{0}-{1}({2}-{3}".format(i + 1, choose_followers[i].name, choose_followers[i].present_damage,
                                                   choose_followers[i].remain_health), end='')
                    if choose_followers[i].armor > 0:
                        print("[{0}]".format(choose_followers[i].armor), end='')
                    print("/{0})".format(choose_followers[i].present_health), end='')
                    if choose_followers[i].present_property != '':
                        print("[{0}]".format(choose_followers[i].present_property), end=' ')
                    else:
                        print(end=' ')
                print('')
                if self.myturn:
                    choose_num = choose_object_num(choose_followers, "请选择要发现的对象序号：")
                else:
                    choose_num = randint(1, len(choose_followers))
                print(">>>{0} 发现 {1}".format(card.name, choose_followers[choose_num - 1].name))
                if len(myhandcards) < HANDCARDNUM:
                    myhandcards.append(choose_followers[choose_num - 1])
            elif card.name == '火车王里诺艾':
                if len(oppoworldcards) < WORLDCARDNUM - 1:
                    oppoworldcards.append(Card('', '雏龙', 'Dragon', '', 1, 1, 1, '', 'Follower'))
                    oppoworldcards.append(Card('', '雏龙', 'Dragon', '', 1, 1, 1, '', 'Follower'))
                elif len(oppoworldcards) == WORLDCARDNUM - 1:
                    oppoworldcards.append(Card('', '雏龙', 'Dragon', '', 1, 1, 1, '', 'Follower'))
            elif card.name == '王牌猎人':
                if self.myturn:
                    world = self.enemyworldcards
                else:
                    world = self.myworldcards
                if CardDamage(world, 4, 7, False):
                    for i in range(len(world)):
                        print("{0}-{1}({2}-{3}".format(i + 1, world[i].name, world[i].present_damage,
                                                       world[i].remain_health), end='')
                        if world[i].armor > 0:
                            print("[{0}]".format(world[i].armor), end='')
                        print("/{0})".format(world[i].present_health), end='')
                        if world[i].present_property != '':
                            print("[{0}]".format(world[i].present_property), end=' ')
                        else:
                            print(end=' ')
                    print('')
                    while True:
                        if self.myturn:
                            choose_num = choose_object_num(world, "请选择要消灭的对象（攻击力大于等于7）序号：")
                        else:
                            choose_num = randint(1, len(world))
                        if world[choose_num - 1].present_damage >= 7 and world[choose_num - 1].present_property.find(
                                'Stealth') == -1:
                            break
                    print(">>>{0} 消灭了 {1}".format(card.name, world[choose_num - 1].name))
                    world.remove(world[choose_num - 1])
            elif card.name == '狂奔的科多兽':
                if self.myturn:
                    world = self.enemyworldcards
                else:
                    world = self.myworldcards
                if CardDamage(world, 5, 2, True):
                    for i in range(len(world)):
                        print("{0}-{1}({2}-{3}".format(i + 1, world[i].name, world[i].present_damage,
                                                       world[i].remain_health), end='')
                        if world[i].armor > 0:
                            print("[{0}]".format(world[i].armor), end='')
                        print("/{0})".format(world[i].present_health), end='')
                        if world[i].present_property != '':
                            print("[{0}]".format(world[i].present_property), end=' ')
                        else:
                            print(end=' ')
                    print('')
                    while True:
                        choose_num = randint(1, len(world))
                        if world[choose_num - 1].present_damage <= 2:
                            break
                    print(">>>{0} 消灭了 {1}".format(card.name, world[choose_num - 1].name))
                    world.remove(world[choose_num - 1])
            elif card.name == '黑骑士':
                if self.myturn:
                    world = self.enemyworldcards
                else:
                    world = self.myworldcards
                if card_has_taunt(world, False):
                    for i in range(len(world)):
                        print("{0}-{1}({2}-{3}".format(i + 1, world[i].name, world[i].present_damage,
                                                       world[i].remain_health), end='')
                        if world[i].armor > 0:
                            print("[{0}]".format(world[i].armor), end='')
                        print("/{0})".format(world[i].present_health), end='')
                        if world[i].present_property != '':
                            print("[{0}]".format(world[i].present_property), end=' ')
                        else:
                            print(end=' ')
                    print('')
                    while True:
                        if self.myturn:
                            choose_num = choose_object_num(world, "请选择要消灭的对象（嘲讽）序号：")
                        else:
                            choose_num = randint(1, len(world))
                        if world[choose_num - 1].present_property.find('Taunt') != -1 and world[
                                    choose_num - 1].present_property.find('Stealth') == -1:
                            break
                    print(">>>{0} 消灭了 {1}".format(card.name, world[choose_num - 1].name))
                    world.remove(world[choose_num - 1])
            elif card.name == '阿莱克斯塔萨':
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
                    print(">>>{0}->{1} 血量：{2} -> ".format(card.name, self.myhero.name, self.myhero.remain_health),
                          end='')
                    self.myhero.remain_health = 15
                    print("{0}".format(self.myhero.remain_health))
                else:
                    print(">>>{0}->{1} 血量：{2} -> ".format(card.name, self.enemyhero.name, self.enemyhero.remain_health),
                          end='')
                    self.enemyhero.remain_health = 15
                    print("{0}".format(self.enemyhero.remain_health))
            elif card.name == '欧克哈特大师':
                if self.myturn:
                    DamageOne = DamageEqualList(self.mycards, 1)
                    DamageTwo = DamageEqualList(self.mycards, 2)
                    DamageThree = DamageEqualList(self.mycards, 3)
                    if len(DamageOne) > 0 and len(self.myworldcards) < WORLDCARDNUM:
                        randnum = randint(0, len(DamageOne) - 1)
                        self.mycards.remove(DamageOne[randnum])
                        self.myworldcards.append(DamageOne[randnum])
                        print(">>>{0}->{1}({2})".format(card.name, DamageOne[randnum].name, DamageOne[randnum].mana),
                              end='')
                        if DamageOne[randnum].present_property != '':
                            print("[{0}]".format(DamageOne[randnum].present_property), end='')
                        print("上场！！！")
                    if len(DamageTwo) > 0 and len(self.myworldcards) < WORLDCARDNUM:
                        randnum = randint(0, len(DamageTwo) - 1)
                        self.mycards.remove(DamageTwo[randnum])
                        self.myworldcards.append(DamageTwo[randnum])
                        print(">>>{0}->{1}({2})".format(card.name, DamageTwo[randnum].name, DamageTwo[randnum].mana),
                              end='')
                        if DamageTwo[randnum].present_property != '':
                            print("[{0}]".format(DamageTwo[randnum].present_property), end='')
                        print("上场！！！")
                    if len(DamageThree) > 0 and len(self.myworldcards) < WORLDCARDNUM:
                        randnum = randint(0, len(DamageThree) - 1)
                        self.mycards.remove(DamageThree[randnum])
                        self.myworldcards.append(DamageThree[randnum])
                        print(
                            ">>>{0}->{1}({2})".format(card.name, DamageThree[randnum].name, DamageThree[randnum].mana),
                            end='')
                        if DamageThree[randnum].present_property != '':
                            print("[{0}]".format(DamageThree[randnum].present_property), end='')
                        print("上场！！！")
                else:
                    DamageOne = DamageEqualList(self.enemycards, 1)
                    DamageTwo = DamageEqualList(self.enemycards, 2)
                    DamageThree = DamageEqualList(self.enemycards, 3)
                    if len(DamageOne) > 0 and len(self.enemyworldcards) < WORLDCARDNUM:
                        randnum = randint(0, len(DamageOne) - 1)
                        self.enemycards.remove(DamageOne[randnum])
                        self.enemyworldcards.append(DamageOne[randnum])
                        print(">>>{0}->{1}({2})".format(card.name, DamageOne[randnum].name, DamageOne[randnum].mana),
                              end='')
                        if DamageOne[randnum].present_property != '':
                            print("[{0}]".format(DamageOne[randnum].present_property), end='')
                        print("上场！！！")
                    if len(DamageTwo) > 0 and len(self.enemyworldcards) < WORLDCARDNUM:
                        randnum = randint(0, len(DamageTwo) - 1)
                        self.enemycards.remove(DamageTwo[randnum])
                        self.enemyworldcards.append(DamageTwo[randnum])
                        print(">>>{0}->{1}({2})".format(card.name, DamageTwo[randnum].name, DamageTwo[randnum].mana),
                              end='')
                        if DamageTwo[randnum].present_property != '':
                            print("[{0}]".format(DamageTwo[randnum].present_property), end='')
                        print("上场！！！")
                    if len(DamageThree) > 0 and len(self.enemyworldcards) < WORLDCARDNUM:
                        randnum = randint(0, len(DamageThree) - 1)
                        self.enemycards.remove(DamageThree[randnum])
                        self.enemyworldcards.append(DamageThree[randnum])
                        print(
                            ">>>{0}->{1}({2})".format(card.name, DamageThree[randnum].name, DamageThree[randnum].mana),
                            end='')
                        if DamageThree[randnum].present_property != '':
                            print("[{0}]".format(DamageThree[randnum].present_property), end='')
                        print("上场！！！")
            elif card.name == '游荡恶鬼':
                for i in range(len(self.myhandcards) - 1, -1, -1):
                    if self.myhandcards[i].mana == 1 and self.myhandcards[i].type == 'Magic':
                        print(">>>{0} 摧毁 {1}(我方手牌)".format(card.name, self.myhandcards[i].name))
                        self.myhandcards.remove(self.myhandcards[i])
                for i in range(len(self.enemyhandcards) - 1, -1, -1):
                    if self.enemyhandcards[i].mana == 1 and self.enemyhandcards[i].type == 'Magic':
                        print(">>>{0} 摧毁 {1}(敌方手牌)".format(card.name, self.enemyhandcards[i].name))
                        self.enemyhandcards.remove(self.enemyhandcards[i])
                for i in range(len(self.mycards) - 1, -1, -1):
                    if self.mycards[i].mana == 1 and self.mycards[i].type == 'Magic':
                        print(">>>{0} 摧毁 {1}(我方牌库)".format(card.name, self.mycards[i].name))
                        self.mycards.remove(self.mycards[i])
                for i in range(len(self.enemycards) - 1, -1, -1):
                    if self.enemycards[i].mana == 1 and self.enemycards[i].type == 'Magic':
                        print(">>>{0} 摧毁 {1}(敌方牌库)".format(card.name, self.enemycards[i].name))
                        self.enemycards.remove(self.enemycards[i])

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
            for worldcard in myworldcards:
                if worldcard.present_property.find('AntiMagic') == -1:
                    world.append(worldcard)
            if self.myturn:
                for worldcard in oppoworldcards:
                    if worldcard.present_property.find('Stealth') == -1 and worldcard.present_property.find(
                            'AntiMagic') == -1:
                        world.append(worldcard)
            if len(world) == 0:
                return False
            else:
                for i in range(len(world)):
                    print("{0}-{1}({2}-{3}".format(i + 1, world[i].name, world[i].present_damage,
                                                   world[i].remain_health), end='')
                    if world[i].armor > 0:
                        print("[{0}]".format(world[i].armor), end='')
                    print("/{0})".format(world[i].present_health), end='')
                    if world[i].present_property != '':
                        print("[{0}]".format(world[i].present_property), end=' ')
                    else:
                        print(end=' ')
                print('')
                if self.myturn:
                    choose_num = choose_direct_num(world, "请选择对象序号：")
                else:
                    choose_num = randint(1, len(world))
                print("使用 {0}->{1} {2}-{3} >>> ".format(card.name, world[choose_num - 1].name,
                                                        world[choose_num - 1].present_damage,
                                                        world[choose_num - 1].remain_health),
                      end='')
                world[choose_num - 1].buff_damage += 1
                world[choose_num - 1].update_buff_damage()
                world[choose_num - 1].remain_health += 1
                world[choose_num - 1].present_health += 1
                print("{0}-{1}".format(world[choose_num - 1].present_damage, world[choose_num - 1].remain_health))
                return True
        elif card.name == '死亡缠绕':
            if self.myturn:
                mysite = [self.myhero]
                for worldcard in self.myworldcards:
                    if worldcard.present_property.find('AntiMagic') == -1:
                        mysite.append(worldcard)
                opposite = [self.enemyhero]
                for worldcard in self.enemyworldcards:
                    if worldcard.present_property.find('AntiMagic') == -1 and worldcard.present_property.find(
                            'Stealth') == -1:
                        opposite.append(worldcard)
                print("1.我方角色 2.敌方角色")
                choose_charater = input_int("请选择角色的序号：")
            else:
                mysite = [self.enemyhero]
                for worldcard in self.enemyworldcards:
                    if worldcard.present_property.find('AntiMagic') == -1:
                        mysite.append(worldcard)
                opposite = [self.myhero]
                for worldcard in self.myworldcards:
                    if worldcard.present_property.find('AntiMagic') == -1 and worldcard.present_property.find(
                            'Stealth') == -1:
                        opposite.append(worldcard)
                choose_charater = randint(1, 2)
            if choose_charater == 1:
                for i in range(len(mysite)):
                    print("{0}-{1}({2}-{3}".format(i + 1, mysite[i].name, mysite[i].present_damage,
                                                   mysite[i].remain_health), end='')
                    if mysite[i].armor > 0:
                        print("[{0}]".format(mysite[i].armor), end='')
                    print("/{0})".format(mysite[i].present_health), end='')
                    if mysite[i].present_property != '':
                        print("[{0}]".format(mysite[i].present_property), end=' ')
                    else:
                        print(end=' ')
                print('')
                if self.myturn:
                    choose_num = choose_direct_num(mysite, "请选择对象序号：")
                else:
                    choose_num = randint(1, len(mysite))
                print(">>>{0}->{1} 生命值 {2}->".format(card.name, mysite[choose_num - 1].name,
                                                     mysite[choose_num - 1].remain_health), end='')
                mysite[choose_num - 1].add_health(5)
                print("{0}".format(mysite[choose_num - 1].remain_health))
            else:
                for i in range(len(opposite)):
                    print("{0}-{1}({2}-{3}".format(i + 1, opposite[i].name, opposite[i].present_damage,
                                                   opposite[i].remain_health), end='')
                    if opposite[i].armor > 0:
                        print("[{0}]".format(opposite[i].armor), end='')
                    print("/{0})".format(opposite[i].present_health), end='')
                    if opposite[i].present_property != '':
                        print("[{0}]".format(opposite[i].present_property), end=' ')
                    else:
                        print(end=' ')
                print('')
                if self.myturn:
                    choose_num = choose_direct_num(opposite, "请选择对象序号：")
                else:
                    choose_num = randint(1, len(opposite))
                print(">>>{0}->{1} 生命值 {2}->".format(card.name, opposite[choose_num - 1].name,
                                                     opposite[choose_num - 1].remain_health), end='')
                opposite[choose_num - 1].reduce_health(5)
                print("{0}".format(opposite[choose_num - 1].remain_health))
            return True
        elif card.name == '死亡之握':
            if self.myturn:
                follower_list = follower_cards(self.enemycards)
                if len(follower_list) != 0:
                    random_num = randint(0, len(follower_list) - 1)
                    print(">>>{0} -> {1}".format(card.name, follower_list[random_num]))
                    self.myhandcards.append(follower_list[random_num])
                    self.enemycards.remove(follower_list[random_num])
            else:
                follower_list = follower_cards(self.mycards)
                if len(follower_list) != 0:
                    random_num = randint(0, len(follower_list) - 1)
                    print(">>>{0} -> {1}".format(card.name, follower_list[random_num].name))
                    self.enemyhandcards.append(follower_list[random_num])
                    self.mycards.remove(follower_list[random_num])
            return True
        elif card.name == '湮灭':
            if self.myturn:
                world = []
                for worldcard in self.enemyworldcards:
                    if worldcard.present_property.find('AntiMagic') == -1 and worldcard.present_property.find(
                            'Stealth') == -1:
                        world.append(worldcard)
            else:
                world = []
                for worldcard in self.myworldcards:
                    if worldcard.present_property.find('AntiMagic') == -1 and worldcard.present_property.find(
                            'Stealth') == -1:
                        world.append(worldcard)
            if len(world) == 0:
                return False
            else:
                for i in range(len(world)):
                    print("{0}-{1}({2}-{3}".format(i + 1, world[i].name, world[i].present_damage,
                                                   world[i].remain_health), end='')
                    if world[i].armor > 0:
                        print("[{0}]".format(world[i].armor), end='')
                    print("/{0})".format(world[i].present_health), end='')
                    if world[i].present_property != '':
                        print("[{0}]".format(world[i].present_property), end=' ')
                    else:
                        print(end=' ')
                print('')
                if self.myturn:
                    choose_num = choose_direct_num(world, "请选择要消灭的对象序号：")
                else:
                    choose_num = randint(1, len(world))
                print(">>>{0} 消灭了 {1}".format(card.name, world[choose_num - 1].name))
                world[choose_num - 1].alive = False
                if self.myturn:
                    print(">>>{0}->{1} 生命值 {2}".format(card.name, self.myhero.name, self.myhero.remain_health), end='')
                    if self.myhero.armor > 0:
                        print("[{0}]".format(self.myhero.armor), end='')
                    self.myhero.reduce_health(world[choose_num - 1].remain_health)
                    print("->{0}".format(self.myhero.remain_health), end='')
                    if self.myhero.armor > 0:
                        print("[{0}]".format(self.myhero.armor), end='')
                    print("")
                else:
                    print(">>>{0}->{1} 生命值 {2}".format(card.name, self.enemyhero.name, self.enemyhero.remain_health),
                          end='')
                    if self.enemyhero.armor > 0:
                        print("[{0}]".format(self.enemyhero.armor), end='')
                    self.enemyhero.reduce_health(world[choose_num - 1].remain_health)
                    print("->{0}".format(self.enemyhero.remain_health), end='')
                    if self.enemyhero.armor > 0:
                        print("[{0}]".format(self.enemyhero.armor), end='')
                    print("")
                return True
        elif card.name == '枯萎凋零':
            if self.myturn:
                print(">>>{0}->{1} 生命值 {2}".format(card.name, self.enemyhero.name, self.enemyhero.remain_health),
                      end='')
                if self.enemyhero.armor > 0:
                    print("[{0}]".format(self.enemyhero.armor), end='')
                self.enemyhero.reduce_health(3)
                print("->{0}".format(self.enemyhero.remain_health), end='')
                if self.enemyhero.armor > 0:
                    print("[{0}]".format(self.enemyhero.armor), end='')
                print("")
                for worldcard in self.enemyworldcards:
                    print(">>>{0}->{1} 生命值 {2}".format(card.name, worldcard.name, worldcard.remain_health),
                          end='')
                    worldcard.reduce_health(3)
                    print("->{0}".format(worldcard.remain_health))
            else:
                print(">>>{0}->{1} 生命值 {2}".format(card.name, self.myhero.name, self.myhero.remain_health), end='')
                if self.myhero.armor > 0:
                    print("[{0}]".format(self.myhero.armor), end='')
                self.myhero.reduce_health(3)
                print("->{0}".format(self.myhero.remain_health), end='')
                if self.myhero.armor > 0:
                    print("[{0}]".format(self.myhero.armor), end='')
                print("")
                for worldcard in self.myworldcards:
                    print(">>>{0}->{1} 生命值 {2}".format(card.name, worldcard.name, worldcard.remain_health), end='')
                    worldcard.reduce_health(3)
                    print("->{0}".format(worldcard.remain_health))
            return True
        elif card.name == '反魔法护罩':
            if self.myturn:
                for worldcard in self.myworldcards:
                    print(">>>{0}->{1} {2}-{3}/{4}->".format(card.name, worldcard.name, worldcard.present_damage,
                                                             worldcard.remain_health, worldcard.present_health), end='')
                    worldcard.buff_damage += 2
                    worldcard.update_buff_damage()
                    worldcard.present_health += 2
                    worldcard.remain_health += 2
                    print("{0}-{1}/{2}".format(worldcard.present_damage, worldcard.remain_health,
                                               worldcard.present_health))
                    if worldcard.present_property == '':
                        worldcard.present_property += 'AntiMagic'
                    elif worldcard.present_property.find('AntiMagic') == -1:
                        worldcard.present_property += ' AntiMagic'
            else:
                for worldcard in self.enemyworldcards:
                    print(">>>{0}->{1} {2}-{3}/{4}->".format(card.name, worldcard.name, worldcard.present_damage,
                                                             worldcard.remain_health, worldcard.present_health), end='')
                    worldcard.buff_damage += 2
                    worldcard.update_buff_damage()
                    worldcard.present_health += 2
                    worldcard.remain_health += 2
                    print("{0}-{1}/{2}".format(worldcard.present_damage, worldcard.remain_health,
                                               worldcard.present_health))
                    if worldcard.present_property == '':
                        worldcard.present_property += 'AntiMagic'
                    elif worldcard.present_property.find('AntiMagic') == -1:
                        worldcard.present_property += ' AntiMagic'
            return True
        elif card.name == '末日契约':
            count = len(self.myworldcards) + len(self.enemyworldcards)
            for worldcard in self.myworldcards:
                print(">>>{0} 消灭 {1}(我方随从)".format(card.name, worldcard.name))
                worldcard.alive = False
            for worldcard in self.enemyworldcards:
                print(">>>{0} 消灭 {1}(敌方随从)".format(card.name, worldcard.name))
                worldcard.alive = False
            while count > 0:
                if len(mylibrarycards) > 0:
                    print(">>>{0} 移除 {1}".format(card.name, mylibrarycards[0].name))
                    mylibrarycards.remove(mylibrarycards[0])
                    count -= 1
                else:
                    break
            return True
        elif card.name == '亡者大军':
            count = 5
            while count > 0:
                if len(mylibrarycards) > 0:
                    print(">>>{0}->{1} ".format(card.name, mylibrarycards[0].name), end='')
                    if mylibrarycards[0].type == 'Follower':
                        if len(myworldcards) < WORLDCARDNUM:
                            print("进入战场")
                            myworldcards.append(mylibrarycards[0])
                        else:
                            print("被弃掉")
                    else:
                        print("被弃掉")
                    mylibrarycards.remove(mylibrarycards[0])
                    count -= 1
                else:
                    break
            return True

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
                if self.enemyhandcards[index].type == 'Follower':
                    if len(self.enemyworldcards) < WORLDCARDNUM:
                        if self.enemyhandcards[index].present_property.find('Battlecry') != -1:
                            self.battle_cry(self.enemyhandcards[index], self.enemyhero, self.myhero,
                                            self.enemyworldcards, self.myworldcards, self.enemyhandcards,
                                            self.myhandcards, self.enemycards, self.mycards)
                        else:
                            self.enemyworldcards.append(self.enemyhandcards[index])
                            print(">>>>>>{0}-{1}({2})".format(
                                index + 1, self.enemyhandcards[index].name,
                                self.enemyhandcards[index].mana),
                                end='')
                            if self.enemyhandcards[index].present_property != '':
                                print("[{0}]".format(self.enemyhandcards[index].present_property), end='')
                            print("上场！！！")
                            self.current_mana -= self.enemyhandcards[index].mana
                    else:
                        print("场上随从已满，随从无法上场！")
                        break
                elif self.enemyhandcards[index].type == 'Magic':
                    if self.cast(self.enemyhandcards[index], self.enemyhero, self.myhero,
                                 self.enemyworldcards, self.myworldcards, self.enemyhandcards, self.myhandcards,
                                 self.enemycards, self.mycards):
                        self.current_mana -= self.enemyhandcards[index].mana
                    else:
                        break
                elif self.enemyhandcards[index].type == 'Weapon':
                    if self.enemyweapon is not None:
                        self.enemyweapon.alive = False
                        self.update_weapon()
                    self.enemyweapon = self.enemyhandcards[index]
                    print(">>>装备 {0}".format(self.enemyweapon.name))
                    self.current_mana -= self.enemyhandcards[index].mana
                try:
                    if self.enemyhandcards[index] in self.enemyhandcards:
                        self.enemyhandcards.remove(self.enemyhandcards[index])
                except Exception as e:
                    print(e)
                index = -1
                select = -1

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
            if card_has_taunt(cards, False):
                if cards[card_id].present_property.find('Taunt') != -1:
                    return card_id
                else:
                    return self.attack_who(cards)
            elif card_has_stealth(cards):
                if cards[card_id].present_property.find('Stealth') == -1:
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
