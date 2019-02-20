# encoding:utf-8
# @Time     : 2019/2/14 15:45
# @Author   : Jerry Chou
# @File     : fight.py
# @Function : 战斗规则

from random import randint


def one_on_one(obj1, obj2, round, obj1_start=0, obj2_start=0):
    """
    两组卡牌，各派一张进入战场，死亡后下一张卡牌进入战场，直到一方卡牌全部死亡
    :param obj1: 
    :param obj2: 
    :param count: 
    :return: 
    """
    if obj1_start < len(obj1) and obj2_start < len(obj2):
        try:
            if (obj1[obj1_start].alive and obj2[obj2_start].alive):
                print("++++++++++第%s回合++++++++++" % (round))
                print("%s%s-%s attack %s%s-%s" % (
                    obj1[obj1_start].name, obj1[obj1_start].damage, obj1[obj1_start].remain_health,
                    obj2[obj2_start].name,
                    obj2[obj2_start].damage, obj2[obj2_start].remain_health))
                print()
                obj1[obj1_start].attack(obj2[obj2_start])
                obj1[obj1_start].show()
                obj2[obj2_start].show()
                round += 1
                one_on_one(obj2, obj1, round, obj2_start, obj1_start)
            elif obj1[obj1_start].alive:
                obj2_start += 1
                if obj2_start < len(obj2):
                    print("++++++++++第%s回合++++++++++" % (round))
                    print("%s%s-%s attack %s%s-%s" % (
                        obj1[obj1_start].name, obj1[obj1_start].damage, obj1[obj1_start].remain_health,
                        obj2[obj2_start].name, obj2[obj2_start].damage, obj2[obj2_start].remain_health))
                    print()
                    obj1[obj1_start].attack(obj2[obj2_start])
                    obj1[obj1_start].show()
                    obj2[obj2_start].show()
                    round += 1
                    one_on_one(obj2, obj1, round, obj2_start, obj1_start)
            elif obj2[obj2_start].alive:
                obj1_start += 1
                if obj1_start < len(obj1):
                    print("++++++++++第%s回合++++++++++" % (round))
                    print("%s%s-%s attack %s%s-%s" % (
                        obj2[obj2_start].name, obj2[obj2_start].damage, obj2[obj2_start].remain_health,
                        obj1[obj1_start].name, obj1[obj1_start].damage, obj1[obj1_start].remain_health))
                    print()
                    obj2[obj2_start].attack(obj1[obj1_start])
                    obj2[obj2_start].show()
                    obj1[obj1_start].show()
                    round += 1
                    one_on_one(obj1, obj2, round, obj1_start, obj2_start)
            else:
                obj1_start += 1
                obj2_start += 1
                one_on_one(obj1, obj2, round, obj1_start, obj2_start)
        except Exception as e:
            print(e)


def battle(obj1, obj2, round):
    """
    两组卡牌，全部进入战场，由一方卡牌随机攻击对方卡牌，交换攻防，直到一方卡牌全部死亡
    :param obj1: 
    :param obj2: 
    :param round: 
    :return: 
    """
    print()
    print("++++++++++第%s回合++++++++++" % (round))
    for obj_a in obj1:
        if obj_a.alive:
            enemy = attack_who(obj2)
            if enemy is not None:
                print("%s%s-%s attack %s%s-%s" % (
                    obj_a.name, obj_a.damage, obj_a.remain_health,
                    enemy.name, enemy.damage, enemy.remain_health))
                obj_a.attack(enemy)
                obj_a.show()
                enemy.show()
    if anybody_alive(obj1) and anybody_alive(obj2):
        round += 1
        battle(obj2, obj1, round)


def attack_who(obj):
    """
    随机找到一个活着的卡牌，如果全部死亡，返回None
    :param obj: 
    :return: 
    """
    attack_obj = obj
    num = randint(0,len(attack_obj)-1)
    if attack_obj[num].alive:
        return attack_obj[num]
    else:
        del attack_obj[num]
        if len(attack_obj)>0:
            return attack_who(attack_obj)
        else:
            return None

    # 顺序检索
    # for attack_obj in obj:
    #     if attack_obj.alive:
    #         return attack_obj
    # return None



def anybody_alive(obj):
    """
    判断一组卡牌是否有存活的
    :param obj: 
    :return: 
    """
    alive = False
    for i in obj:
        alive = alive or i.alive
    return alive
