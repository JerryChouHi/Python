# encoding:utf-8
# @Time     : 2019/6/18 19:30
# @Author   : Jerry Chou
# @File     : main.py
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
#             35.格鲁尔：每个回合结束时，获得+1/+1
#                海巨人：战场上每有一个其他随从，该牌的法力值消耗就减少1点
#             36.乌达斯塔：突袭、超杀--从你的手牌中召唤一个野兽
#                恩佐斯：战吼--召唤所有你在本局对战中死亡的，并具有亡语的随从
#             37.伊瑟拉：在你的回合结束时,随机将一张梦境牌置入你的手牌
#                根据卡牌id从卡牌库中获取卡牌信息来生成卡牌对象
#             38.老狐狸马林：战吼--为你的对手召唤一个0/8的宝箱。
#                大师宝箱：亡语--使你的对手获得一份惊人的战利品
#             39.森林狼：你的其他野兽获得+1攻击力
#                魔泉山猫：突袭、战吼--将一张1/1并具有突袭的山猫置入你的手牌
#                闪光蝴蝶：亡语--随机将一张猎人法术牌置入你的手牌
#                追踪术：检视你的牌库顶的三张牌，将其中一张置入你的手牌，弃掉其余牌
#                食腐土狼：每当一个友方野兽死亡时，便获得+2/+1
#                致命射击：随机消灭一个敌方随从
#                关门放狗：战场上每有一个敌方随从，便召唤一个1/1并具有冲锋的猎犬
#                杀戮命令：造成3点伤害，如果你控制一个野兽，则改为造成5点伤害
#                动物伙伴：随机召唤一个野兽伙伴
#                主人的召唤：从你的牌库中发现一张随从牌。如果三张牌都是野兽牌，则改为抽取全部三张牌
#                凶猛狂暴：使一个野兽获得+3/+3，将它的三个复制洗入你的牌库，且这个复制都具有+3/+3
#                标记射击：对一个随从造成4点伤害。发现一张法术牌
#                苔原犀牛：你的野兽获得冲锋
#                猛兽出笼：双生法术--召唤一个5/5并具有突袭的双足飞龙
#                祖尔金：战吼--释放你本局对战中使用过的所有法术（目标随机而定）
#             40.优化电脑AI
#                主人的召唤抽取不重复的随从

from generate_cards import *
from parse import parse_card
from fight import *
from random import randint
import random
from common import *
from card_collection import *

INIT_HAND_COUNT = 3
HANDCARDNUM = 10
WORLDCARDNUM = 7
MANANUM = 10


