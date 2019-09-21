# encoding:utf-8
# @Time     : 2019/2/13 17:24
# @Author   : Jerry Chou
# @File     : card.py
# @Function : 攻击目标如果是英雄，攻击方不受伤害
#             增加加血、减血方法

import random
from common import *
from random import randint


class Card(object):
    def __init__(self, id, name, race, property, damage, health, mana, color, type, occupation=None,
                 SpecialMagic=None, hero=None):
        self.id = id
        self.name = name
        self.race = race
        self.color = color
        self.type = type
        self.occupation = occupation
        self.hero = hero
        # 初始值
        self.property = property
        self.health = health
        self.damage = damage
        self.mana = mana
        self.armor = 0
        self.value = 0
        if self.property.find('WindAngry') != -1:
            self.attack_count = 2
        else:
            self.attack_count = 1
        # 当前值
        self.present_property = property
        self.remain_health = health
        self.present_health = health
        self.present_damage = damage
        self.present_attack_count = self.attack_count
        self.present_mana = mana
        # 临时值
        self.change_damage = 0
        self.halo_damage = 0
        self.buff_damage = 0
        # 其它
        self.alive = True
        if self.property.find('Rush') != -1 or self.property.find('Charge') != -1:
            self.sleep = False
        else:
            self.sleep = True

        self.SpecialMagic = SpecialMagic

    def reset(self):
        # 当前值
        self.present_property = self.property
        self.remain_health = self.health
        self.present_health = self.health
        self.present_damage = self.damage
        self.present_attack_count = self.attack_count
        self.present_mana = self.mana
        # 临时值
        self.change_damage = 0
        self.halo_damage = 0
        self.buff_damage = 0
        # 其它
        self.alive = True
        if self.property.find('Rush') != -1 or self.property.find('Charge') != -1:
            self.sleep = False
        else:
            self.sleep = True

    def update_halo_damage(self):
        """
        更新光环伤害
        :return: 
        """
        self.present_damage += self.halo_damage

    def reset_halo_damage(self):
        """
        返回当前回合光环的伤害
        :return: 
        """
        self.present_damage -= self.halo_damage
        self.halo_damage = 0

    def reset_property(self, property):
        """
        重置属性
        :return: 
        """
        if self.property.find(property) == -1:
            self.present_property = self.present_property.replace(property, '').strip()

    def add_property(self, property):
        """
        增加属性
        :param property: 
        :return: 
        """
        if self.property.find(property) == -1:
            if self.present_property == '':
                self.present_property = property
            elif self.present_property.find(property) == -1:
                self.present_property += (' ' + property)

    def update_buff_damage(self):
        """
        更新buff伤害
        :return: 
        """
        self.present_damage += self.buff_damage
        self.buff_damage = 0

    def reset_attack_count(self):
        """
        重置攻击次数
        :return: 
        """
        self.present_attack_count = self.attack_count

    def reset_change_damage(self):
        """
        返回当前回合变更的伤害
        :return: 
        """
        self.present_damage -= self.change_damage
        self.change_damage = 0

    def attack(self, oppo, myhero=None, oppohero=None):
        """
        物理攻击
        :param oppo: 
        :param myhero: 
        :param oppohero: 
        :return: 
        """
        over_kill = False
        self.present_attack_count -= 1
        # 我方是英雄
        if self.type == 'Hero':
            # 敌方是英雄
            if oppo.type == 'Hero':
                # 敌方英雄受伤
                oppo.reduce_health(self.present_damage)
            else:
                # 我方英雄受伤
                self.reduce_health(oppo.present_damage)
                # 敌方卡牌没有圣盾
                if oppo.present_property.find('DivineShield') == -1:
                    # 敌方卡牌受伤
                    oppo.reduce_health(self.present_damage)
                    if oppo.remain_health < 0:
                        over_kill = True
                else:
                    # 敌方卡牌破盾
                    oppo.present_property = oppo.present_property.replace('DivineShield', '').strip()
                # 敌方卡牌有吸血
                if oppo.present_property.find('BloodSucking') != -1:
                    # 敌方英雄回血
                    print("{0} 回血：{1}->".format(oppohero.name, oppohero.remain_health), end='')
                    oppohero.add_health(oppo.present_damage)
                    print("{0}".format(oppohero.remain_health))
        else:
            # 敌方是英雄
            if oppo.type == 'Hero':
                # 敌方英雄受伤
                oppo.reduce_health(self.present_damage)
                # 我方卡牌有吸血
                if self.present_property.find('BloodSucking') != -1:
                    # 我方英雄回血
                    print("{0} 回血：{1}->".format(myhero.name, myhero.remain_health), end='')
                    myhero.add_health(self.present_damage)
                    print("{0}".format(myhero.remain_health))
                if self.name == '凶恶的雏龙':
                    evolution = ['+3攻', '+3血', '+1攻+1血', '风怒', '潜行', '嘲讽']
                    choose_list = random.sample(evolution, 3)
                    for index, item in enumerate(choose_list):
                        print("{0}.{1}".format(index + 1, item), end=' ')
                    print("")
                    if self.hero == 'myhero':
                        choose = input_int("请选择进化的序号：")
                    elif self.hero == 'enemyhero':
                        choose = randint(1, 6)
                    if choose_list[choose - 1] == '+3攻':
                        print("{0} 的攻击力 {1} >>>".format(self.name, self.present_damage), end='')
                        self.buff_damage += 3
                        self.update_buff_damage()
                        print("{0}".format(self.present_damage))
                    elif choose_list[choose - 1] == '+3血':
                        print("{0} 生命值 {1}/{2} >>>".format(self.name, self.remain_health, self.present_health), end='')
                        self.remain_health += 3
                        self.present_health += 3
                        print("{0}/{1}".format(self.remain_health, self.present_health))
                    elif choose_list[choose - 1] == '+1攻+1血':
                        print("{0} {1}-{2}/{3} >>>".format(self.name, self.present_damage, self.remain_health,
                                                           self.present_health), end='')
                        self.buff_damage += 1
                        self.update_buff_damage()
                        self.remain_health += 1
                        self.present_health += 1
                        print("{0}-{1}/{2}".format(self.present_damage, self.remain_health, self.present_health))
                    elif choose_list[choose - 1] == '风怒':
                        if self.present_property.find('WindAngry') == -1:
                            print("{0} 获得 风怒".format(self.name))
                            self.present_property += ' WindAngry'
                            self.present_attack_count += 1
                            self.attack_count = 2
                    elif choose_list[choose - 1] == '潜行':
                        if self.present_property.find('Stealth') == -1:
                            print("{0} 获得 潜行".format(self.name))
                            self.present_property += ' Stealth'
                    elif choose_list[choose - 1] == '嘲讽':
                        if self.present_property.find('Taunt') == -1:
                            print("{0} 获得 嘲讽".format(self.name))
                            self.present_property += ' Taunt'
            else:
                # 敌方卡牌没有圣盾
                if oppo.present_property.find('DivineShield') == -1:
                    # 敌方卡牌受伤
                    oppo.reduce_health(self.present_damage)
                    if oppo.remain_health < 0:
                        over_kill = True
                    # 我方卡牌有吸血
                    if self.present_property.find('BloodSucking') != -1:
                        # 我方英雄回血
                        print("{0} 回血：{1}->".format(myhero.name, myhero.remain_health), end='')
                        myhero.add_health(self.present_damage)
                        print("{0}".format(myhero.remain_health))
                    # 我方卡牌有剧毒
                    if self.present_property.find('Toxic') != -1:
                        # 敌方卡牌死亡
                        oppo.alive = False
                else:
                    # 敌方卡牌破盾
                    oppo.present_property = oppo.present_property.replace('DivineShield', '').strip()

                # 我方卡牌没有圣盾
                if self.present_property.find('DivineShield') == -1:
                    # 我方卡牌受伤
                    self.reduce_health(oppo.present_damage)
                    # 敌方卡牌有吸血
                    if oppo.present_property.find('BloodSucking') != -1:
                        # 敌方英雄回血
                        print("{0} 回血：{1}->".format(oppohero.name, oppohero.remain_health), end='')
                        oppohero.add_health(oppo.present_damage)
                        print("{0}".format(oppohero.remain_health))
                    # 敌方卡牌有剧毒
                    if oppo.present_property.find('Toxic') != -1:
                        # 我方卡牌死亡
                        self.alive = False
                else:
                    if oppo.present_damage > 0:
                        # 我方卡牌破盾
                        self.present_property = self.present_property.replace('DivineShield', '').strip()

            # 如果我方卡牌是潜行状态
            if self.present_property.find('Stealth') != -1:
                # 我方卡牌潜行状态消失
                self.present_property = self.present_property.replace('Stealth', '').strip()
        if self.present_property.find('Charge') != -1:
            self.present_property = self.present_property.replace('Charge', '').strip()
        return over_kill

    def add_health(self, blood):
        """
        加血
        :param blood: 
        :return: 
        """
        if self.remain_health <= self.present_health - blood:
            self.remain_health += blood
        else:
            self.remain_health = self.present_health

    def reduce_health(self, blood):
        """
        优先破盾，然后减甲，最后减血
        :param blood: 
        :return: 
        """
        if self.present_property.find('DivineShield') == -1:
            if self.armor > blood:
                self.armor -= blood
            else:
                self.remain_health -= (blood - self.armor)
                self.armor = 0
            self.update()
        else:
            self.present_property = self.present_property.replace('DivineShield', '').strip()

    def update(self):
        """
        更新卡牌是否死亡
        :return: 
        """
        if self.remain_health <= 0:
            self.alive = False

    def show(self):
        """
        打印当前卡牌的状态
        :return: 
        """
        if self.type == 'Follower' or self.type == 'Hero':
            if self.alive:
                print("{0}({1})".format(self.name, self.present_mana), end='')
                if self.present_property != '':
                    print("[{0}]".format(self.present_property), end='')
                if self.sleep:
                    print("--sleep")
                else:
                    print("")
                print("\t攻击力：{0}".format(self.present_damage))
                print("\t生命值：{0}".format(self.remain_health), end='')
                if self.armor > 0:
                    print("[{0}]".format(self.armor))
                else:
                    print("")
            else:
                print("%s 已死亡" % (self.name))
        else:
            print("{0}({1})".format(self.name, self.present_mana))
