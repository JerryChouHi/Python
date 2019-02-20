# encoding:utf-8
# @Time     : 2019/2/13 17:24
# @Author   : Jerry Chou
# @File     : card.py
# @Function :

class Card(object):
    def __init__(self, name, race, property, damage, health, mana):
        self.name = name
        self.race = race
        self.property = property
        self.health = health
        self.damage = damage
        self.alive = True
        self.remain_health = health
        self.mana = mana

    def attack(self, obj):
        """
        攻击一个卡牌，计算 剩余生命=剩余生命-对方攻击力
        :param obj: 
        :return: 
        """
        self.remain_health = self.remain_health - obj.damage
        obj.remain_health = obj.remain_health - self.damage
        self.update()
        obj.update()

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
        if self.alive:
            print("%s(%s)" % (self.name, self.mana))
            print("\t攻击力：", self.damage)
            print("\t生命值：", self.remain_health)
        else:
            print("%s 已死亡" % (self.name))
