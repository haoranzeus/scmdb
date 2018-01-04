# coding=utf-8
"""
synopsis: some other tools
author: haoranzeus@gmail.com (zhanghaoran)
"""
import codecs
import os
import yaml


def get_api_conf(conf_path):
    """
    从配置文件路径将api.yaml文件转换为字典
    """
    api_conf = os.path.join(conf_path, 'api.yaml')
    with codecs.open(api_conf, 'r', 'utf-8') as conff:
        api_conf_dict = yaml.load(conff)
    return api_conf_dict
