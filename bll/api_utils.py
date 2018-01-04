# coding=utf-8
"""
synopsis: utils used for api processes
author: haoranzeus@gmail.com (zhanghaoran)
"""
from sqlalchemy import desc
from sqlalchemy import text

from utils.str_tools import str_add_quot


def query_sort(q_res, q_dict):
    """
    针对sqlalchemy的基础查询结果进行查询和排序
    paras:
        q_res - sqlalchemy的查询结果
        q_dict - 传入的标准查询参数
    """
    # 查询参数
    query = q_dict.get('query', {})
    precise = query.get('precise', {})
    fuzzy = query.get('fuzzy', {})
    for k, v in precise.items():
        sql_str = '{k}={v}'.format(k=k, v=str_add_quot(v))
        q_res = q_res.filter(text(sql_str))
    for k, v in fuzzy.items():
        sql_str = '{k} like {v}'.format(k=k, v=str_add_quot(v))
        q_res = q_res.filter(text(sql_str))

    # 排序参数
    sorts = q_dict.get('sorts', [{'sort_field': 'id', 'priority': 1}, ])
    sorts.sort(key=lambda n: n['priority'])
    for sort in sorts:
        order = sort.get('sort', 'asc')
        if order == 'asc':
            q_res = q_res.order_by(sort['sort_field'])
        else:
            q_res = q_res.order_by(desc(sort['sort_field']))

    return q_res


def pagination(q_res, q_dict):
    """
    针对sqlalchemy的基础查询结果进行分页
    paras:
        q_res - sqlalchemy的查询结果
        q_dict - 传入的标准查询参数
    """
    # 分页参数
    size = q_dict.get('size', 10000)
    index = q_dict.get('index', 0)
    page_head = index * size
    page_tail = (index+1) * size
    q_res = q_res[page_head:page_tail]

    return q_res
