# encoding:utf-8
# @Time     : 2019/5/13 9:27
# @Author   : Jerry Chou
# @File     : common.py
# @Function : 公共方法


def show_cards(cards):
    """
    显示卡牌
    :param cards: 
    :return: 
    """
    for i, card in enumerate(cards):
        print("\t{0}-{1}({2})".format(i + 1, card.name, card.present_mana), end='')
        if card.present_property != '':
            print("[{0}]".format(card.present_property))
        else:
            print("")


def input_int(desc):
    """
    整数输入
    :param desc: 
    :return: 
    """
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
    if search_for_property(direct_list, 'AntiMagic', 1, True):
        if direct_list[direct_num - 1].present_property.find('AntiMagic') != -1:
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
    if search_for_property(attack_list, 'Taunt', 1, False):
        if attack_list[attack_num - 1].present_property.find('Taunt') == -1:
            print("必须攻击具有嘲讽属性的卡牌！")
            return choose_attack_num(attack_list, desc)
    if search_for_property(attack_list, 'Stealth', 1, True):
        if attack_list[attack_num - 1].present_property.find('Stealth') != -1:
            print("潜行的卡牌无法被攻击！")
            return choose_attack_num(attack_list, desc)
    return attack_num


def search_for_damage(card_list, damage, calc, includeStealth):
    """
    是否存在相应攻击力的卡牌
    :param card_list: 
    :param calc: 1-等于 2-大于 3-小于 4-大于等于 5-小于等于
    :param damage: 
    :param includeStealth: True 包含隐藏   False 不包含隐藏
    :return: 
    """
    if calc == 1:
        for card in card_list:
            if includeStealth:
                if card.present_damage == damage:
                    return True
            else:
                if card.present_damage == damage and card.present_property.find('Stealth') == -1:
                    return True
    elif calc == 2:
        for card in card_list:
            if includeStealth:
                if card.present_damage > damage:
                    return True
            else:
                if card.present_damage > damage and card.present_property.find('Stealth') == -1:
                    return True
    elif calc == 3:
        for card in card_list:
            if includeStealth:
                if card.present_damage < damage:
                    return True
            else:
                if card.present_damage < damage and card.present_property.find('Stealth') == -1:
                    return True
    elif calc == 4:
        for card in card_list:
            if includeStealth:
                if card.present_damage >= damage:
                    return True
            else:
                if card.present_damage >= damage and card.present_property.find('Stealth') == -1:
                    return True
    elif calc == 5:
        for card in card_list:
            if includeStealth:
                if card.present_damage <= damage:
                    return True
            else:
                if card.present_damage <= damage and card.present_property.find('Stealth') == -1:
                    return True
    return False


def search_for_health(card_list, health, calc, includeStealth):
    """
    是否存在相应生命值的卡牌
    :param card_list: 
    :param calc: 1-等于 2-大于 3-小于 4-大于等于 5-小于等于
    :param health: 
    :param includeStealth: True 包含隐藏   False 不包含隐藏
    :return: 
    """
    if calc == 1:
        for card in card_list:
            if includeStealth:
                if card.remain_health == health:
                    return True
            else:
                if card.remain_health == health and card.present_property.find('Stealth') == -1:
                    return True
    elif calc == 2:
        for card in card_list:
            if includeStealth:
                if card.remain_health > health:
                    return True
            else:
                if card.remain_health > health and card.present_property.find('Stealth') == -1:
                    return True
    elif calc == 3:
        for card in card_list:
            if includeStealth:
                if card.remain_health < health:
                    return True
            else:
                if card.remain_health < health and card.present_property.find('Stealth') == -1:
                    return True
    elif calc == 4:
        for card in card_list:
            if includeStealth:
                if card.remain_health >= health:
                    return True
            else:
                if card.remain_health >= health and card.present_property.find('Stealth') == -1:
                    return True
    elif calc == 5:
        for card in card_list:
            if includeStealth:
                if card.remain_health <= health:
                    return True
            else:
                if card.remain_health <= health and card.present_property.find('Stealth') == -1:
                    return True
    return False