class World:
    def __init__(self):
        self.mana = 1
        self.myworldcards = []
        self.enemyworldcards = []
        self.myhero = parse_card(
            get_card_info('card_pool.txt', int(get_card_info('cards_my.txt', 1).strip('\n'))).strip('\n'))
        self.myhero.hero = 'myhero'
        self.myweapon = None
        self.my_death_follower_id = []
        self.mydeathfollower = []
        self.enemyhero = parse_card(
            get_card_info('card_pool.txt', int(get_card_info('cards_enemy.txt', 1).strip('\n'))).strip('\n'))
        self.enemyhero.hero = 'enemyhero'
        self.enemyweapon = None
        self.enemy_death_follower_id = []
        self.enemydeathfollower = []
        print("**************我的卡牌**************")
        self.mycards = generate_mycards()
        for card in self.mycards:
            if card.type == 'Follower':
                card.hero = 'myhero'
        show_cards(self.mycards)
        print("**************敌方卡牌**************")
        self.enemycards = generate_enemycards()
        for card in self.enemycards:
            if card.type == 'Follower':
                card.hero = 'enemyhero'
        show_cards(self.enemycards)
        self.round = 1

    def who_first(self):
        if randint(0, 1) == 0:
            self.myturn = True
            self.myhandcards = self.mycards[:INIT_HAND_COUNT]
            for i in range(INIT_HAND_COUNT):
                self.mycards.remove(self.mycards[0])
            self.enemyhandcards = self.enemycards[:INIT_HAND_COUNT + 1]
            self.enemyhandcards.append(parse_card(get_card_info('card_pool.txt', 1137).strip('\n')))
            for i in range(INIT_HAND_COUNT + 1):
                self.enemycards.remove(self.enemycards[0])
        else:
            self.myturn = False
            self.myhandcards = self.mycards[:INIT_HAND_COUNT + 1]
            self.myhandcards.append(parse_card(get_card_info('card_pool.txt', 1137).strip('\n')))
            for i in range(INIT_HAND_COUNT + 1):
                self.mycards.remove(self.mycards[0])
            self.enemyhandcards = self.enemycards[:INIT_HAND_COUNT]
            for i in range(INIT_HAND_COUNT):
                self.enemycards.remove(self.enemycards[0])

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
        for card in self.myworldcards:
            if card.present_property.find('EveryRoundEnd') != -1:
                print("------> 每个回合结束触发 <------")
                if card.name == '格鲁尔':
                    print(">>>{0} {1}-{2}/{3} -> ".format(card.name, card.present_damage, card.remain_health,
                                                          card.present_health), end='')
                    card.present_health += 1
                    card.remain_health += 1
                    card.present_damage += 1
                    print("{0}-{1}/{2}".format(card.present_damage, card.remain_health, card.present_health))
        for card in self.enemyworldcards:
            if card.present_property.find('EveryRoundEnd') != -1:
                print("------> 每个回合结束触发 <------")
                if card.name == '格鲁尔':
                    print(">>>{0} {1}-{2}/{3} -> ".format(card.name, card.present_damage, card.remain_health,
                                                          card.present_health), end='')
                    card.present_health += 1
                    card.remain_health += 1
                    card.present_damage += 1
                    print("{0}-{1}/{2}".format(card.present_damage, card.remain_health, card.present_health))
        if self.myturn:
            for card in self.myworldcards:
                if card.present_property.find('MyRoundEnd') != -1:
                    print("------> 你的回合结束触发 <------")
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
                    elif card.name == '伊瑟拉':
                        if len(self.myhandcards) < HANDCARDNUM:
                            ysera_card = ysera_cards()
                            self.myhandcards.append(ysera_card)
                            print(">>>{0}->{1}".format(card.name, ysera_card.name))
        else:
            for card in self.enemyworldcards:
                if card.present_property.find('MyRoundEnd') != -1:
                    print("------> 你的回合结束触发 <------")
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
                    elif card.name == '伊瑟拉':
                        if len(self.enemyhandcards) < HANDCARDNUM:
                            ysera_card = ysera_cards()
                            self.enemyhandcards.append(ysera_card)
                            print(">>>{0}->{1}".format(card.name, ysera_card.name))

    def round_begin(self):
        """
        回合开始触发效果
        :return: 
        """
        if self.myturn:
            self.myhero.use_skill = False
            for card in self.myworldcards:
                if card.present_property.find('MyRoundBegin') != -1:
                    print("------> 回合开始触发 <------")
                    if card.name == '治疗图腾':
                        print("{0}：己方在场卡牌群体治疗+1".format(card.name))
                        for card in self.myworldcards:
                            card.add_health(1)
                    elif card.name == '梦魇之龙':
                        card.present_damage *= 2
                elif card.present_property.find('MyNightmare') != -1:
                    print(">>> 梦魇->{0} 死亡".format(card.name))
                    card.alive = False
            for card in self.enemyworldcards:
                if card.present_property.find('MyNightmare') != -1:
                    print(">>> 梦魇->{0} 死亡".format(card.name))
                    card.alive = False
        else:
            self.enemyhero.use_skill = False
            for card in self.enemyworldcards:
                if card.present_property.find('MyRoundBegin') != -1:
                    print("------> 回合开始触发 <------")
                    if card.name == '治疗图腾':
                        print("{0}：己方在场卡牌群体治疗+1".format(card.name))
                        for card in self.enemyworldcards:
                            card.add_health(1)
                    elif card.name == '梦魇之龙':
                        card.present_damage *= 2
                elif card.present_property.find('EnemyNightmare') != -1:
                    print(">>> 梦魇->{0} 死亡".format(card.name))
                    card.alive = False
            for card in self.myworldcards:
                if card.present_property.find('EnemyNightmare') != -1:
                    print(">>> 梦魇->{0} 死亡".format(card.name))
                    card.alive = False
        self.update_world_card()

    def can_use_skill(self):
        """
        判断是否可以使用英雄技能
        :return: 
        """
        can_use = False
        if self.myturn:
            if self.myhero.name == '乌瑟尔':
                if len(self.myworldcards) < WORLDCARDNUM and self.myhero.use_skill == False and self.current_mana >= 2:
                    can_use = True
            elif self.myhero.name == '萨尔':
                if len(self.myworldcards) < WORLDCARDNUM and len(
                        self.myhero.totem) > 0 and self.myhero.use_skill == False and self.current_mana >= 2:
                    can_use = True
            else:
                if self.myhero.use_skill == False and self.current_mana >= 2:
                    can_use = True
        else:
            if self.enemyhero.name == '乌瑟尔':
                if len(
                        self.enemyworldcards) < WORLDCARDNUM and self.enemyhero.use_skill == False and self.current_mana >= 2:
                    can_use = True
            elif self.enemyhero.name == '萨尔':
                if len(self.enemyworldcards) < WORLDCARDNUM and len(
                        self.enemyhero.totem) > 0 and self.enemyhero.use_skill == False and self.current_mana >= 2:
                    can_use = True
            elif self.enemyhero.name == '安度因':
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

    def card_can_use(self, card, myhero, oppohero, myworldcards, oppoworldcards, myhandcards, oppohandcards,
                     mylibrarycards, oppolibrarycards, myweapon, oppoweapon):
        """
        卡牌是否可用
        :param card: 
        :return: 
        """
        can_use = False
        if card.type == 'Follower':
            if card.present_mana <= self.current_mana and len(myworldcards) < WORLDCARDNUM:
                can_use = True
        elif card.type == 'Magic':
            if (card.SpecialMagic.find('CreateFollower') != -1 and len(
                    myworldcards) < WORLDCARDNUM) or card.SpecialMagic.find('CreateFollower') == -1:
                if card.SpecialMagic.find('MyFollowerDirect') != -1 and card.present_mana <= self.current_mana:
                    for worldcard in myworldcards:
                        if worldcard.present_property.find('AntiMagic') == -1:
                            can_use = True
                            break
                elif card.SpecialMagic.find('EnemyFollowerDirect') != -1 and card.present_mana <= self.current_mana:
                    for worldcard in oppoworldcards:
                        if worldcard.present_property.find('AntiMagic') == -1 and worldcard.present_property.find(
                                'Stealth') == -1:
                            if card.name == '湮灭':
                                if myhero.remain_health + myhero.armor > worldcard.remain_health:
                                    can_use = True
                                    break
                            else:
                                can_use = True
                                break
                elif card.SpecialMagic.find('MyFollowerBeastDirect') != -1 and card.present_mana <= self.current_mana:
                    for worldcard in myworldcards:
                        if worldcard.present_property.find('AntiMagic') == -1 and worldcard.race == 'Beast':
                            can_use = True
                            break
                elif card.SpecialMagic.find(
                        'EnemyFollowerBeastDirect') != -1 and card.present_mana <= self.current_mana:
                    for worldcard in oppoworldcards:
                        if worldcard.present_property.find('AntiMagic') == -1 and worldcard.present_property.find(
                                'Stealth') == -1 and worldcard.race == 'Beast':
                            can_use = True
                            break
                elif card.SpecialMagic.find('NeedEnemyFollower') != -1 and card.present_mana <= self.current_mana:
                    if len(oppoworldcards) > 0:
                        can_use = True
                else:
                    if card.present_mana <= self.current_mana:
                        can_use = True
        else:
            if card.present_mana <= self.current_mana:
                can_use = True
        return can_use

    def can_use_handcard(self, myhero, oppohero, myworldcards, oppoworldcards, myhandcards, oppohandcards,
                         mylibrarycards, oppolibrarycards, myweapon, oppoweapon):
        """
        可用卡牌列表
        :return: 
        """
        can_use_list = []
        for card in myhandcards:
            if self.card_can_use(card, myhero, oppohero, myworldcards, oppoworldcards, myhandcards, oppohandcards,
                                 mylibrarycards, oppolibrarycards, myweapon, oppoweapon):
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

    def card_can_attack(self, card, attack_hero):
        """
        卡牌是否可以攻击
        :param attack_hero:  True 攻击英雄  False 攻击随从
        :param card: 
        :return: 
        """
        can_attack = False
        if self.myturn:
            if attack_hero:
                if (card.present_property.find(
                        'Charge') != -1 and card.present_attack_count > 0 and card.present_damage > 0) or (
                                            card.present_property.find('Rush') == -1 and card.present_property.find(
                                        'Charge') == -1 and card.present_attack_count > 0 and card.sleep == False and card.present_damage > 0) and search_for_property(
                    self.enemyworldcards, 'Taunt', 2, True):
                    can_attack = True
            else:
                if card.present_property.find('Rush') != -1 and card.present_property.find('Charge') == -1:
                    if card.present_attack_count > 0 and card.present_damage > 0 \
                            and search_for_property(self.enemyworldcards, 'Stealth', 2, True) and len(
                        self.enemyworldcards) > 0:
                        can_attack = True
                else:
                    if card.present_attack_count > 0 and card.sleep == False and card.present_damage > 0 and search_for_property(
                            self.enemyworldcards, 'Stealth', 2, True):
                        can_attack = True
        else:
            if attack_hero:
                if ((card.present_property.find(
                        'Charge') != -1 and card.present_attack_count > 0 and card.present_damage > 0) or (
                                            card.present_property.find('Rush') == -1 and card.present_property.find(
                                        'Charge') == -1 and card.present_attack_count > 0 and card.sleep == False and card.present_damage > 0)) and search_for_property(
                    self.myworldcards, 'Taunt', 2, True):
                    can_attack = True
            else:
                if card.present_property.find('Rush') != -1 and card.present_property.find('Charge') == -1:
                    if card.present_attack_count > 0 and card.present_damage > 0 and search_for_property(
                            self.myworldcards, 'Stealth', 2, True) and len(self.myworldcards) > 0:
                        can_attack = True
                else:
                    if card.present_attack_count > 0 and (card.sleep == False or card.present_property.find(
                            'Charge') != -1) and card.present_damage > 0 and search_for_property(
                        self.myworldcards, 'Stealth', 2, True):
                        can_attack = True
        return can_attack

    def follower_can_attack(self, attack_hero):
        """
        可以攻击随从列表
        :return: 
        """
        can_attack_list = []
        if self.myturn:
            for card in self.myworldcards:
                if self.card_can_attack(card, attack_hero):
                    can_attack_list.append(card)
        else:
            for card in self.enemyworldcards:
                if self.card_can_attack(card, attack_hero):
                    can_attack_list.append(card)
        return can_attack_list

    def do_action(self, myhero, oppohero, myworldcards, oppoworldcards, myhandcards, oppohandcards,
                  mylibrarycards, oppolibrarycards, myweapon, oppoweapon):
        while self.can_use_skill() or self.hero_can_attack() or len(self.follower_can_attack(True)) != 0 or len(
                self.follower_can_attack(False)) != 0 or len(
            self.can_use_handcard(myhero, oppohero, myworldcards, oppoworldcards, myhandcards, oppohandcards,
                                  mylibrarycards, oppolibrarycards, myweapon, oppoweapon)) != 0:
            if self.myturn:
                if len(self.can_use_handcard(myhero, oppohero, myworldcards, oppoworldcards, myhandcards, oppohandcards,
                                             mylibrarycards, oppolibrarycards, myweapon, oppoweapon)) != 0:
                    print("1-使用手牌", end=' ')
                if self.can_use_skill():
                    print("2-使用技能", end=' ')
                if self.hero_can_attack():
                    print("3-英雄攻击", end=' ')
                if len(self.follower_can_attack(True)) != 0 or len(self.follower_can_attack(False)) != 0:
                    print("4-随从攻击", end=' ')
                print("5-结束回合")
                choose = input_int("请选择操作的序号：")
                if choose == 2:
                    if self.can_use_skill():
                        self.skill_using(myhero, oppohero, myworldcards, oppoworldcards, myhandcards, oppohandcards,
                                         mylibrarycards, oppolibrarycards, myweapon, oppoweapon)
                elif choose == 3:
                    if self.hero_can_attack():
                        self.hero_battle()
                elif choose == 4:
                    if len(self.follower_can_attack(True)) != 0 or len(self.follower_can_attack(False)) != 0:
                        self.follower_battle()
                elif choose == 1:
                    if len(self.can_use_handcard(myhero, oppohero, myworldcards, oppoworldcards, myhandcards,
                                                 oppohandcards,
                                                 mylibrarycards, oppolibrarycards, myweapon, oppoweapon)) != 0:
                        self.use_handcard(myhero, oppohero, myworldcards, oppoworldcards, myhandcards, oppohandcards,
                                          mylibrarycards, oppolibrarycards, myweapon, oppoweapon)
                elif choose == 5:
                    break
                else:
                    continue
            else:
                if len(self.can_use_handcard(myhero, oppohero, myworldcards, oppoworldcards, myhandcards, oppohandcards,
                                             mylibrarycards, oppolibrarycards, myweapon, oppoweapon)) != 0:
                    self.use_handcard(myhero, oppohero, myworldcards, oppoworldcards, myhandcards, oppohandcards,
                                      mylibrarycards, oppolibrarycards, myweapon, oppoweapon)
                elif self.can_use_skill():
                    self.skill_using(myhero, oppohero, myworldcards, oppoworldcards, myhandcards, oppohandcards,
                                     mylibrarycards, oppolibrarycards, myweapon, oppoweapon)
                elif len(self.follower_can_attack(True)) != 0 or len(self.follower_can_attack(False)) != 0:
                    self.follower_battle()
                elif self.hero_can_attack():
                    self.hero_battle()
            if not self.check_game_over():
                self.update_hero_damage()
                self.update_world()
                self.update_thisround_cards()
                self.instantly_refresh()
            else:
                break

    def before_round(self):
        """
        回合开始前的动作
        :return: 
        """
        self.current_mana = self.mana
        self.update_previousround_cards()
        self.update_rush_card()
        self.round_begin()
        self.update_hero()
        self.update_world()
        self.update_thisround_cards()
        self.draw_card()
        self.instantly_refresh()

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
        if self.myturn:
            self.before_round()
            self.show_world()
            if not self.check_game_over():
                surrender = input(">>>>>>>>>>>>>>是否投降(Y/N)？")
                if surrender == 'Y' or surrender == 'y':
                    print("~~~~~~~~~~~{0}~~~~~~~~~~~~~".format(self.myhero.surrender))
                else:
                    self.do_action(self.myhero, self.enemyhero, self.myworldcards, self.enemyworldcards,
                                   self.myhandcards, self.enemyhandcards, self.mycards, self.enemycards,
                                   self.myweapon, self.enemyweapon)
                    self.round_end()
        else:
            self.before_round()
            self.show_world()
            if not self.check_game_over():
                self.do_action(self.enemyhero, self.myhero, self.enemyworldcards, self.myworldcards,
                               self.enemyhandcards, self.myhandcards, self.enemycards, self.mycards,
                               self.enemyweapon, self.myweapon)
                self.round_end()
        if not self.check_game_over():
            self.myturn = not self.myturn
            # 水晶达到10后不再增加
            if self.mana < 10 and self.round % 2 == 0:
                self.mana += 1
            self.round += 1
            self.turn_round()

    def instantly_refresh(self):
        """
        即时数据更新
        """
        for handcard in self.myhandcards:
            if handcard.name == '海巨人':
                world_card_count = len(self.myworldcards) + len(self.enemyworldcards)
                if handcard.mana > world_card_count:
                    handcard.present_mana = handcard.mana - world_card_count
                else:
                    handcard.present_mana = 0
        for handcard in self.enemyhandcards:
            if handcard.name == '海巨人':
                world_card_count = len(self.myworldcards) + len(self.enemyworldcards)
                if handcard.mana > world_card_count:
                    handcard.present_mana = handcard.mana - world_card_count
                else:
                    handcard.present_mana = 0
        # 计算卡牌价值
        for worldcard in self.myworldcards:
            worldcard.value = cal_value(worldcard)
        for worldcard in self.enemyworldcards:
            worldcard.value = cal_value(worldcard)

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

    def update_rush_card(self):
        """
        更新突袭后的随从属性
        :return: 
        """
        for card in self.myworldcards:
            if card.present_property.find('Rush') != -1:
                card.present_property = card.present_property.replace('Rush', '').strip()
        for card in self.enemyworldcards:
            if card.present_property.find('Rush') != -1:
                card.present_property = card.present_property.replace('Rush', '').strip()

    def update_world(self):
        """
        删除血量<=0的卡牌
        :return: 
        """
        # 食腐土狼
        my_606_index_list = search_for_id(self.myworldcards, 606)
        for i in range(len(self.myworldcards) - 1, -1, -1):
            card = self.myworldcards[i]
            if card.remain_health <= 0 or not card.alive:
                if len(my_606_index_list) > 0:
                    for index in my_606_index_list:
                        if index != i and self.myworldcards[index].remain_health > 0 and self.myworldcards[
                            index].alive and card.race == 'Beast':
                            print(">>>{0}->{1} {2}-{3} -> ".format(card.name, self.myworldcards[index].name,
                                                                   self.myworldcards[index].present_damage,
                                                                   self.myworldcards[index].remain_health), end='')
                            self.myworldcards[index].present_damage += 2
                            self.myworldcards[index].present_health += 1
                            self.myworldcards[index].remain_health += 1
                            print("{0}-{1}".format(self.myworldcards[index].present_damage,
                                                   self.myworldcards[index].remain_health))
                self.my_death_follower_id.append(card.id)
                if card.name == '苔原犀牛':
                    for worldcard in self.myworldcards:
                        worldcard.reset_property('Charge')
                for handcard in self.myhandcards:
                    if handcard.name == '通道爬行者' and handcard.present_mana > 0:
                        handcard.present_mana -= 1
                for handcard in self.enemyhandcards:
                    if handcard.name == '通道爬行者' and handcard.present_mana > 0:
                        handcard.present_mana -= 1
                if card.present_property.find('Deathrattle') != -1:
                    self.death_rattle(card, self.myhero, self.enemyhero, self.myworldcards, self.enemyworldcards,
                                      self.myhandcards, self.enemyhandcards, self.mycards, self.enemycards)
                self.myworldcards.remove(card)
                if card.race == 'totem':
                    card.reset()
                    self.myhero.totem.append(card)
        # 食腐土狼
        enemy_606_index_list = search_for_id(self.enemyworldcards, 606)
        for i in range(len(self.enemyworldcards) - 1, -1, -1):
            card = self.enemyworldcards[i]
            if card.remain_health <= 0 or not card.alive:
                if len(enemy_606_index_list) > 0:
                    for index in enemy_606_index_list:
                        if index != i and self.enemyworldcards[index].remain_health > 0 and self.enemyworldcards[
                            index].alive and card.race == 'Beast':
                            print(">>>{0}->{1} {2}-{3} -> ".format(card.name, self.enemyworldcards[index].name,
                                                                   self.enemyworldcards[index].present_damage,
                                                                   self.enemyworldcards[index].remain_health), end='')
                            self.enemyworldcards[index].present_damage += 2
                            self.enemyworldcards[index].present_health += 1
                            self.enemyworldcards[index].remain_health += 1
                            print("{0}-{1}".format(self.enemyworldcards[index].present_damage,
                                                   self.enemyworldcards[index].remain_health))
                self.enemy_death_follower_id.append(card.id)
                if card.name == '苔原犀牛':
                    for worldcard in self.enemyworldcards:
                        worldcard.reset_property('Charge')
                for handcard in self.myhandcards:
                    if handcard.name == '通道爬行者' and handcard.present_mana > 0:
                        handcard.present_mana -= 1
                for handcard in self.enemyhandcards:
                    if handcard.name == '通道爬行者' and handcard.present_mana > 0:
                        handcard.present_mana -= 1
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
        # 重置光环伤害
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
        # 森林狼
        my_602_index_list = search_for_id(self.myworldcards, 602)
        if len(my_602_index_list) > 0:
            for my_index in my_602_index_list:
                for index, card in enumerate(self.myworldcards):
                    if card.race == 'Beast' and index != my_index:
                        card.halo_damage += 1
        enemy_602_index_list = search_for_id(self.enemyworldcards, 602)
        if len(enemy_602_index_list) > 0:
            for enemy_index in enemy_602_index_list:
                for index, card in enumerate(self.enemyworldcards):
                    if card.race == 'Beast' and index != enemy_index:
                        card.halo_damage += 1
        # 雷欧克
        my_1135_index_list = search_for_id(self.myworldcards, 1135)
        if len(my_1135_index_list) > 0:
            for my_index in my_1135_index_list:
                for index, card in enumerate(self.myworldcards):
                    if index != my_index:
                        card.halo_damage += 1
        enemy_1135_index_list = search_for_id(self.enemyworldcards, 1135)
        if len(enemy_1135_index_list) > 0:
            for enemy_index in enemy_1135_index_list:
                for index, card in enumerate(self.enemyworldcards):
                    if index != enemy_index:
                        card.halo_damage += 1
        # 苔原犀牛
        my_614_index_list = search_for_id(self.myworldcards, 614)
        if len(my_614_index_list) > 0:
            for my_index in my_614_index_list:
                for index, card in enumerate(self.myworldcards):
                    if index != my_index:
                        card.add_property('Charge')
        enemy_614_index_list = search_for_id(self.enemyworldcards, 614)
        if len(enemy_614_index_list) > 0:
            for enemy_index in enemy_614_index_list:
                for index, card in enumerate(self.enemyworldcards):
                    if index != enemy_index:
                        card.add_property('Charge')
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
        if self.myhero.name == '玛法里奥':
            self.myhero.hero_damage = 0
        if self.enemyhero.name == '玛法里奥':
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
                    print("---------------我方抽牌---------------")
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
                            self.mycards.insert(randnum1, parse_card(get_card_info('card_pool.txt', 1101).strip('\n')))
                            randnum2 = randint(0, len(self.mycards))
                            self.mycards.insert(randnum2, parse_card(get_card_info('card_pool.txt', 1101).strip('\n')))
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
                    self.mycards.insert(randnum1, parse_card(get_card_info('card_pool.txt', 1101).strip('\n')))
                    randnum2 = randint(0, len(self.mycards))
                    self.mycards.insert(randnum2, parse_card(get_card_info('card_pool.txt', 1101).strip('\n')))
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
                    print("---------------敌方抽牌---------------")
                    if draw_card.name == '堕落之血':
                        print(">>>{0}->{1} 生命值 {2}".format(draw_card.name, self.enemyhero.name,
                                                           self.enemyhero.remain_health), end='')
                        if self.enemyhero.armor > 0:
                            print("[{0}]".format(self.enemyhero.armor), end='')
                        self.enemyhero.reduce_health(3)
                        print("->{0}".format(self.enemyhero.remain_health), end='')
                        if self.enemyhero.armor > 0:
                            print("[{0}]".format(self.enemyhero.armor), end='')
                        print("")
                        BloodOfFallenNum += 1
                        self.draw_card(BloodOfFallenNum)
                    else:
                        self.enemyhandcards.append(draw_card)
                        while BloodOfFallenNum > 0:
                            randnum1 = randint(0, len(self.enemycards))
                            self.enemycards.insert(randnum1,
                                                   parse_card(get_card_info('card_pool.txt', 1101).strip('\n')))
                            randnum2 = randint(0, len(self.enemycards))
                            self.enemycards.insert(randnum2,
                                                   parse_card(get_card_info('card_pool.txt', 1101).strip('\n')))
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
                    self.enemycards.insert(randnum1, parse_card(get_card_info('card_pool.txt', 1101).strip('\n')))
                    randnum2 = randint(0, len(self.enemycards))
                    self.enemycards.insert(randnum2, parse_card(get_card_info('card_pool.txt', 1101).strip('\n')))
                    BloodOfFallenNum -= 1

    def skill_using(self, myhero, oppohero, myworldcards, oppoworldcards, myhandcards, oppohandcards,
                    mylibrarycards, oppolibrarycards, myweapon, oppoweapon):
        """
        使用技能 
        :param myhero: 
        :param oppohero: 
        :param myworldcards: 
        :param oppoworldcards: 
        :param myhandcards: 
        :param oppohandcards: 
        :param mylibrarycards: 
        :param oppolibrarycards: 
        :param myweapon: 
        :param oppoweapon: 
        :return: 
        """
        self.current_mana -= 2
        myhero.use_skill = True
        if myhero.name == '加尔鲁什·地狱咆哮':
            myhero.armor += 2
            print("英雄技能：全副武装")
        elif myhero.name == '雷克萨':
            print("英雄技能：稳固射击")
            print(">>>稳固射击->{0} 生命值 {1}".format(oppohero.name, oppohero.remain_health), end='')
            if oppohero.armor > 0:
                print("[{0}]".format(oppohero.armor), end='')
            oppohero.reduce_health(2)
            print("->{0}".format(oppohero.remain_health), end='')
            if oppohero.armor > 0:
                print("[{0}]".format(oppohero.armor), end='')
            print("")
        elif myhero.name == '祖尔金':
            world = [oppohero]
            for card in oppoworldcards:
                if card.present_property.find('AntiMagic') == -1 and card.present_property.find('Stealth') == -1:
                    world.append(card)
            if self.myturn:
                world += [myhero] + myworldcards
            for i in range(len(world)):
                print("{0}-{1}({2}-{3}".format(i + 1, world[i].name, world[i].present_damage,
                                               world[i].remain_health), end='')
                if world[i].armor > 0:
                    print("[{0}]".format(world[i].armor), end='')
                print("/{0})".format(world[i].present_health), end='')
                if world[i].present_property != '':
                    print("[{0}]".format(world[i].present_property), end='')
                else:
                    print(end='')
                if world[i].hero == 'myhero':
                    print("{友}", end=' ')
                else:
                    print("{敌}", end=' ')
            print('')
            if self.myturn:
                choose_num = choose_direct_num(world, "请选择飞斧对象序号：")
            else:
                choose_num = -1
                for i in range(len(world)):
                    if world[i].remain_health <= 2:
                        choose_num = i + 1
                        break
                if choose_num == -1:
                    choose_num = randint(1, len(world))
            print("英雄技能：飞斧->{0} 生命值 {1}".format(world[choose_num - 1].name, world[choose_num - 1].remain_health),
                  end='')
            if world[choose_num - 1].armor > 0:
                print("[{0}]".format(world[choose_num - 1].armor), end='')
            world[choose_num - 1].reduce_health(2)
            print("->{0}".format(world[choose_num - 1].remain_health), end='')
            if world[choose_num - 1].armor > 0:
                print("[{0}]".format(world[choose_num - 1].armor), end='')
            print("")
        elif myhero.name == '古尔丹':
            print("英雄技能：生命分流")
            self.draw_card()
            print(">>>生命分流->{0} 生命值 {1}".format(myhero.name, myhero.remain_health), end='')
            if myhero.armor > 0:
                print("[{0}]".format(myhero.armor), end='')
            myhero.reduce_health(2)
            print("->{0}".format(myhero.remain_health), end='')
            if myhero.armor > 0:
                print("[{0}]".format(myhero.armor), end='')
            print("")
        elif myhero.name == '安度因':
            if self.myturn:
                world = [oppohero]
                for card in oppoworldcards:
                    if card.present_property.find('Stealth') == -1:
                        world.append(card)
                world += [myhero] + myworldcards
            else:
                world = [myhero]
                for card in myworldcards:
                    if card.present_property.find('AntiMagic') == -1:
                        world.append(card)
            for i in range(len(world)):
                print("{0}-{1}({2}-{3}".format(i + 1, world[i].name, world[i].present_damage,
                                               world[i].remain_health), end='')
                if world[i].armor > 0:
                    print("[{0}]".format(world[i].armor), end='')
                print("/{0})".format(world[i].present_health), end='')
                if world[i].present_property != '':
                    print("[{0}]".format(world[i].present_property), end='')
                else:
                    print(end='')
                if world[i].hero == 'myhero':
                    print("{友}", end=' ')
                else:
                    print("{敌}", end=' ')
            print('')
            if self.myturn:
                choose_num = choose_direct_num(world, "请选择加血对象序号：")
            else:
                for i in range(len(world)):
                    if world[i].remain_health != world[i].present_health:
                        choose_num = i + 1
                        break
                else:
                    choose_num = randint(1, len(world))
            world[choose_num - 1].add_health(2)
            print("英雄技能：次级治疗术->{0}".format(world[choose_num - 1].name))
            print("{0}-{1}({2}-{3}/{4})".format(choose_num, world[choose_num - 1].name,
                                                world[choose_num - 1].present_damage,
                                                world[choose_num - 1].remain_health,
                                                world[choose_num - 1].present_health))
        elif myhero.name == '吉安娜':
            world = [oppohero]
            for card in oppoworldcards:
                if card.present_property.find('AntiMagic') == -1 and card.present_property.find('Stealth') == -1:
                    world.append(card)
            if self.myturn:
                world += [myhero] + myworldcards
            for i in range(len(world)):
                print("{0}-{1}({2}-{3}".format(i + 1, world[i].name, world[i].present_damage,
                                               world[i].remain_health), end='')
                if world[i].armor > 0:
                    print("[{0}]".format(world[i].armor), end='')
                print("/{0})".format(world[i].present_health), end='')
                if world[i].present_property != '':
                    print("[{0}]".format(world[i].present_property), end='')
                else:
                    print(end='')
                if world[i].hero == 'myhero':
                    print("{友}", end=' ')
                else:
                    print("{敌}", end=' ')
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
            print("英雄技能：火焰冲击->{0} 生命值 {1}".format(world[choose_num - 1].name, world[choose_num - 1].remain_health),
                  end='')
            if world[choose_num - 1].armor > 0:
                print("[{0}]".format(world[choose_num - 1].armor), end='')
            world[choose_num - 1].reduce_health(1)
            print("->{0}".format(world[choose_num - 1].remain_health), end='')
            if world[choose_num - 1].armor > 0:
                print("[{0}]".format(world[choose_num - 1].armor), end='')
            print("")
        elif myhero.name == '瓦莉拉':
            print("英雄技能：匕首精通")
            sword = parse_card(get_card_info('card_pool.txt', 1102).strip('\n'))
            if myweapon is not None:
                myweapon.alive = False
                self.update_weapon()
            myweapon = sword
            print(">>>装备 {0}".format(myweapon.name))
        elif myhero.name == '玛法里奥':
            myhero.hero_damage += 1
            myhero.armor += 1
            print("英雄技能：变形")
        elif myhero.name == '乌瑟尔':
            soldier = parse_card(get_card_info('card_pool.txt', 1103).strip('\n'))
            soldier.hero = 'myhero'
            print("英雄技能：援军")
            myworldcards.append(soldier)
        elif myhero.name == '萨尔':
            random_index = randint(0, len(myhero.totem) - 1)
            myhero.totem[random_index].hero = 'myhero'
            myworldcards.append(myhero.totem[random_index])
            print("英雄技能：{0}".format(myhero.totem[random_index].name))
            myhero.totem.remove(myhero.totem[random_index])

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
        print(" 剩余卡牌：{0}，剩余手牌：{1}".format(len(self.enemycards), len(self.enemyhandcards)))
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
        print(" 剩余卡牌：{0}，剩余手牌：{1}".format(len(self.mycards), len(self.myhandcards)))

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

    def use_handcard(self, myhero, oppohero, myworldcards, oppoworldcards, myhandcards, oppohandcards,
                     mylibrarycards, oppolibrarycards, myweapon, oppoweapon):
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
            if self.card_can_use(self.myhandcards[goto_num - 1], myhero, oppohero, myworldcards, oppoworldcards,
                                 myhandcards, oppohandcards, mylibrarycards, oppolibrarycards, myweapon, oppoweapon):
                temp_handcard = self.myhandcards[goto_num - 1]
                self.current_mana -= temp_handcard.present_mana
                del self.myhandcards[goto_num - 1]
                if temp_handcard.type == 'Follower':
                    if temp_handcard.present_property.find('Battlecry') != -1:
                        self.battle_cry(temp_handcard, self.myhero, self.enemyhero,
                                        self.myworldcards, self.enemyworldcards, self.myhandcards,
                                        self.enemyhandcards, self.mycards, self.enemycards, self.myweapon,
                                        self.enemyweapon)
                    else:
                        if len(self.myworldcards) == 0:
                            self.myworldcards.append(temp_handcard)
                        else:
                            for index, worldcard in enumerate(self.myworldcards):
                                print(" <<{0}>> {1}".format(index, worldcard.name), end='')
                            print(" <<{0}>>".format(len(self.myworldcards)))
                            choose_num = choose_object_num(self.myworldcards, "请选择卡牌要上场位置的序号：")
                            if choose_num < len(self.myworldcards):
                                if self.myworldcards[choose_num].race.find(
                                        'Machine') != -1 and temp_handcard.present_property.find('Magnetic') != -1:
                                    self.myworldcards[choose_num].present_health += temp_handcard.health
                                    self.myworldcards[choose_num].remain_health += temp_handcard.health
                                    self.myworldcards[choose_num].buff_damage += temp_handcard.damage
                                    self.myworldcards[choose_num].update_buff_damage()
                                    property_list = temp_handcard.present_property.split(' ')
                                    for property in property_list:
                                        if self.myworldcards[choose_num].present_property.find(property) == -1:
                                            self.myworldcards[choose_num].present_property += (' ' + property)
                                else:
                                    self.myworldcards.insert(choose_num, temp_handcard)
                            else:
                                self.myworldcards.insert(choose_num, temp_handcard)
                        print(">>>>>>{0}-{1}({2})".format(goto_num, temp_handcard.name, temp_handcard.present_mana),
                              end='')
                        if temp_handcard.present_property != '':
                            print("[{0}]".format(temp_handcard.present_property), end='')
                        print("上场！！！")
                elif temp_handcard.type == 'Magic':
                    self.myhero.cast_list.append(temp_handcard)
                    self.cast(temp_handcard, self.myhero, self.enemyhero, self.myworldcards, self.enemyworldcards,
                              self.myhandcards, self.enemyhandcards, self.mycards, self.enemycards, self.myweapon,
                              self.enemyweapon, False)
                elif temp_handcard.type == 'Weapon':
                    if self.myweapon is not None:
                        self.myweapon.alive = False
                        self.update_weapon()
                    self.myweapon = temp_handcard
                    print(">>>装备 {0}".format(self.myweapon.name))
                elif temp_handcard.type == 'Hero':
                    if temp_handcard.present_property.find('Battlecry') != -1:
                        self.battle_cry(temp_handcard, self.myhero, self.enemyhero,
                                        self.myworldcards, self.enemyworldcards, self.myhandcards,
                                        self.enemyhandcards, self.mycards, self.enemycards, self.myweapon,
                                        self.enemyweapon)
            else:
                print(">>>您无法使用这张牌！！！")
        else:
            self.auto_usehandcard()

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
            attack_obj = self.attack_who(self.enemyhero, opposite)
            if not (attack_obj.remain_health + attack_obj.armor - self.enemyhero.present_damage > 0 and \
                                        self.enemyhero.remain_health + self.enemyhero.armor - attack_obj.present_damage < 0):
                print(
                    "{0}{1}-{2} ".format(self.enemyhero.name, self.enemyhero.present_damage,
                                         self.enemyhero.remain_health),
                    end='')
                if self.enemyhero.armor > 0:
                    print("[{0}]".format(self.enemyhero.armor), end=' ')
                print("attack {0}{1}-{2}".format(attack_obj.name, attack_obj.present_damage,
                                                 attack_obj.remain_health), end='')
                if attack_obj.armor > 0:
                    print("[{0}]".format(attack_obj.armor), end='')
                print('')
                self.enemyhero.attack(attack_obj, self.enemyhero, self.myhero)
                attack_obj.show()
                if self.myweapon is not None:
                    if self.enemyweapon.name == '霜之哀伤' and attack_obj.type == 'Follower' and not attack_obj.alive:
                        self.enemyhero.add_kill(attack_obj)
                if self.myhero.remain_health <= 0 or self.enemyhero.remain_health <= 0:
                    return
                self.enemyhero.show()
                if self.enemyweapon is not None:
                    if self.enemyweapon.remain_health > 0:
                        self.enemyweapon.reduce_health(1)
            else:
                self.enemyhero.present_attack_count -= 1
        self.update_weapon()

    def follower_battle(self):
        """
        随从对战
        :return: 
        """
        if self.myturn:
            for i in range(len(self.myworldcards)):
                print("{0}-{1}({2}-{3}/{4})".format(i + 1, self.myworldcards[i].name,
                                                    self.myworldcards[i].present_damage,
                                                    self.myworldcards[i].remain_health,
                                                    self.myworldcards[i].present_health), end='')
                if self.myworldcards[i].present_property != '':
                    print("[{0}]".format(self.myworldcards[i].present_property), end='')
                if self.card_can_attack(self.myworldcards[i], False) or self.card_can_attack(self.myworldcards[i],
                                                                                             True):
                    print("<Active>", end=' ')
                else:
                    print("<No Active>", end=' ')
            print('')
            ready_attack_num = choose_object_num(self.myworldcards, "请选择进行攻击的对象序号，不攻击输入0：")
            if ready_attack_num == 0:
                return
            if self.card_can_attack(self.myworldcards[ready_attack_num - 1], False) or self.card_can_attack(
                    self.myworldcards[ready_attack_num - 1], True):
                if self.myworldcards[ready_attack_num - 1].present_property.find('Rush') != -1 and self.myworldcards[
                            ready_attack_num - 1].present_property.find('Charge') == -1:
                    opposite = self.enemyworldcards
                else:
                    opposite = [self.enemyhero] + self.enemyworldcards
                print("------------攻击----------------")
                print("{0}({1}-{2})".format(self.myworldcards[ready_attack_num - 1].name,
                                            self.myworldcards[ready_attack_num - 1].present_damage,
                                            self.myworldcards[ready_attack_num - 1].remain_health), end='')
                if self.myworldcards[ready_attack_num - 1].present_property != '':
                    print("[{0}] 准备攻击：".format(self.myworldcards[ready_attack_num - 1].present_property))
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
                if self.myworldcards[ready_attack_num - 1].attack(opposite[attack_num - 1], self.myhero,
                                                                  self.enemyhero) and \
                                self.myworldcards[ready_attack_num - 1].present_property.find('OverKill') != -1:
                    self.over_kill(self.myworldcards[ready_attack_num - 1], self.myhero, self.enemyhero,
                                   self.myworldcards,
                                   self.enemyworldcards, self.myhandcards, self.enemyhandcards, self.mycards,
                                   self.enemycards)
                if self.enemyhero.remain_health <= 0:
                    return
                self.myworldcards[ready_attack_num - 1].show()
                opposite[attack_num - 1].show()
            else:
                print(">>>这个随从无法攻击！！！")
        else:
            can_attack_hero_list = self.follower_can_attack(True)
            attack_hero_list = all_smart_attack_one(can_attack_hero_list, self.myhero)
            # 可以杀死英雄
            if attack_hero_list is not None:
                for card in attack_hero_list:
                    print("------------攻击----------------")
                    print("{0}{1}-{2} ".format(card.name, card.present_damage,
                                               card.remain_health), end='')
                    if card.armor > 0:
                        print("[{0}]".format(card.armor), end='')
                    if card.present_property != '':
                        print("[{0}]".format(card.present_property), end='')
                    else:
                        print(end='')
                    print(" attack {0}{1}-{2}".format(self.myhero.name, self.myhero.present_damage,
                                                      self.myhero.remain_health), end='')
                    if self.myhero.armor > 0:
                        print("[{0}]".format(self.myhero.armor), end='')
                    if self.myhero.present_property != '':
                        print("[{0}]".format(self.myhero.present_property))
                    else:
                        print('')
                    if card.attack(self.myhero, self.enemyhero, self.myhero) and \
                                    card.present_property.find('OverKill') != -1:
                        self.over_kill(card, self.enemyhero, self.myhero, self.enemyworldcards,
                                       self.myworldcards,
                                       self.enemyhandcards, self.myhandcards, self.enemycards, self.mycards)
                    if self.myhero.remain_health <= 0:
                        return
                    self.myhero.show()
                    card.show()
            # 无法杀死英雄
            else:
                # 有嘲讽随从
                if search_for_property(self.myworldcards, 'Taunt', 1, False):
                    beaten_follower_list = search_property(self.myworldcards, 'Taunt', 1, False)
                    smart_value_order(beaten_follower_list, True)
                    beaten_follower = beaten_follower_list[0]
                    can_attack_follower_list = self.follower_can_attack(False)
                    smart_value_order(can_attack_follower_list, False)
                    attack_follower_list = all_smart_attack_one(can_attack_follower_list, beaten_follower)
                    # 可以杀死嘲讽随从
                    if attack_follower_list is not None:
                        for card in attack_follower_list:
                            print("------------攻击----------------")
                            print("{0}{1}-{2} ".format(card.name, card.present_damage,
                                                       card.remain_health), end='')
                            if card.armor > 0:
                                print("[{0}]".format(card.armor), end='')
                            if card.present_property != '':
                                print("[{0}]".format(card.present_property), end='')
                            else:
                                print(end='')
                            print(" attack {0}{1}-{2}".format(beaten_follower.name, beaten_follower.present_damage,
                                                              beaten_follower.remain_health), end='')
                            if beaten_follower.armor > 0:
                                print("[{0}]".format(beaten_follower.armor), end='')
                            if beaten_follower.present_property != '':
                                print("[{0}]".format(beaten_follower.present_property))
                            else:
                                print('')
                            if card.attack(beaten_follower, self.enemyhero, self.myhero) and \
                                            card.present_property.find('OverKill') != -1:
                                self.over_kill(card, self.enemyhero, self.myhero, self.enemyworldcards,
                                               self.myworldcards,
                                               self.enemyhandcards, self.myhandcards, self.enemycards,
                                               self.mycards)
                            beaten_follower.show()
                            card.show()
                    else:
                        for card in can_attack_follower_list:
                            card.present_attack_count -= 1
                # 无嘲讽随从
                else:
                    can_attack_follower_list = self.follower_can_attack(False)
                    # 有不潜行随从
                    if len(can_attack_follower_list) > 0:
                        battle_follower = all_smart_attack_all(can_attack_follower_list,
                                                               search_property(self.myworldcards, 'Stealth', 2, True))
                        if battle_follower is not None:
                            print("------------攻击----------------")
                            print("{0}{1}-{2} ".format(battle_follower[0].name, battle_follower[0].present_damage,
                                                       battle_follower[0].remain_health), end='')
                            if battle_follower[0].armor > 0:
                                print("[{0}]".format(battle_follower[0].armor), end='')
                            if battle_follower[0].present_property != '':
                                print("[{0}]".format(battle_follower[0].present_property), end='')
                            else:
                                print(end='')
                            print(
                                " attack {0}{1}-{2}".format(battle_follower[1].name,
                                                            battle_follower[1].present_damage,
                                                            battle_follower[1].remain_health), end='')
                            if battle_follower[1].armor > 0:
                                print("[{0}]".format(battle_follower[1].armor), end='')
                            if battle_follower[1].present_property != '':
                                print("[{0}]".format(battle_follower[1].present_property))
                            else:
                                print('')
                            if battle_follower[0].attack(battle_follower[1], self.enemyhero, self.myhero) and \
                                            battle_follower[0].present_property.find('OverKill') != -1:
                                self.over_kill(battle_follower[0], self.enemyhero, self.myhero,
                                               self.enemyworldcards,
                                               self.myworldcards,
                                               self.enemyhandcards, self.myhandcards, self.enemycards,
                                               self.mycards)
                            battle_follower[0].show()
                            battle_follower[1].show()
                        else:
                            can_attack_hero_list = self.follower_can_attack(True)
                            if len(can_attack_hero_list) > 0:
                                print("------------攻击----------------")
                                print("{0}{1}-{2} ".format(can_attack_hero_list[0].name,
                                                           can_attack_hero_list[0].present_damage,
                                                           can_attack_hero_list[0].remain_health), end='')
                                if can_attack_hero_list[0].armor > 0:
                                    print("[{0}]".format(can_attack_hero_list[0].armor), end='')
                                if can_attack_hero_list[0].present_property != '':
                                    print("[{0}]".format(can_attack_hero_list[0].present_property), end='')
                                else:
                                    print(end='')
                                print(" attack {0}{1}-{2}".format(self.myhero.name, self.myhero.present_damage,
                                                                  self.myhero.remain_health), end='')
                                if self.myhero.armor > 0:
                                    print("[{0}]".format(self.myhero.armor), end='')
                                if self.myhero.present_property != '':
                                    print("[{0}]".format(self.myhero.present_property))
                                else:
                                    print('')
                                if can_attack_hero_list[0].attack(self.myhero, self.enemyhero, self.myhero) and \
                                                can_attack_hero_list[0].present_property.find('OverKill') != -1:
                                    self.over_kill(can_attack_hero_list[0], self.enemyhero, self.myhero,
                                                   self.enemyworldcards,
                                                   self.myworldcards,
                                                   self.enemyhandcards, self.myhandcards, self.enemycards,
                                                   self.mycards)
                                if self.myhero.remain_health <= 0:
                                    return
                                self.myhero.show()
                                can_attack_hero_list[0].show()
                            else:
                                for card in can_attack_follower_list:
                                    card.present_attack_count -= 1
                    # 没有随从或者都是潜行的随从
                    else:
                        can_attack_hero_list = self.follower_can_attack(True)
                        if len(can_attack_hero_list) > 0:
                            print("------------攻击----------------")
                            print("{0}{1}-{2} ".format(can_attack_hero_list[0].name,
                                                       can_attack_hero_list[0].present_damage,
                                                       can_attack_hero_list[0].remain_health), end='')
                            if can_attack_hero_list[0].armor > 0:
                                print("[{0}]".format(can_attack_hero_list[0].armor), end='')
                            if can_attack_hero_list[0].present_property != '':
                                print("[{0}]".format(can_attack_hero_list[0].present_property), end='')
                            else:
                                print(end='')
                            print(" attack {0}{1}-{2}".format(self.myhero.name, self.myhero.present_damage,
                                                              self.myhero.remain_health), end='')
                            if self.myhero.armor > 0:
                                print("[{0}]".format(self.myhero.armor), end='')
                            if self.myhero.present_property != '':
                                print("[{0}]".format(self.myhero.present_property))
                            else:
                                print('')
                            if can_attack_hero_list[0].attack(self.myhero, self.enemyhero, self.myhero) and \
                                            can_attack_hero_list[0].present_property.find('OverKill') != -1:
                                self.over_kill(can_attack_hero_list[0], self.enemyhero, self.myhero,
                                               self.enemyworldcards,
                                               self.myworldcards,
                                               self.enemyhandcards, self.myhandcards, self.enemycards, self.mycards)
                            if self.myhero.remain_health <= 0:
                                return
                            self.myhero.show()
                            can_attack_hero_list[0].show()
                        else:
                            for card in can_attack_follower_list:
                                card.present_attack_count -= 1

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
        elif card.name == '乌达斯塔':
            beast_list = search_race(myhandcards, 'Beast')
            if len(beast_list) > 0:
                random_beast = random.choice(beast_list)
                if len(myworldcards) < WORLDCARDNUM:
                    print(">>>{0} -> {1}".format(card.name, random_beast.name))
                    myworldcards.append(random_beast)
                    myhandcards.remove(random_beast)

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
                myhandcards.append(parse_card(get_card_info('card_pool.txt', 1104).strip('\n')))
                myhandcards.append(parse_card(get_card_info('card_pool.txt', 1104).strip('\n')))
                if self.myturn:
                    myhandcards[-1].hero = 'myhero'
                    myhandcards[-2].hero = 'myhero'
                else:
                    myhandcards[-1].hero = 'enemyhero'
                    myhandcards[-2].hero = 'enemyhero'
            elif len(myhandcards) == HANDCARDNUM - 1:
                myhandcards.append(parse_card(get_card_info('card_pool.txt', 1104).strip('\n')))
                if self.myturn:
                    myhandcards[-1].hero = 'myhero'
                else:
                    myhandcards[-1].hero = 'enemyhero'
        elif card.name == '紫色岩虫':
            while len(myworldcards) < WORLDCARDNUM:
                myworldcards.append(parse_card(get_card_info('card_pool.txt', 1105).strip('\n')))
                if self.myturn:
                    myworldcards[-1].hero = 'myhero'
                else:
                    myworldcards[-1].hero = 'enemyhero'
        elif card.name == '机械克苏恩':
            if len(myworldcards) == 0 and len(myhandcards) == 0 and len(mylibrarycards) == 0:
                oppohero.alive = False
        elif card.name == '夺灵者哈卡':
            myrandnum = randint(0, len(mylibrarycards) - 1)
            mylibrarycards.insert(myrandnum, parse_card(get_card_info('card_pool.txt', 1101).strip('\n')))
            opporandnum = randint(0, len(oppolibrarycards) - 1)
            oppolibrarycards.insert(opporandnum, parse_card(get_card_info('card_pool.txt', 1101).strip('\n')))
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
        elif card.name == '大师宝箱':
            if len(oppohandcards) < HANDCARDNUM:
                master_treasure_chest_card = master_treasure_chest_cards()
                oppohandcards.append(master_treasure_chest_card)
                if oppohandcards[-1].type == 'Follower':
                    if card.hero == 'myhero':
                        oppohandcards[-1].hero = 'enemyhero'
                    else:
                        oppohandcards[-1].hero = 'myhero'
                print(">>>{0} -> {1}".format(card.name, master_treasure_chest_card.name))
        elif card.name == '闪光蝴蝶':
            if len(myhandcards) < HANDCARDNUM:
                hunter_magic_list = search_occupation_type(get_card_pool(), 'Hunter', 'Magic')
                random_hunter_magic = random.sample(hunter_magic_list, 1)[0]
                print(">>>{0} -> {1}".format(card.name, random_hunter_magic.name))
                myhandcards.append(random_hunter_magic)

    def battle_cry(self, card, myhero, oppohero, myworldcards, oppoworldcards, myhandcards, oppohandcards,
                   mylibrarycards, oppolibrarycards, myweapon, oppoweapon):
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
        card.present_property = card.present_property.replace('Battlecry', '').strip()
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
            print(">>>>>>{0}({1})".format(card.name, card.present_mana), end='')
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
                        print("[{0}]".format(world[i].present_property), end='')
                    else:
                        print(end='')
                    if world[i].hero == 'myhero':
                        print("{友}", end=' ')
                    else:
                        print("{敌}", end=' ')
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
            print(">>>>>>{0}({1})".format(card.name, card.present_mana), end='')
            if card.present_property != '':
                print("[{0}]".format(card.present_property), end='')
            print("上场！！！")
        elif card.name == '龙骨卫士':
            if self.myturn:
                handcard = self.myhandcards
            else:
                handcard = self.enemyhandcards
            if search_for_race(handcard, 'Dragon', 1):
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
            print(">>>>>>{0}({1})".format(card.name, card.present_mana), end='')
            if card.present_property != '':
                print("[{0}]".format(card.present_property), end='')
            print("上场！！！")
        elif card.name == '始生幼龙':
            for worldcard in myworldcards:
                print(">>>{0}->{1}(我方随从) 血量：{2} -> ".format(card.name, worldcard.name, worldcard.remain_health),
                      end='')
                worldcard.reduce_health(2)
                print("{0}".format(worldcard.remain_health))
            for worldcard in oppoworldcards:
                print(">>>{0}->{1}(敌方随从) 血量：{2} -> ".format(card.name, worldcard.name, worldcard.remain_health),
                      end='')
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
            print(">>>>>>{0}({1})".format(card.name, card.present_mana), end='')
            if card.present_property != '':
                print("[{0}]".format(card.present_property), end='')
            print("上场！！！")
        elif card.name == '祖尔金':
            myhero.name = card.name
            myhero.armor += 7
            myhero.say_hi = card.say_hi
            myhero.surrender = card.surrender
            print(">>>祖尔金-----------------------开始")
            random.shuffle(myhero.cast_list)
            for cast in myhero.cast_list:
                self.cast(cast, myhero, oppohero, myworldcards, oppoworldcards, myhandcards,
                          oppohandcards, mylibrarycards, oppolibrarycards, myweapon, oppoweapon, True)
                self.update_hero_damage()
                self.update_world()
                self.update_thisround_cards()
                self.instantly_refresh()
            print(">>>祖尔金-----------------------结束")
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
            print(">>>>>>{0}({1})".format(card.name, card.present_mana), end='')
            if card.present_property != '':
                print("[{0}]".format(card.present_property), end='')
            print("上场！！！")
            if card.name == '火羽精灵':
                if len(myhandcards) < HANDCARDNUM:
                    myhandcards.append(parse_card(get_card_info('card_pool.txt', 1106).strip('\n')))
                    if self.myturn:
                        myhandcards[-1].hero = 'myhero'
                    else:
                        myhandcards[-1].hero = 'enemyhero'
            elif card.name == '穆克拉':
                banana = parse_card(get_card_info('card_pool.txt', 1107).strip('\n'))
                if len(oppohandcards) < HANDCARDNUM - 1:
                    oppohandcards.append(banana)
                    oppohandcards.append(banana)
                elif len(oppohandcards) == HANDCARDNUM - 1:
                    oppohandcards.append(banana)
            elif card.name == '石丘防御者':
                choose_followers = random.sample(search_property(get_card_pool(), 'Taunt', 1, True), 3)
                for i in range(len(choose_followers)):
                    print("{0}-{1}({2}-{3}/{0})".format(i + 1, choose_followers[i].name,
                                                        choose_followers[i].present_damage,
                                                        choose_followers[i].remain_health,
                                                        choose_followers[i].present_health), end='')
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
                    if self.myturn:
                        myhandcards[-1].hero = 'myhero'
                    else:
                        myhandcards[-1].hero = 'enemyhero'
            elif card.name == '火车王里诺艾':
                if len(oppoworldcards) < WORLDCARDNUM - 1:
                    oppoworldcards.append(parse_card(get_card_info('card_pool.txt', 1108).strip('\n')))
                    oppoworldcards.append(parse_card(get_card_info('card_pool.txt', 1108).strip('\n')))
                elif len(oppoworldcards) == WORLDCARDNUM - 1:
                    oppoworldcards.append(parse_card(get_card_info('card_pool.txt', 1108).strip('\n')))
            elif card.name == '王牌猎人':
                if self.myturn:
                    world = self.enemyworldcards
                else:
                    world = self.myworldcards
                if search_for_damage(world, 7, 4, False):
                    for i in range(len(world)):
                        print("{0}-{1}({2}-{3}".format(i + 1, world[i].name, world[i].present_damage,
                                                       world[i].remain_health), end='')
                        if world[i].armor > 0:
                            print("[{0}]".format(world[i].armor), end='')
                        print("/{0})".format(world[i].present_health), end='')
                        if world[i].present_property != '':
                            print("[{0}]".format(world[i].present_property), end='')
                        else:
                            print(end='')
                        if world[i].hero == 'myhero':
                            print("{友}", end=' ')
                        else:
                            print("{敌}", end=' ')
                    print('')
                    while True:
                        if self.myturn:
                            choose_num = choose_object_num(world, "请选择要消灭的对象（攻击力大于等于7）序号：")
                        else:
                            choose_num = randint(1, len(world))
                        if world[choose_num - 1].present_damage >= 7 and world[
                                    choose_num - 1].present_property.find(
                            'Stealth') == -1:
                            break
                    print(">>>{0} 消灭了 {1}".format(card.name, world[choose_num - 1].name))
                    world.remove(world[choose_num - 1])
            elif card.name == '狂奔的科多兽':
                if self.myturn:
                    world = self.enemyworldcards
                else:
                    world = self.myworldcards
                if search_for_damage(world, 2, 5, True):
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
                if search_for_property(world, 'Taunt', 1, False):
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
                print("/{0}){友}".format(self.myhero.present_health))
                print("2-{0}({1}-{2}".format(self.enemyhero.name, self.enemyhero.present_damage,
                                             self.enemyhero.remain_health), end='')
                if self.enemyhero.armor > 0:
                    print("[{0}]".format(self.enemyhero.armor), end='')
                print("/{0}){敌}".format(self.enemyhero.present_health))
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
                    print(">>>{0}->{1} 血量：{2} -> ".format(card.name, self.enemyhero.name,
                                                          self.enemyhero.remain_health),
                          end='')
                    self.enemyhero.remain_health = 15
                    print("{0}".format(self.enemyhero.remain_health))
            elif card.name == '欧克哈特大师':
                if self.myturn:
                    DamageOne = search_damage(self.mycards, 1)
                    DamageTwo = search_damage(self.mycards, 2)
                    DamageThree = search_damage(self.mycards, 3)
                    if len(DamageOne) > 0 and len(self.myworldcards) < WORLDCARDNUM:
                        randnum = randint(0, len(DamageOne) - 1)
                        self.mycards.remove(DamageOne[randnum])
                        self.myworldcards.append(DamageOne[randnum])
                        print(">>>{0}->{1}({2})".format(card.name, DamageOne[randnum].name,
                                                        DamageOne[randnum].present_mana),
                              end='')
                        if DamageOne[randnum].present_property != '':
                            print("[{0}]".format(DamageOne[randnum].present_property), end='')
                        print("上场！！！")
                    if len(DamageTwo) > 0 and len(self.myworldcards) < WORLDCARDNUM:
                        randnum = randint(0, len(DamageTwo) - 1)
                        self.mycards.remove(DamageTwo[randnum])
                        self.myworldcards.append(DamageTwo[randnum])
                        print(">>>{0}->{1}({2})".format(card.name, DamageTwo[randnum].name,
                                                        DamageTwo[randnum].present_mana),
                              end='')
                        if DamageTwo[randnum].present_property != '':
                            print("[{0}]".format(DamageTwo[randnum].present_property), end='')
                        print("上场！！！")
                    if len(DamageThree) > 0 and len(self.myworldcards) < WORLDCARDNUM:
                        randnum = randint(0, len(DamageThree) - 1)
                        self.mycards.remove(DamageThree[randnum])
                        self.myworldcards.append(DamageThree[randnum])
                        print(
                            ">>>{0}->{1}({2})".format(card.name, DamageThree[randnum].name,
                                                      DamageThree[randnum].present_mana),
                            end='')
                        if DamageThree[randnum].present_property != '':
                            print("[{0}]".format(DamageThree[randnum].present_property), end='')
                        print("上场！！！")
                else:
                    DamageOne = search_damage(self.enemycards, 1)
                    DamageTwo = search_damage(self.enemycards, 2)
                    DamageThree = search_damage(self.enemycards, 3)
                    if len(DamageOne) > 0 and len(self.enemyworldcards) < WORLDCARDNUM:
                        randnum = randint(0, len(DamageOne) - 1)
                        self.enemycards.remove(DamageOne[randnum])
                        self.enemyworldcards.append(DamageOne[randnum])
                        print(">>>{0}->{1}({2})".format(card.name, DamageOne[randnum].name,
                                                        DamageOne[randnum].present_mana),
                              end='')
                        if DamageOne[randnum].present_property != '':
                            print("[{0}]".format(DamageOne[randnum].present_property), end='')
                        print("上场！！！")
                    if len(DamageTwo) > 0 and len(self.enemyworldcards) < WORLDCARDNUM:
                        randnum = randint(0, len(DamageTwo) - 1)
                        self.enemycards.remove(DamageTwo[randnum])
                        self.enemyworldcards.append(DamageTwo[randnum])
                        print(">>>{0}->{1}({2})".format(card.name, DamageTwo[randnum].name,
                                                        DamageTwo[randnum].present_mana),
                              end='')
                        if DamageTwo[randnum].present_property != '':
                            print("[{0}]".format(DamageTwo[randnum].present_property), end='')
                        print("上场！！！")
                    if len(DamageThree) > 0 and len(self.enemyworldcards) < WORLDCARDNUM:
                        randnum = randint(0, len(DamageThree) - 1)
                        self.enemycards.remove(DamageThree[randnum])
                        self.enemyworldcards.append(DamageThree[randnum])
                        print(
                            ">>>{0}->{1}({2})".format(card.name, DamageThree[randnum].name,
                                                      DamageThree[randnum].present_mana),
                            end='')
                        if DamageThree[randnum].present_property != '':
                            print("[{0}]".format(DamageThree[randnum].present_property), end='')
                        print("上场！！！")
            elif card.name == '游荡恶鬼':
                for i in range(len(self.myhandcards) - 1, -1, -1):
                    if self.myhandcards[i].present_mana == 1 and self.myhandcards[i].type == 'Magic':
                        print(">>>{0} 摧毁 {1}(我方手牌)".format(card.name, self.myhandcards[i].name))
                        self.myhandcards.remove(self.myhandcards[i])
                for i in range(len(self.enemyhandcards) - 1, -1, -1):
                    if self.enemyhandcards[i].present_mana == 1 and self.enemyhandcards[i].type == 'Magic':
                        print(">>>{0} 摧毁 {1}(敌方手牌)".format(card.name, self.enemyhandcards[i].name))
                        self.enemyhandcards.remove(self.enemyhandcards[i])
                for i in range(len(self.mycards) - 1, -1, -1):
                    if self.mycards[i].present_mana == 1 and self.mycards[i].type == 'Magic':
                        print(">>>{0} 摧毁 {1}(我方牌库)".format(card.name, self.mycards[i].name))
                        self.mycards.remove(self.mycards[i])
                for i in range(len(self.enemycards) - 1, -1, -1):
                    if self.enemycards[i].present_mana == 1 and self.enemycards[i].type == 'Magic':
                        print(">>>{0} 摧毁 {1}(敌方牌库)".format(card.name, self.enemycards[i].name))
                        self.enemycards.remove(self.enemycards[i])
            elif card.name == '恩佐斯':
                if self.myturn:
                    self.mydeathfollower = []
                    for id in self.my_death_follower_id:
                        self.mydeathfollower.append(parse_card(get_card_info('card_pool.txt', id).strip('\n')))
                    deathrattle_list = search_property(self.mydeathfollower, 'Deathrattle', 1, True)
                    for deathcard in deathrattle_list:
                        if len(self.myworldcards) < WORLDCARDNUM:
                            print(">>>{0} -> {1}".format(card.name, deathcard.name))
                            self.myworldcards.append(deathcard)
                            self.myworldcards[-1].hero = 'myhero'
                else:
                    self.enemydeathfollower = []
                    for id in self.enemy_death_follower_id:
                        self.enemydeathfollower.append(parse_card(get_card_info('card_pool.txt', id).strip('\n')))
                    deathrattle_list = search_property(self.enemydeathfollower, 'Deathrattle', 1, True)
                    for deathcard in deathrattle_list:
                        if len(self.enemyworldcards) < WORLDCARDNUM:
                            print(">>>{0} -> {1}".format(card.name, deathcard.name))
                            self.enemyworldcards.append(deathcard)
                            self.enemyworldcards[-1].hero = 'enemyhero'
            elif card.name == '老狐狸马林':
                if len(oppoworldcards) < WORLDCARDNUM:
                    master_treasure_chest = parse_card(get_card_info('card_pool.txt', 1126).strip('\n'))
                    oppoworldcards.append(master_treasure_chest)
                    print(">>>{0} -> {1}".format(card.name, master_treasure_chest.name))
                    if self.myturn:
                        oppoworldcards[-1].hero = 'enemyhero'
                    else:
                        oppoworldcards[-1].hero = 'myhero'
            elif card.name == '黄金狗头人':
                print(">>>{0} -> ".format(card.name), end='')
                card_num = len(myhandcards)
                myhandcards.clear()
                while card_num > 0:
                    legend_card = random.sample(search_color(get_card_pool(), 'golden'), 1)[0]
                    myhandcards.append(legend_card)
                    if self.myturn:
                        myhandcards[-1].hero = 'myhero'
                    else:
                        myhandcards[-1].hero = 'enemyhero'
                    print("{0} ".format(legend_card.name), end='')
                    card_num -= 1
                print("")
            elif card.name == '魔泉山猫':
                if len(myhandcards) < HANDCARDNUM:
                    myhandcards.append(parse_card(get_card_info('card_pool.txt', 1131).strip('\n')))
                    if self.myturn:
                        myhandcards[-1].hero = 'myhero'
                    else:
                        myhandcards[-1].hero = 'enemyhero'

    def can_use_random_cast(self, card):
        """
        随机法术是否可用
        :param card: 
        :return: 
        """
        can_use = False
        if card.SpecialMagic == 'DirectFollower':
            for worldcard in self.myworldcards:
                if worldcard.present_property.find('AntiMagic') == -1:
                    can_use = True
                    break
            for worldcard in self.enemyworldcards:
                if worldcard.present_property.find('AntiMagic') == -1 and worldcard.present_property.find(
                        'Stealth') == -1:
                    can_use = True
                    break
        elif card.SpecialMagic == 'DirectBeast':
            for worldcard in self.myworldcards:
                if worldcard.present_property.find('AntiMagic') == -1 and worldcard.race == 'Beast':
                    can_use = True
                    break
            for worldcard in self.enemyworldcards:
                if worldcard.present_property.find('AntiMagic') == -1 and worldcard.present_property.find(
                        'Stealth') == -1 and worldcard.race == 'Beast':
                    can_use = True
                    break
        elif card.SpecialMagic == 'NeedEnemyFollower':
            if len(self.enemyworldcards) > 0:
                can_use = True
        else:
            can_use = True
        return can_use

    def cast(self, card, myhero, oppohero, myworldcards, oppoworldcards, myhandcards, oppohandcards,
             mylibrarycards, oppolibrarycards, myweapon, oppoweapon, isRandom):
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
        if card.SpecialMagic.find('Direct') != -1:
            my_follower = []
            oppo_follower = []
            for worldcard in myworldcards:
                if worldcard.present_property.find('AntiMagic') == -1:
                    my_follower.append(worldcard)
            for worldcard in oppoworldcards:
                if worldcard.present_property.find('Stealth') == -1 and worldcard.present_property.find(
                        'AntiMagic') == -1:
                    oppo_follower.append(worldcard)
            follower = my_follower + oppo_follower
            my_follower_hero = [myhero] + my_follower
            oppo_follower_hero = [oppohero] + oppo_follower
            follower_hero = [myhero] + [oppohero] + follower

            if not self.myturn and not isRandom:
                if card.SpecialMagic.find('MyAll') != -1:
                    choose_area = my_follower_hero
                elif card.SpecialMagic.find('MyFollower') != -1:
                    choose_area = my_follower
                elif card.SpecialMagic.find('EnemyAll') != -1:
                    choose_area = oppo_follower_hero
                elif card.SpecialMagic.find('EnemyFollower') != -1:
                    choose_area = oppo_follower
                elif card.SpecialMagic.find('All') != -1:
                    choose_area = follower_hero
                if card.SpecialMagic.find('Beast') != -1:
                    choose_area = search_race(choose_area, 'Beast')
            else:
                if card.SpecialMagic.find('All') != -1:
                    choose_area = follower_hero
                elif card.SpecialMagic.find('Follower') != -1:
                    choose_area = follower
                if card.SpecialMagic.find('Beast') != -1:
                    choose_area = search_race(choose_area, 'Beast')

            for i in range(len(choose_area)):
                print("{0}-{1}({2}-{3}".format(i + 1, choose_area[i].name, choose_area[i].present_damage,
                                               choose_area[i].remain_health), end='')
                if choose_area[i].armor > 0:
                    print("[{0}]".format(choose_area[i].armor), end='')
                print("/{0})".format(choose_area[i].present_health), end='')
                if choose_area[i].present_property != '':
                    print("[{0}]".format(choose_area[i].present_property), end='')
                else:
                    print(end='')
                if choose_area[i].hero == 'myhero':
                    print("{友}", end=' ')
                else:
                    print("{敌}", end=' ')
            print('')

            if self.myturn and not isRandom:
                choose_num = choose_direct_num(choose_area, "请选择对象序号：")
            elif isRandom:
                choose_num = randint(1, len(choose_area))

            if card.name == '香蕉':
                if not self.myturn and not isRandom:
                    choose_num = randint(1, len(choose_area))
                print("使用 {0}->{1} {2}-{3} >>> ".format(card.name, choose_area[choose_num - 1].name,
                                                        choose_area[choose_num - 1].present_damage,
                                                        choose_area[choose_num - 1].remain_health), end='')
                choose_area[choose_num - 1].buff_damage += 1
                choose_area[choose_num - 1].update_buff_damage()
                choose_area[choose_num - 1].remain_health += 1
                choose_area[choose_num - 1].present_health += 1
                print(
                    "{0}-{1}".format(choose_area[choose_num - 1].present_damage,
                                     choose_area[choose_num - 1].remain_health))
            elif card.name == '湮灭':
                if not self.myturn and not isRandom:
                    smart_value_order(choose_area, True)
                    for index, choose_card in enumerate(choose_area):
                        if myhero.remain_health + myhero.armor > choose_card.remain_health:
                            choose_num = index + 1
                            break
                print(">>>{0} 消灭了 {1}".format(card.name, choose_area[choose_num - 1].name))
                choose_area[choose_num - 1].alive = False
                print(">>>{0}->{1} 生命值 {2}".format(card.name, myhero.name, myhero.remain_health),
                      end='')
                if myhero.armor > 0:
                    print("[{0}]".format(myhero.armor), end='')
                myhero.reduce_health(choose_area[choose_num - 1].remain_health)
                print("->{0}".format(myhero.remain_health), end='')
                if myhero.armor > 0:
                    print("[{0}]".format(myhero.armor), end='')
                print("")
            elif card.name == '梦境':
                if not self.myturn and not isRandom:
                    smart_value_order(choose_area, True)
                    choose_num = 0
                print(">>>{0}->{1} 从战场移回手牌".format(card.name, choose_area[choose_num - 1].name))
                choose_area[choose_num - 1].reset()
                if choose_area[choose_num - 1].hero == 'myhero':
                    self.myhandcards.append(choose_area[choose_num - 1])
                    self.myworldcards.remove(choose_area[choose_num - 1])
                else:
                    self.enemyhandcards.append(choose_area[choose_num - 1])
                    self.enemyworldcards.remove(choose_area[choose_num - 1])
            elif card.name == '梦魇':
                if not self.myturn and not isRandom:
                    smart_mana_order(choose_area)
                    choose_num = -1
                print(">>>{0}->{1} {2}-{3}/{4}->".format(card.name, choose_area[choose_num - 1].name,
                                                         choose_area[choose_num - 1].present_damage,
                                                         choose_area[choose_num - 1].remain_health,
                                                         choose_area[choose_num - 1].present_health), end='')
                choose_area[choose_num - 1].buff_damage += 5
                choose_area[choose_num - 1].update_buff_damage()
                choose_area[choose_num - 1].remain_health += 5
                choose_area[choose_num - 1].present_health += 5
                print("{0}-{1}/{2}".format(choose_area[choose_num - 1].present_damage,
                                           choose_area[choose_num - 1].remain_health,
                                           choose_area[choose_num - 1].present_health))
                if self.myturn:
                    if choose_area[choose_num - 1].present_property == '':
                        choose_area[choose_num - 1].present_property = 'MyNightmare'
                    else:
                        choose_area[choose_num - 1].present_property += ' MyNightmare'
                else:
                    if choose_area[choose_num - 1].present_property == '':
                        choose_area[choose_num - 1].present_property = 'EnemyNightmare'
                    else:
                        choose_area[choose_num - 1].present_property += ' EnemyNightmare'
            elif card.name == '标记射击':
                if not self.myturn and not isRandom:
                    if search_for_health(choose_area, 4, 5, False):
                        smart_value_order(choose_area, True)
                        for index, choose_card in enumerate(choose_area):
                            if choose_card.remain_health + choose_card.armor <= 4:
                                choose_num = index + 1
                                break
                    else:
                        choose_num = randint(1, len(choose_area))
                if len(choose_area) > 0:
                    print(">>>{0}->{1} {2}->".format(card.name, choose_area[choose_num - 1].name,
                                                     choose_area[choose_num - 1].remain_health), end='')
                    choose_area[choose_num - 1].reduce_health(4)
                    print("{0}".format(choose_area[choose_num - 1].remain_health))
                hunter_magic_list = search_occupation_type(get_card_pool(), 'Hunter', 'Magic')
                random_hunter_magic = random.sample(hunter_magic_list, 3)
                for i in range(len(random_hunter_magic)):
                    print("{0}-{1}".format(i + 1, random_hunter_magic[i].name), end=' ')
                print('')
                if self.myturn and not isRandom:
                    choose_num = choose_direct_num(random_hunter_magic, "请选择对象序号：")
                else:
                    choose_num = randint(1, len(random_hunter_magic))
                if len(myhandcards) < HANDCARDNUM:
                    print(">>>{0} -> {1}".format(card.name, random_hunter_magic[choose_num - 1].name))
                    myhandcards.append(random_hunter_magic[choose_num - 1])
            elif card.name == '凶猛狂暴':
                if not self.myturn and not isRandom:
                    smart_value_order(choose_area, True)
                    choose_num = 1
                print(">>>{0}->{1} {2}-{3}/{4}->".format(card.name, choose_area[choose_num - 1].name,
                                                         choose_area[choose_num - 1].present_damage,
                                                         choose_area[choose_num - 1].remain_health,
                                                         choose_area[choose_num - 1].present_health), end='')
                choose_area[choose_num - 1].buff_damage += 3
                choose_area[choose_num - 1].update_buff_damage()
                choose_area[choose_num - 1].remain_health += 3
                choose_area[choose_num - 1].present_health += 3
                print("{0}-{1}/{2}".format(choose_area[choose_num - 1].present_damage,
                                           choose_area[choose_num - 1].remain_health,
                                           choose_area[choose_num - 1].present_health))
                count = 3
                while count > 0:
                    temp_card = parse_card(get_card_info('card_pool.txt', choose_area[choose_num - 1].id).strip('\n'))
                    if self.myturn:
                        temp_card.hero = 'myhero'
                    else:
                        temp_card.hero = 'enemyhero'
                    temp_card.present_damage += 3
                    temp_card.remain_health += 3
                    temp_card.present_health += 3
                    if len(mylibrarycards) > 0:
                        randnum = randint(0, len(mylibrarycards) - 1)
                        mylibrarycards.insert(randnum, temp_card)
                    else:
                        mylibrarycards.append(temp_card)
                    count -= 1
            elif card.name == '死亡缠绕':
                if not self.myturn and not isRandom:
                    smart_value_order(choose_area, True)
                    if search_for_health(choose_area, 5, 5, False):
                        for index, choose_card in enumerate(choose_area):
                            if choose_card.remain_health + choose_card.armor <= 5:
                                choose_num = index + 1
                                break
                    else:
                        choose_num = 1
                print(">>>{0}->{1} 生命值 {2}->".format(card.name, choose_area[choose_num - 1].name,
                                                     choose_area[choose_num - 1].remain_health), end='')
                if choose_area[choose_num - 1].hero == 'myhero':
                    choose_area[choose_num - 1].add_health(5)
                else:
                    choose_area[choose_num - 1].reduce_health(5)
                print("{0}".format(choose_area[choose_num - 1].remain_health))
            elif card.name == '杀戮命令':
                if search_for_race(myworldcards, 'Beast', 1):
                    damage = 5
                else:
                    damage = 3
                if not self.myturn and not isRandom:
                    smart_value_order(choose_area, True)
                    if search_for_health(choose_area, damage, 5, False):
                        for index, choose_card in enumerate(choose_area):
                            if choose_card.remain_health + choose_card.armor <= damage:
                                choose_num = index + 1
                                break
                    else:
                        choose_num = 1
                print(">>>{0}->{1} {2}".format(card.name, choose_area[choose_num - 1].name,
                                               choose_area[choose_num - 1].remain_health), end='')
                if choose_area[choose_num - 1].armor > 0:
                    print("[{0}]".format(choose_area[choose_num - 1].armor), end='')
                choose_area[choose_num - 1].reduce_health(damage)
                print("->{0}".format(choose_area[choose_num - 1].remain_health), end='')
                if choose_area[choose_num - 1].armor > 0:
                    print("[{0}]".format(choose_area[choose_num - 1].armor), end='')
                print('')
        else:
            if card.name == '幸运币':
                print(">>>使用幸运币！")
                if self.current_mana < 10:
                    self.current_mana += 1
            elif card.name == '死亡之握':
                if self.myturn:
                    follower_list = search_type(self.enemycards, 'Follower')
                    if len(follower_list) != 0:
                        random_num = randint(0, len(follower_list) - 1)
                        print(">>>{0} -> {1}".format(card.name, follower_list[random_num]))
                        follower_list[random_num].hero = 'myhero'
                        self.myhandcards.append(follower_list[random_num])
                        self.enemycards.remove(follower_list[random_num])
                else:
                    follower_list = search_type(self.mycards, 'Follower')
                    if len(follower_list) != 0:
                        random_num = randint(0, len(follower_list) - 1)
                        print(">>>{0} -> {1}".format(card.name, follower_list[random_num].name))
                        follower_list[random_num].hero = 'enemyhero'
                        self.enemyhandcards.append(follower_list[random_num])
                        self.mycards.remove(follower_list[random_num])
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
            elif card.name == '反魔法护罩':
                if self.myturn:
                    for worldcard in self.myworldcards:
                        print(">>>{0}->{1} {2}-{3}/{4}->".format(card.name, worldcard.name, worldcard.present_damage,
                                                                 worldcard.remain_health, worldcard.present_health),
                              end='')
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
                                                                 worldcard.remain_health, worldcard.present_health),
                              end='')
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
            elif card.name == '伊瑟拉的觉醒':
                print(">>>{0}->{1} 生命值 {2}".format(card.name, self.myhero.name, self.myhero.remain_health), end='')
                if self.myhero.armor > 0:
                    print("[{0}]".format(self.myhero.armor), end='')
                self.myhero.reduce_health(5)
                print("->{0}".format(self.myhero.remain_health), end='')
                if self.myhero.armor > 0:
                    print("[{0}]".format(self.myhero.armor), end='')
                print("")
                print(">>>{0}->{1} 生命值 {2}".format(card.name, self.enemyhero.name, self.enemyhero.remain_health),
                      end='')
                if self.enemyhero.armor > 0:
                    print("[{0}]".format(self.enemyhero.armor), end='')
                self.enemyhero.reduce_health(5)
                print("->{0}".format(self.enemyhero.remain_health), end='')
                if self.enemyhero.armor > 0:
                    print("[{0}]".format(self.enemyhero.armor), end='')
                print("")
                for worldcard in self.myworldcards:
                    if worldcard.name != '伊瑟拉':
                        print(">>>{0}->{1}(我方随从) 生命值 {2}".format(card.name, worldcard.name, worldcard.remain_health),
                              end='')
                        worldcard.reduce_health(5)
                        print("->{0}".format(worldcard.remain_health))
                for worldcard in self.enemyworldcards:
                    if worldcard.name != '伊瑟拉':
                        print(">>>{0}->{1}(敌方随从) 生命值 {2}".format(card.name, worldcard.name, worldcard.remain_health),
                              end='')
                        worldcard.reduce_health(5)
                        print("->{0}".format(worldcard.remain_health))
            elif card.name == '托林的酒杯':
                flag = False
                if len(myhandcards) < HANDCARDNUM:
                    flag = True
                self.draw_card()
                if flag:
                    copy_card = myhandcards[-1]
                    print(">>>{0} -> {1}".format(card.name, copy_card.name))
                    while len(myhandcards) < HANDCARDNUM:
                        myhandcards.append(copy_card)
            elif card.name == '神奇的魔杖':
                card_num = 3
                while card_num > 0:
                    flag = False
                    if len(myhandcards) < HANDCARDNUM:
                        flag = True
                    self.draw_card()
                    if flag:
                        myhandcards[-1].present_mana = 0
                        print()
                    card_num -= 1
            elif card.name == '扎罗格的皇冠':
                choose_followers = random.sample(search_color(get_card_pool(), 'golden'), 3)
                for i in range(len(choose_followers)):
                    print("{0}-{1}({2}-{3}/{4})".format(i + 1, choose_followers[i].name,
                                                        choose_followers[i].present_damage,
                                                        choose_followers[i].remain_health,
                                                        choose_followers[i].present_health), end='')
                    if choose_followers[i].present_property != '':
                        print("[{0}]".format(choose_followers[i].present_property), end=' ')
                    else:
                        print(end=' ')
                print('')
                if self.myturn and not isRandom:
                    choose_num = choose_object_num(choose_followers, "请选择要发现的对象序号：")
                else:
                    choose_num = randint(1, 3)
                print(">>>{0} -> {1}".format(card.name, choose_followers[choose_num - 1].name))
                count = 3
                while count > 0 and len(myworldcards) < WORLDCARDNUM:
                    myworldcards.append(
                        parse_card(get_card_info('card_pool.txt', choose_followers[choose_num - 1].id).strip('\n')))
                    if self.myturn:
                        myworldcards[-1].hero = 'myhero'
                    else:
                        myworldcards[-1].hero = 'enemyhero'
                    count -= 1
            elif card.name == '追踪术':
                choose_cards = []
                count = 3
                while count > 0 and len(mylibrarycards) > 0:
                    top_card = mylibrarycards[0]
                    mylibrarycards.remove(top_card)
                    choose_cards.append(top_card)
                    count -= 1
                if len(choose_cards) > 0:
                    for i in range(len(choose_cards)):
                        print("{0}-{1}".format(i + 1, choose_cards[i].name), end=' ')
                    print('')
                    if self.myturn and not isRandom:
                        choose_num = choose_object_num(choose_cards, "请选择要发现的对象序号：")
                    else:
                        choose_num = randint(1, len(choose_cards))
                    print(">>>{0} -> {1}".format(card.name, choose_cards[choose_num - 1].name))
                    if len(myhandcards)<HANDCARDNUM:
                        myhandcards.append(choose_cards[choose_num - 1])
            elif card.name == '致命射击':
                if len(oppoworldcards) > 0:
                    rand_follower = random.sample(oppoworldcards, 1)[0]
                    rand_follower.alive = False
                    print(">>>{0} -> {1}".format(card.name, rand_follower.name))
            elif card.name == '关门放狗':
                print(">>>{0}".format(card.name))
                count = len(oppoworldcards)
                while count > 0 and len(myworldcards) < WORLDCARDNUM:
                    myworldcards.append(parse_card(get_card_info('card_pool.txt', 1132).strip('\n')))
                    if self.myturn:
                        myworldcards[-1].hero = 'myhero'
                    else:
                        myworldcards[-1].hero = 'enemyhero'
                    count -= 1
            elif card.name == '动物伙伴':
                rand_id = random.sample([1133, 1134, 1135], 1)[0]
                if len(myworldcards) < WORLDCARDNUM:
                    myworldcards.append(parse_card(get_card_info('card_pool.txt', rand_id).strip('\n')))
                    if self.myturn:
                        myworldcards[-1].hero = 'myhero'
                    else:
                        myworldcards[-1].hero = 'enemyhero'
                    print(">>>{0} -> {1}".format(card.name, myworldcards[-1].name))
            elif card.name == '主人的召唤':
                follower_list = search_type(mylibrarycards, 'Follower')
                follower_list = remove_duplicate(follower_list)
                if len(follower_list) >= 3:
                    rand_follower = random.sample(follower_list, 3)
                elif 0 < len(follower_list) < 3:
                    rand_follower = follower_list
                else:
                    return
                if search_for_race(rand_follower, 'Beast', 2):
                    for rand_card in rand_follower:
                        if len(myhandcards) < HANDCARDNUM:
                            print(">>>{0} -> {1}".format(card.name, rand_card.name))
                            myhandcards.append(rand_card)
                            mylibrarycards.remove(rand_card)
                        else:
                            print(">>>手牌已满，【{0}】被摧毁！".format(rand_card.name))
                else:
                    for i in range(len(rand_follower)):
                        print(
                            "{0}-{1}({2}-{3}/{4})".format(i + 1, rand_follower[i].name, rand_follower[i].present_damage,
                                                          rand_follower[i].remain_health,
                                                          rand_follower[i].present_health), end='')
                        if rand_follower[i].present_property != '':
                            print("[{0}]".format(rand_follower[i].present_property), end=' ')
                        else:
                            print(end=' ')
                    print('')
                    if self.myturn and not isRandom:
                        choose_num = choose_direct_num(rand_follower, "请选择对象序号：")
                    else:
                        choose_num = randint(1, len(rand_follower))
                    if len(myhandcards) < HANDCARDNUM:
                        myhandcards.append(rand_follower[choose_num - 1])
                        print(">>>{0} -> {1}".format(card.name, rand_follower[choose_num - 1].name))
            elif card.name == '猛兽出笼':
                if card.present_property.find('Twice') != -1:
                    card.present_property = card.present_property.replace('Twice', '').strip()
                    myhandcards.append(card)
                if len(myworldcards) < WORLDCARDNUM:
                    fly_dragon = parse_card(get_card_info('card_pool.txt', 1136).strip('\n'))
                    if self.myturn:
                        fly_dragon.hero = 'myhero'
                    else:
                        fly_dragon.hero = 'enemyhero'
                    myworldcards.append(fly_dragon)
                    print(">>>{0} -> {1}".format(card.name, myworldcards[-1].name))

    def auto_usehandcard(self):
        """
        敌方使用手牌
        :return: 
        """
        print("-----------------剩余水晶为:{0}".format(self.current_mana))
        can_use_list = self.can_use_handcard(self.enemyhero, self.myhero, self.enemyworldcards, self.myworldcards,
                                             self.enemyhandcards, self.myhandcards, self.enemycards, self.mycards,
                                             self.enemyweapon, self.myweapon)

        select = self.current_mana - can_use_list[0].present_mana
        index = 0
        if len(can_use_list) > 1:
            for i in range(1, len(can_use_list)):
                select2 = self.current_mana - can_use_list[i].present_mana
                if select > select2:
                    select = select2
                    index = i
        print("^^^^敌方手牌^^^^^^^^^^^^")
        show_cards(self.enemyhandcards)
        temp_handcard = can_use_list[index]
        self.current_mana -= temp_handcard.present_mana
        self.enemyhandcards.remove(can_use_list[index])
        if temp_handcard.type == 'Follower':
            if temp_handcard.present_property.find('Battlecry') != -1:
                self.battle_cry(temp_handcard, self.enemyhero, self.myhero,
                                self.enemyworldcards, self.myworldcards, self.enemyhandcards,
                                self.myhandcards, self.enemycards, self.mycards, self.enemyweapon, self.myweapon)
            else:
                self.enemyworldcards.append(temp_handcard)
                print(">>>>>>{0}({1})".format(temp_handcard.name,
                                              temp_handcard.present_mana), end='')
                if temp_handcard.present_property != '':
                    print("[{0}]".format(temp_handcard.present_property), end='')
                print("上场！！！")
        elif temp_handcard.type == 'Magic':
            self.enemyhero.cast_list.append(temp_handcard)
            self.cast(temp_handcard, self.enemyhero, self.myhero, self.enemyworldcards, self.myworldcards,
                      self.enemyhandcards, self.myhandcards, self.enemycards, self.mycards, self.enemyweapon,
                      self.myweapon, False)
        elif temp_handcard.type == 'Weapon':
            if self.enemyweapon is not None:
                self.enemyweapon.alive = False
                self.update_weapon()
            self.enemyweapon = temp_handcard
            print(">>>装备 {0}".format(self.enemyweapon.name))
        elif temp_handcard.type == 'Hero':
            if temp_handcard.present_property.find('Battlecry') != -1:
                self.battle_cry(temp_handcard, self.enemyhero, self.myhero,
                                self.enemyworldcards, self.myworldcards, self.enemyhandcards,
                                self.myhandcards, self.enemycards, self.mycards, self.enemyweapon, self.myweapon)

    def attack_who(self, card, cards):
        """
        敌方攻击
        :param card: 
        :param cards: 
        :return: 
        """
        if not self.myturn:
            taunt_list = search_property(cards, 'Taunt', 1, False)
            if len(taunt_list) > 0:
                attack_card = smart_attack(card, taunt_list)
            else:
                not_stealth_list = search_property(cards, 'Stealth', 2, False)
                if len(not_stealth_list) > 0:
                    smart_property_order(not_stealth_list, True)
                    attack_card = smart_attack(card, not_stealth_list)
            return attack_card


def main():
    game = World()
    game.say_hi()
    game.who_first()
    game.turn_round()


if __name__ == '__main__':
    main()
