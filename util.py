#!/usr/bin/python3
# -*- coding: utf-8 -*-


# 替换非法字符
from datetime import datetime
from os import path


def replace(resource):

    return resource.strip()\
        .replace('.', '_')\
        .replace('-', '_')\
        .replace('#', '')\
        .replace(' ', '')\
        .replace('(', '')\
        .replace(')', '') \
        .replace('（', '') \
        .replace('）', '') \
        .replace('(Top)', '')\
        .replace('#OC2VBB_Position', 'OC2VBB_Position2')\
        .replace('测温方案', 'thermometer')\
        .replace('中英文对照', 'translate')

def replace4columns(resource):
    return resource.strip()\
        .replace('.', '_')\
        .replace('-', '_')\
        .replace('#', '')\
        .replace(' ', '')\
        .replace('(', '')\
        .replace(')', '')\
        .replace('（', '')\
        .replace('）', '')\
        .replace('(Top)', '')\
        .replace('进线功能单元', 'oc_incoming_line')\
        .replace('测温等级', 'oc_thermometer_level')


def gen_time():
    """生成时间字符串
    """
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H-%M-%S")


def write2txt(content):
    """
    追加日志
    :param content:
    :return:
    """
    file = path.join(path.expanduser("~"), 'Desktop') + '/log.txt'
    with open(file, 'a+') as f:
        f.write(gen_time() + '\n' + content + '\n')


def get_desktop_path():
    """
    获取用户Desktop路径
    :return:
    """
    return path.join(path.expanduser("~"), 'Desktop')


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False
