# encoding:utf-8
# @Time     : 2019/2/14 15:48
# @Author   : Jerry Chou
# @File     : parse.py
# @Function :

from card import Card
from hero import Hero

def parse_card(str):
    """
    从字符串中解析卡牌属性，创建卡牌对象
    :param str: 
    :return: 
    """
    member = str.split(',')
    try:
        if member[8]=='Follower':
            return Card(int(member[0]), member[1], member[2], member[3], int(member[4]), int(member[5]),
                        int(member[6]), member[7], member[8], member[9], member[10],member[11])
        if member[8]=='Hero':
            return Hero(member)
        else:
            return Card(int(member[0]), member[1], member[2], member[3], member[4], member[5],
                        int(member[6]), member[7], member[8], member[9], member[10],member[11])
    except Exception as e:
        print(e)
