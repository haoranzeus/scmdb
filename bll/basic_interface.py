# coding=utf-8
"""
synopsis: cmdb basic interface
author: haoranzeus@gmail.com (zhanghaoran)
"""
import logging
import sqlalchemy
from functools import wraps

from mysqldal import models
from utils.context import Context
from mysqldal import schema
from mysqldal import sql_engine
from . import query_schema
from .exceptions import ParameterError
from .exceptions import QueryParameterError
from .exceptions import InsertParameterError
from .exceptions import UpdateParameterError
from .exceptions import DeleteParameterError
from .api_utils import query_sort, pagination

context = Context()
_log = logging.getLogger(__name__)


def base_parameter_check(func):
    """
    对传入的参数形式进行基本检测
    """
    @wraps(func)
    def wrapper(condiction_dict, *args, **kwargs):
        condiction_dict, error = query_schema.BaseParameterSchema().load(
                condiction_dict)
        if error != {}:
            raise ParameterError('parameter error: {}'.format(str(error)))
        return func(condiction_dict, *args, **kwargs)
    return wrapper


# =====================================================================
# 机房操作
# =====================================================================
@base_parameter_check
def api_idc_list(condiction_dict):
    """
    获取机房列表
    """
    condiction_dict, error = query_schema.BaseParameterSchema().load(
            condiction_dict)
    query_dict = condiction_dict['action']
    q_dict, error = query_schema.PageQueryBaseSchema().load(query_dict)
    if error != {}:
        raise QueryParameterError('参数错误: {}'.format(error))

    with sql_engine.session_scope() as session:
        q_res = session.query(models.Idc)
        total = q_res.count()   # 总计
        q_res = query_sort(q_res, q_dict)
        q_res = pagination(q_res, q_dict)

        ci_schema = schema.IdcSchema(many=True, exclude=('rack', ))
        res, error = ci_schema.dump(q_res)

    data = {
        'total': total,
        'rows': res
    }

    return data


@base_parameter_check
def api_idc_add(condiction_dict):
    """
    新增机房
    """
    query_list = condiction_dict['action']
    q_list, error = schema.IdcSchema(
            many=True, exclude=('id', )).load(query_list)
    if error != {}:
        raise InsertParameterError('参数错误: {}'.format(error))
    ci_items = [models.Idc(**item) for item in q_list]
    with sql_engine.session_scope() as session:
        session.add_all(ci_items)


@base_parameter_check
def api_idc_del(condiction_dict):
    """
    删除机房
    参数是一个id列表组成的list
    """
    query_list = condiction_dict['action']
    if not isinstance(query_list, list):
        raise DeleteParameterError('参数错误，必须为int组成的列表')
    if not query_schema.NormalVerify.intlist(query_list):
        raise DeleteParameterError('参数错误，必须为int组成的列表')
    with sql_engine.session_scope() as session:
        session.query(models.Idc).filter(
                models.Idc.id.in_(query_list)).delete(
                        synchronize_session=False)


@base_parameter_check
def api_idc_update(condiction_dict):
    """
    编辑机房
    condiction_dict =
    {
        'action': [
            {
                'id': 1,
                'name': xxx,
                ...
            },
            {
                'id': 2,
                ...
            }
        ]
    }
    每个object中id是必填项
    """
    query_list = condiction_dict['action']
    para_list = []
    for item in query_list:
        q_dict, error = schema.IdcSchema().load(item)
        if error != {}:
            raise UpdateParameterError('parament error: {}'.format(error))
        para_list.append(q_dict)
    with sql_engine.session_scope() as session:
        for para in para_list:
            session.query(models.Idc).filter(
                    models.Idc.id == para['id']).update(para)


# =====================================================================
# 机柜操作
# =====================================================================
@base_parameter_check
def api_rack_add(condiction_dict):
    """
    新增机柜
    """
    query_list = condiction_dict['action']
    q_list, error = schema.RackSchema(
            many=True, exclude=('id', )).load(query_list)
    if error != {}:
        raise InsertParameterError('参数错误: {}'.format(error))
    ci_items = [models.Rack(**item) for item in q_list]
    try:
        with sql_engine.session_scope() as session:
            session.add_all(ci_items)
    except sqlalchemy.exc.IntegrityError as e:
        _log.warning('rack insert failed: %s', str(e.args))
        raise InsertParameterError(
                "Insert failed. Maybe you didn't "
                "choose an valid foreign key id")