def search_for_id(card_list, card_id):
    """
    从指定的列表中查询卡牌id是否存在
    :param card_id: 
    :param card_list: 
    :return: 
    """
    index_list = []
    for index, card in enumerate(card_list):
        if card.id == card_id:
            index_list.append(index)
    return index_list


def search_for_race(card_list, card_race, calc):
    """
    从指定的列表中查询卡牌种族
    :param card_race: 
    :param card_list: 
    :param calc: 1-存在  2-全部都是
    :return: 
    """
    if calc == 1:
        for card in card_list:
            if card.race == card_race:
                return True
        return False
    elif calc == 2:
        for card in card_list:
            if card.race != card_race:
                return False
        return True


def search_for_property(card_list, card_property, calc, includeStealth):
    """
    从指定的列表中查询卡牌属性
    :param card_property: 
    :param card_list: 
    :param calc: 1-包含  2-不包含
    :param includeStealth: True 包含隐藏   False 不包含隐藏
    :return: 
    """
    if calc == 1:
        for card in card_list:
            if includeStealth:
                if card.present_property.find(card_property) != -1:
                    return True
            else:
                if card.present_property.find(card_property) != -1 and card.present_property.find('Stealth') == -1:
                    return True
    elif calc == 2:
        if len(card_list) == 0:
            return True
        else:
            for card in card_list:
                if includeStealth:
                    if card.present_property.find(card_property) == -1:
                        return True
                else:
                    if card.present_property.find(card_property) == -1 and card.present_property.find('Stealth') == -1:
                        return True
    return False


def search_damage(card_list, damage):
    """
    找到攻击力为damage的卡牌
    :param card_list: 
    :param damage: 
    :return: 
    """
    search_result = []
    for card in card_list:
        if card.present_damage == damage:
            search_result.append(card)
    return search_result


def search_race(card_list, card_race):
    """
    从指定的列表中查询卡牌种族
    :param card_race: 
    :param card_list: 
    :return: 
    """
    search_result = []
    for card in card_list:
        if card.race == card_race:
            search_result.append(card)
    return search_result


def search_property(card_list, card_property, calc, includeStealth):
    """
    从指定的列表中查询卡牌属性
    :param card_property: 
    :param card_list: 
    :param calc: 1-包含  2-不包含
    :param includeStealth: True 包含隐藏   False 不包含隐藏
    :return: 
    """
    search_result = []
    if calc == 1:
        for card in card_list:
            if includeStealth:
                if card.present_property.find(card_property) != -1:
                    search_result.append(card)
            else:
                if card.present_property.find(card_property) != -1 and card.present_property.find('Stealth') == -1:
                    search_result.append(card)
    elif calc == 2:
        for card in card_list:
            if includeStealth:
                if card.present_property.find(card_property) == -1:
                    search_result.append(card)
            else:
                if card.present_property.find(card_property) == -1 and card.present_property.find('Stealth') == -1:
                    search_result.append(card)
    return search_result


def search_color(card_list, card_color):
    """
    从指定的列表中查询卡牌成色
    :param card_color: 
    :param card_list: 
    :return: 
    """
    search_result = []
    for card in card_list:
        if card.color == card_color:
            search_result.append(card)
    return search_result


def search_type(card_list, card_type):
    """
    从指定的列表中查询卡牌类型
    :param card_type: 
    :param card_list: 
    :return: 
    """
    search_result = []
    for card in card_list:
        if card.type == card_type:
            search_result.append(card)
    return search_result


def search_hero(card_list, hero):
    """
    从指定的列表中查询所属阵营
    :param card_list: 
    :param hero: 
    :return: 
    """
    search_result = []
    for card in card_list:
        if card.hero == hero:
            search_result.append(card)
    return search_result


