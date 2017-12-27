# coding=utf-8
"""
synopsis: string format tools
author: haoranzeus@gmail.com (zhanghaoran)
"""
from datetime import datetime


def datetime_format(dtime, format_type):
    """
    按需求格式化时间
    paras:
        dtime - 一个datetime.datetime实例
        format_type - 字符串，可以是['mysql', ]
    """
    FORMAT_TYPE = ['mysql', ]
    assert isinstance(dtime, datetime)
    assert format_type in FORMAT_TYPE
    return dtime.strftime('%Y-%m-%d %H:%M:%S')


def now_format(format_type):
    """
    格式化当前时间
    paras:
        format_type - 字符串，可以是['mysql', ]
    """
    return datetime_format(datetime.now(), format_type)
