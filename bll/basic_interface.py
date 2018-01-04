# coding=utf-8
"""
synopsis: cmdb basic interface
author: haoranzeus@gmail.com (zhanghaoran)
"""
from sqlalchemy import desc
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker

from mysqldal import models
from utils.context import Context
from utils.str_tools import str_add_quot
from mysqldal import schema
from . import query_schema
from .exceptions import QueryParameterError

context = Context()


def api_idc_list(condiction_dict):
    query_dict = condiction_dict['action']
    q_dict, error = query_schema.PageQueryBaseSchema().load(query_dict)
    if error != {}:
        raise QueryParameterError('参数错误: {}'.format(error))

    session = context.Session()
    q_res = session.query(models.Idc)
    total = q_res.count()   # 总计

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

    # 分页参数
    size = q_dict.get('size', 10000)
    index = q_dict.get('index', 0)
    page_head = index * size
    page_tail = (index+1) * size
    q_res = q_res[page_head:page_tail]

    idc_schema = schema.IdcSchema(many=True, exclude=('rack', ))
    res = idc_schema.dump(q_res)
    data = {
        'total': total,
        'rows': res
    }
    session.close()
    return data
