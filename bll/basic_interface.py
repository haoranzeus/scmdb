# coding=utf-8
"""
synopsis: cmdb basic interface
author: haoranzeus@gmail.com (zhanghaoran)
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from mysqldal import models
from utils.context import Context
from mysqldal import schema

context = Context()


def api_idc_list(condiction_dict):
    query_dict = condiction_dict['action']
    session = context.Session()
    a = session.query(models.Idc)
    idc_schema = schema.IdcSchema(many=True)
    res = idc_schema.dump(a.all())
    session.close()
    return res