def search_occupation(card_list, card_occupation):
    """
    从指定的列表中查询卡牌所属
    :param card_occupation: 
    :param card_list: 
    :return: 
    """
    search_result = []
    for card in card_list:
        if card.occupation == card_occupation:
            search_result.append(card)
    return search_result


def search_occupation_type(card_list, card_occupation, card_type):
    """
    从指定的列表中查询卡牌所属的卡牌类型
    :param card_list: 
    :param card_occupation: 
    :param card_type: 
    :return: 
    """
    search_result = []
    for card in card_list:
        if card.occupation == card_occupation and card.type == card_type:
            search_result.append(card)
    return search_result


def smart_attack(my_card, card_list):
    """
    智能攻击
    :param my_card: 
    :param card_list: 
    :return: 
    """
    my_remain_health = my_card.remain_health + my_card.armor - card_list[0].present_damage
    attack_card_remain_health = card_list[0].remain_health + card_list[0].armor - my_card.present_damage
    attack_card = card_list[0]
    if len(card_list) > 1:
        for card in card_list[1:]:
            my_health = my_card.remain_health + my_card.armor - card.present_damage
            attack_health = card.remain_health + card.armor - my_card.present_damage
            if not (my_health <= 0 and attack_health > 0) and (
                                    (attack_health <= attack_card_remain_health and my_health >= my_remain_health) or (
                                                attack_health <= attack_card_remain_health and 0 < my_health < my_remain_health) or (
                                            attack_health <= 0 <= attack_card_remain_health) or (
                                            attack_card_remain_health <= attack_health <= 0 and my_health >= my_remain_health) or (
                                            attack_card_remain_health <= attack_health <= 0 and 0 < my_health < my_remain_health and card.present_damage >= attack_card.present_damage)):
                my_remain_health = my_health
                attack_card_remain_health = attack_health
                attack_card = card
    return attack_card


def all_smart_attack_one(card_list, attack_card):
    """
    多打一
    :param card_list: 
    :param attack_card: 
    :return: 
    """
    total_present_damage = 0
    attack_list = []
    smart_value_order(card_list, False)
    if search_for_damage(card_list, attack_card.remain_health + attack_card.armor, 4, True):
        smart_damage_order(card_list)
        if (card_list[0].remain_health + card_list[0].armor > attack_card.present_damage and card_list[
            0].value <= 5 * attack_card.value) or (
                            card_list[0].remain_health + card_list[0].armor <= attack_card.present_damage and card_list[
                    0].value <= 3 * attack_card.value):
            return [card_list[0]]
    else:
        for card in card_list:
            total_present_damage += card.present_damage
            attack_list.append(card)
            if total_present_damage >= attack_card.remain_health + attack_card.armor:
                return attack_list


def all_smart_attack_all(attack_list, beaten_list):
    """
    多打多
    :param attack_list: 
    :param beaten_list: 
    :return: 击打双方
    """
    smart_value_order(beaten_list, True)
    for follower in beaten_list:
        attack_follower_list = all_smart_attack_one(attack_list, follower)
        if attack_follower_list is not None:
            return attack_follower_list[0], follower


def smart_property_order(card_list, order):
    """
    特殊属性排序，相同属性血量高的前置
    :param order: True 特殊属性前置  False 特殊属性后置
    :param card_list: 
    :return: 
    """
    length = len(card_list)
    for i in range(length):
        temp = card_list[i]
        for j in range(i + 1, length):
            if order:
                if (card_list[i].present_property == '' and card_list[j].present_property != '') or (
                                card_list[i].present_property.find('Taunt') == -1 and card_list[
                            j].present_property.find(
                            'Taunt') != -1) or (
                                card_list[i].present_property == card_list[j].present_property and card_list[
                            i].remain_health <
                            card_list[j].remain_health):
                    card_list[i] = card_list[j]
                    card_list[j] = temp
                    temp = card_list[i]
            else:
                if (card_list[i].present_property != '' and card_list[j].present_property == '') or (
                                card_list[i].present_property.find('Taunt') != -1 and card_list[
                            j].present_property.find(
                            'Taunt') == -1):
                    card_list[i] = card_list[j]
                    card_list[j] = temp
                    temp = card_list[i]