@base_parameter_check
def api_rack_del(condiction_dict):
    """
    删除机柜
    参数是一个id列表组成的list
    """
    query_list = condiction_dict['action']
    if not isinstance(query_list, list):
        raise DeleteParameterError('参数错误，必须为int组成的列表')
    if not query_schema.NormalVerify.intlist(query_list):
        raise DeleteParameterError('参数错误，必须为int组成的列表')
    with sql_engine.session_scope() as session:
        session.query(models.Rack).filter(
                models.Rack.id.in_(query_list)).delete(
                        synchronize_session=False)


@base_parameter_check
def api_rack_list(condiction_dict):
    """
    获取机柜列表
    """
    condiction_dict, error = query_schema.BaseParameterSchema().load(
            condiction_dict)
    query_dict = condiction_dict['action']
    q_dict, error = query_schema.PageQueryBaseSchema().load(query_dict)
    if error != {}:
        raise QueryParameterError('参数错误: {}'.format(error))

    with sql_engine.session_scope() as session:
        q_res = session.query(models.Rack)
        total = q_res.count()   # 总计
        q_res = query_sort(q_res, q_dict)
        q_res = pagination(q_res, q_dict)

        ci_schema = schema.RackSchema(many=True, exclude=('server', ))
        res, error = ci_schema.dump(q_res)

    data = {
        'total': total,
        'rows': res
    }

    return data


@base_parameter_check
def api_rack_update(condiction_dict):
    """
    编辑机房
    condiction_dict =
    {
        'action': [
            {
                'id': 1,
                'rackcode': xxx,
                ...
            },
            {
                'id': 2,
                ...
            }
        ]
    }
    每个object中id是必填项
    """
    query_list = condiction_dict['action']
    para_list = []
    for item in query_list:
        q_dict, error = schema.RackSchema().load(item)
        if error != {}:
            raise UpdateParameterError('parament error: {}'.format(error))
        para_list.append(q_dict)
    with sql_engine.session_scope() as session:
        for para in para_list:
            session.query(models.Rack).filter(
                    models.Rack.id == para['id']).update(para)


# =====================================================================
# 物理机操作
# =====================================================================
@base_parameter_check
def api_server_add(condiction_dict):
    """
    新增物理机
    """
    query_list = condiction_dict['action']
    q_list, error = schema.ServerSchema(
            many=True, exclude=('id', )).load(query_list)
    if error != {}:
        raise InsertParameterError('参数错误: {}'.format(error))
    ci_items = [models.Server(**item) for item in q_list]
    try:
        with sql_engine.session_scope() as session:
            session.add_all(ci_items)
    except sqlalchemy.exc.IntegrityError as e:
        _log.warning('server insert failed: %s', str(e.args))
        raise InsertParameterError(
                "Insert failed. Maybe you didn't "
                "choose an valid foreign key id")


@base_parameter_check
def api_server_del(condiction_dict):
    """
    删除物理机
    参数是一个id列表组成的list
    """
    query_list = condiction_dict['action']
    if not isinstance(query_list, list):
        raise DeleteParameterError('参数错误，必须为int组成的列表')
    if not query_schema.NormalVerify.intlist(query_list):
        raise DeleteParameterError('参数错误，必须为int组成的列表')
    with sql_engine.session_scope() as session:
        session.query(models.Server).filter(
                models.Server.id.in_(query_list)).delete(
                        synchronize_session=False)


