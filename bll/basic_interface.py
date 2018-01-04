# coding=utf-8
"""
synopsis: cmdb basic interface
author: haoranzeus@gmail.com (zhanghaoran)
"""
from sqlalchemy import desc
from sqlalchemy import text

from mysqldal import models
from utils.context import Context
from utils.str_tools import str_add_quot
from mysqldal import schema
from . import query_schema
from .exceptions import QueryParameterError
from .api_utils import query_sort, pagination

context = Context()


def api_idc_list(condiction_dict):
    query_dict = condiction_dict['action']
    q_dict, error = query_schema.PageQueryBaseSchema().load(query_dict)
    if error != {}:
        raise QueryParameterError('参数错误: {}'.format(error))

    session = context.Session()
    q_res = session.query(models.Idc)
    total = q_res.count()   # 总计
    q_res = query_sort(q_res, q_dict)
    q_res = pagination(q_res, q_dict)

    idc_schema = schema.IdcSchema(many=True, exclude=('rack', ))
    res = idc_schema.dump(q_res)
    data = {
        'total': total,
        'rows': res
    }
    session.close()
    return data