def smart_damage_order(card_list):
    """
    攻击从大到小排列，相同攻击力（血量多的、有突袭的前置）
    :param card_list: 
    :return: 
    """
    length = len(card_list)
    for i in range(length):
        temp = card_list[i]
        for j in range(i + 1, length):
            if (card_list[i].present_damage < card_list[j].present_damage) or (
                            card_list[i].present_damage == card_list[j].present_damage and (card_list[i].remain_health <
                                                                                                card_list[
                                                                                                    j].remain_health or
                                                                                                    card_list[
                                                                                                        j].present_property.find(
                                                                                                        'Rush') != -1)):
                card_list[i] = card_list[j]
                card_list[j] = temp
                temp = card_list[i]


def smart_mana_order(card_list):
    """
    法力值从大到小排列
    :param card_list: 
    :return: 
    """
    length = len(card_list)
    for i in range(length):
        temp = card_list[i]
        for j in range(i + 1, length):
            if card_list[i].mana < card_list[j].mana:
                card_list[i] = card_list[j]
                card_list[j] = temp
                temp = card_list[i]


def smart_health_order(card_list):
    """
    生命值从大到小排列，生命值相同，把有属性的对象排在前面
    :param card_list: 
    :return: 
    """
    length = len(card_list)
    for i in range(length):
        temp = card_list[i]
        for j in range(i + 1, length):
            if (card_list[i].remain_health < card_list[j].remain_health) or (
                                card_list[i].remain_health == card_list[j].remain_health and card_list[
                            i].present_property == '' and card_list[j].present_property != ''):
                card_list[i] = card_list[j]
                card_list[j] = temp
                temp = card_list[i]


def smart_value_order(card_list, order):
    """
    根据卡牌价值排序
    :param order: True 从大到小  False 从小到大
    :param card_list: 
    :return: 
    """
    length = len(card_list)
    for i in range(length):
        temp = card_list[i]
        for j in range(i + 1, length):
            if order:
                if card_list[i].value < card_list[j].value or (
                                card_list[i].value == card_list[j].value and card_list[i].present_damage < card_list[
                            j].present_damage):
                    card_list[i] = card_list[j]
                    card_list[j] = temp
                    temp = card_list[i]
            else:
                if card_list[i].value > card_list[j].value or (
                                card_list[i].value == card_list[j].value and card_list[i].present_damage > card_list[
                            j].present_damage):
                    card_list[i] = card_list[j]
                    card_list[j] = temp
                    temp = card_list[i]


def remove_duplicate(card_list):
    """
    去重
    :param card_list: 
    :return: 
    """
    li = []
    for item in card_list:
        for li_item in li:
            if item.name == li_item.name:
                break
        else:
            li.append(item)
    return li


def cal_value(card):
    """
    计算卡牌的价值
    :param card: 
    :return: 
    """
    value = card.present_damage + card.remain_health * 0.5
    if card.present_property.find('Special') != -1 or card.present_property.find(
            'MyRoundBegin') != -1 or card.present_property.find(
        'MyRoundEnd') != -1 or card.present_property.find('EveryRoundEnd') != -1:
        value *= 5
    if card.present_property.find('Halo') != -1 or card.present_property.find(
            'Toxic') != -1 or card.present_property.find('WindAngry') != -1:
        value *= 4
    if card.present_property.find('BloodSucking') != -1 or card.present_property.find(
            'DivineShield') != -1 or card.present_property.find('AntiMagic') != -1:
        value *= 1.5
    return value