@base_parameter_check
def api_server_list(condiction_dict):
    """
    获取物理机列表
    """
    condiction_dict, error = query_schema.BaseParameterSchema().load(
            condiction_dict)
    query_dict = condiction_dict['action']
    q_dict, error = query_schema.PageQueryBaseSchema().load(query_dict)
    if error != {}:
        raise QueryParameterError('参数错误: {}'.format(error))

    with sql_engine.session_scope() as session:
        q_res = session.query(models.Server)
        total = q_res.count()   # 总计
        q_res = query_sort(q_res, q_dict)
        q_res = pagination(q_res, q_dict)

        ci_schema = schema.ServerSchema(many=True, exclude=('server', ))
        res, error = ci_schema.dump(q_res)

    data = {
        'total': total,
        'rows': res
    }

    return data


@base_parameter_check
def api_server_update(condiction_dict):
    """
    编辑物理机
    condiction_dict =
    {
        'action': [
            {
                'id': 1,
                'name': xxx,
                ...
            },
            {
                'id': 2,
                ...
            }
        ]
    }
    每个object中id是必填项
    """
    query_list = condiction_dict['action']
    para_list = []
    for item in query_list:
        q_dict, error = schema.ServerSchema().load(item)
        if error != {}:
            raise UpdateParameterError('parament error: {}'.format(error))
        para_list.append(q_dict)
    with sql_engine.session_scope() as session:
        for para in para_list:
            session.query(models.Server).filter(
                    models.Server.id == para['id']).update(para)


# =====================================================================
# 虚拟机操作
# =====================================================================
@base_parameter_check
def api_vm_add(condiction_dict):
    """
    新增虚拟机
    """
    query_list = condiction_dict['action']
    q_list, error = schema.VmSchema(
            many=True, exclude=('id', )).load(query_list)
    if error != {}:
        raise InsertParameterError('参数错误: {}'.format(error))
    ci_items = [models.Vm(**item) for item in q_list]
    try:
        with sql_engine.session_scope() as session:
            session.add_all(ci_items)
    except sqlalchemy.exc.IntegrityError as e:
        _log.warning('server insert failed: %s', str(e.args))
        raise InsertParameterError(
                "Insert failed. Maybe you didn't "
                "choose an valid foreign key id")


@base_parameter_check
def api_vm_del(condiction_dict):
    """
    删除虚拟机
    参数是一个id列表组成的list
    """
    query_list = condiction_dict['action']
    if not isinstance(query_list, list):
        raise DeleteParameterError('参数错误，必须为int组成的列表')
    if not query_schema.NormalVerify.intlist(query_list):
        raise DeleteParameterError('参数错误，必须为int组成的列表')
    with sql_engine.session_scope() as session:
        session.query(models.Vm).filter(
                models.Vm.id.in_(query_list)).delete(
                        synchronize_session=False)


@base_parameter_check
def api_vm_list(condiction_dict):
    """
    获取虚拟机列表
    """
    condiction_dict, error = query_schema.BaseParameterSchema().load(
            condiction_dict)
    query_dict = condiction_dict['action']
    q_dict, error = query_schema.PageQueryBaseSchema().load(query_dict)
    if error != {}:
        raise QueryParameterError('参数错误: {}'.format(error))

    with sql_engine.session_scope() as session:
        q_res = session.query(models.Vm)
        total = q_res.count()   # 总计
        q_res = query_sort(q_res, q_dict)
        q_res = pagination(q_res, q_dict)

        ci_schema = schema.VmSchema(many=True, exclude=('server', ))
        res, error = ci_schema.dump(q_res)

    data = {
        'total': total,
        'rows': res
    }

    return data


@base_parameter_check
def api_vm_update(condiction_dict):
    """
    编辑虚拟机
    condiction_dict =
    {
        'action': [
            {
                'id': 1,
                'name': xxx,
                ...
            },
            {
                'id': 2,
                ...
            }
        ]
    }
    每个object中id是必填项
    """
    query_list = condiction_dict['action']
    para_list = []
    for item in query_list:
        q_dict, error = schema.VmSchema().load(item)
        if error != {}:
            raise UpdateParameterError('parament error: {}'.format(error))
        para_list.append(q_dict)
    with sql_engine.session_scope() as session:
        for para in para_list:
            session.query(models.Vm).filter(
                    models.Vm.id == para['id']).update(para)
