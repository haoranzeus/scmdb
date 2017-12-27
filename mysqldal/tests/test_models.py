# coding=utf-8
import sqlalchemy
from nose.tools import assert_equal
from nose.tools import assert_raises
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text

from mysqldal.models import Idc
from mysqldal.models import Rack
from mysqldal.models import Server
from mysqldal.models import Vm


engine = create_engine(
        'mysql+pymysql://root:123456@localhost:3306/scmdb_test?charset=utf8',
        echo=True)
Session = sessionmaker(bind=engine)


IDC1 = {
    'name': '红山机房',
    'address': '红山机房的地址',
    'status': '正常',
    'contact': '张三',
    'telephone': '13344445555',
    'floor': '1,2',
    'province': '浙江省',
    'city': '杭州市',
    'district': '上城区',
    'operator': '中国移动',
    'stars': 5
}

RACK1 = {
    'rackcode': 'A01',
    'floor': '1',
    'room': '001'
}

RACK2 = {
    'rackcode': 'A02',
    'floor': '1',
    'room': '002'
}

SERVER1 = {
    'name': 'server1',
    'brand': '浪潮',
    'sn': '1234567890',
}

SERVER2 = {
    'name': 'server2',
    'brand': 'IBM',
    'sn': '0123456789',
}

VM1 = {
    'name': 'vm1',
    'end_date': '2018-10-03 22:59:52'
}

VM2 = {
    'name': 'vm2',
    'end_date': '2018-11-03 22:59:52'
}


class TestIdc:
    def setup(self):
        self.idc1 = Idc(**IDC1)
        self.session = Session()

    def teardown(self):
        self.session.delete(self.idc1)
        self.session.commit()
        self.session.close()

    def test_create(self):
        assert_equal('红山机房', self.idc1.name)
        self.session.add(self.idc1)
        self.session.commit()


class TestRack:
    def setup(self):
        self.session = Session()
        self.idc1 = Idc(**IDC1)
        self.rack1 = Rack(**RACK1)
        self.rack2 = Rack(**RACK2)

    def teardown(self):
        with engine.connect() as con:
            con.execute(text('delete from rack'))
            con.execute(text('delete from idc'))
        self.session.close()

    def test_rack(self):
        self.idc1.rack = [self.rack1, self.rack2]
        self.session.add(self.idc1)
        self.session.commit()
        self.session.delete(self.idc1)
        with assert_raises(sqlalchemy.exc.IntegrityError):
            # 外键约束，机柜没删不准删idc
            self.session.commit()


class TestServer:
    def setup(self):
        self.session = Session()
        self.idc1 = Idc(**IDC1)
        self.rack1 = Rack(**RACK1)
        self.rack2 = Rack(**RACK2)
        self.server1 = Server(**SERVER1)
        self.server2 = Server(**SERVER2)

    def teardown(self):
        with engine.connect() as con:
            con.execute(text('delete from server'))
            con.execute(text('delete from rack'))
            con.execute(text('delete from idc'))
        self.session.close()

    def test_server(self):
        self.idc1.rack = [self.rack1, self.rack2]
        self.rack2.server = [self.server1, self.server2]
        self.session.add(self.idc1)
        self.session.commit()

        s_get = self.session.query(Server).filter_by(name='server1').first()
        assert_equal(s_get.sn, SERVER1['sn'])


class TestVm:
    def setup(self):
        self.session = Session()
        self.idc1 = Idc(**IDC1)
        self.rack1 = Rack(**RACK1)
        self.rack2 = Rack(**RACK2)
        self.server1 = Server(**SERVER1)
        self.server2 = Server(**SERVER2)
        self.vm1 = Vm(**VM1)
        self.vm2 = Vm(**VM2)

    def teardown(self):
        self.session.close()

    def test_vm(self):
        self.idc1.rack = [self.rack1, self.rack2]
        self.rack2.server = [self.server1, self.server2]
        self.server1.vm = [self.vm1, self.vm2]
        self.session.add(self.idc1)
        self.session.commit()
