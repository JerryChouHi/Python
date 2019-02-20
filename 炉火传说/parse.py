# encoding:utf-8
# @Time     : 2019/2/14 15:48
# @Author   : Jerry Chou
# @File     : parse.py
# @Function :

from card import Card


def parse_card(str):
    """
    从字符串中解析卡牌属性，创建卡牌对象
    :param str: 
    :return: 
    """
    member = str.split(',')
    try:
        return Card(member[0], member[1], member[2], int(member[3]), int(member[4]), int(member[5]))
    except Exception as e:
        print(e)
