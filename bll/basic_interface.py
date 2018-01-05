# coding=utf-8
"""
synopsis: cmdb basic interface
author: haoranzeus@gmail.com (zhanghaoran)
"""

from mysqldal import models
from utils.context import Context
from mysqldal import schema
from mysqldal import sql_engine
from . import query_schema
from .exceptions import QueryParameterError
from .api_utils import query_sort, pagination

context = Context()


def api_idc_list(condiction_dict):
    """
    获取机房列表
    """
    query_dict = condiction_dict['action']
    q_dict, error = query_schema.PageQueryBaseSchema().load(query_dict)
    if error != {}:
        raise QueryParameterError('参数错误: {}'.format(error))

    # session = context.Session()
    # q_res = session.query(models.Idc)
    # total = q_res.count()   # 总计
    # q_res = query_sort(q_res, q_dict)
    # q_res = pagination(q_res, q_dict)

    # idc_schema = schema.IdcSchema(many=True, exclude=('rack', ))
    # res, error = idc_schema.dump(q_res)
    # data = {
    #     'total': total,
    #     'rows': res
    # }
    # session.close()

    with sql_engine.session_scope() as session:
        q_res = session.query(models.Idc)
        total = q_res.count()   # 总计
        q_res = query_sort(q_res, q_dict)
        q_res = pagination(q_res, q_dict)

        idc_schema = schema.IdcSchema(many=True, exclude=('rack', ))
        res, error = idc_schema.dump(q_res)

    data = {
        'total': total,
        'rows': res
    }

    return data


def api_idc_add(condiction_dict):
    """
    新增机房
    """
    query_list = condiction_dict['action']
    q_list, error = schema.IdcSchema(many=True).load(query_list)
    session = context.Session()
    
