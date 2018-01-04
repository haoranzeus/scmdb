# coding=utf-8
"""
synopsis: context use to share information
author: haoranzeus@gmail.com (zhanghaoran)
"""
from utils.singleton import Singleton


class Context(metaclass=Singleton):
    """
    上下文环境，用于不同文件之间共享信息
    """
    def __init__(self):
        super(Context, self).__init__()

    def init(self, conf_dict):
        self._conf_dict = conf_dict

    @property
    def conf_dict(self):
        return self._conf_dict
