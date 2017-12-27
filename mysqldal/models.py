# coding=utf-8
"""
synopsis: sqlalchemy models
author: haoranzeus@gmail.com (zhanghaoran)
"""

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class Idc(Base):
    __tablename__ = 'idc'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, doc='idc名称')
    address = Column(String(100), doc='地址')
    status = Column(String(100), server_default='正常', doc='状态(正常;异常)')
    contact = Column(String(100), doc='联系人')
    telephone = Column(String(100), doc='联系电话')
    floor = Column(String(100), doc='楼层')
    province = Column(String(100), doc='省')
    city = Column(String(100), doc='市')
    district = Column(String(100), doc='区')
    operator = Column(String(100), doc='运营商')
    stars = Column(Integer, default=5, doc='星级')

    rack = relationship('Rack', order_by='Rack.id', back_populates='idc')


class Rack(Base):
    __tablename__ = 'rack'
    id = Column(Integer, primary_key=True)
    rackcode = Column(String(100), nullable=False, doc='机柜号')
    floor = Column(String(100), doc='所在楼层')
    room = Column(String(100), doc='房间号')
    idc_id = Column(
            Integer,
            ForeignKey('idc.id', onupdate='RESTRICT', ondelete='RESTRICT'),
            nullable=False)

    idc = relationship('Idc', back_populates='rack')
    server = relationship(
            'Server', order_by='Server.id', back_populates='rack')


class Server(Base):
    __tablename__ = 'server'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), doc='主机名')
    brand = Column(String(100), doc='品牌')
    model_number = Column(String(100), doc='型号')
    sn = Column(String(100), doc='序列号')
    status = Column(String(100), doc='状态')
    form_factor = Column(String(100), doc='规格')
    multi_thread = Column(String(100), doc='多线程')
    drivers_detail = Column(String(100), doc='磁盘详情')
    console_ip = Column(String(100), doc='控制台ip')
    control_type = Column(String(100), doc='类型')
    affliated_area = Column(String(100), doc='关联区域')
    os = Column(String(100), doc='操作系统')
    ipmi_user = Column(String(100), doc='ipmi密码')
    kvm_ip = Column(String(100), doc='kvmip')
    kvm_pwd = Column(String(100), doc='kvm密码')
    position = Column(String(100), doc='物理位置')
    raid_cache_s = Column(String(100), doc='阵列缓存大小')
    machine_area = Column(String(100), doc='域')
    remark = Column(String(100), doc='备注')
    processors = Column(Integer, doc='处理器数')
    cores = Column(Integer, doc='核数')
    logical_processor = Column(Integer, doc='逻辑核数')
    memory = Column(Integer, doc='内存')
    storage = Column(Integer, doc='磁盘阵列大小')
    rack_id = Column(
            Integer,
            ForeignKey('rack.id', onupdate='RESTRICT', ondelete='RESTRICT'),
            nullable=False)

    rack = relationship('Rack', back_populates='server')
    vm = relationship('Vm', order_by='Vm.id', back_populates='server')


class Vm(Base):
    __tablename__ = 'vm'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, doc='虚拟机名')
    os = Column(String(100), doc='操作系统')
    inner_ip = Column(String(100), doc='内网ip')
    pwd = Column(String(100), doc='密码')
    use = Column(String(100), doc='用途')
    contact = Column(String(100), doc='联系人')
    status = Column(String(100), doc='状态(启用;停用)')
    remarks = Column(String(100), doc='备注')
    wk_no = Column(String(100), doc='工单号')
    server_type = Column(String(100), doc='服务器类型')
    cores = Column(Integer, doc='核数')
    ram = Column(Integer, doc='内存(M)')
    hdd = Column(Integer, doc='磁盘容量')
    assigned_date = Column(DateTime, doc='分配时间')
    end_date = Column(DateTime, doc='到期时间')
    server_id = Column(
            Integer,
            ForeignKey('server.id', onupdate='RESTRICT', ondelete='RESTRICT'),
            nullable=False)

    server = relationship('Server', back_populates='vm')
