# coding=utf-8
from copy import deepcopy
from nose.tools import assert_equal
from mysqldal.schema import IdcSchema

import fixture


class TestIdcSchema:
    def setup(self):
        self.idc1 = deepcopy(fixture.IDC1)
        self.rack1 = deepcopy(fixture.RACK1)
        self.rack2 = deepcopy(fixture.RACK2)
        self.server1 = deepcopy(fixture.SERVER1)
        self.server2 = deepcopy(fixture.SERVER2)
        self.vm1 = deepcopy(fixture.VM1)
        self.vm2 = deepcopy(fixture.VM2)
        self.server1['vm'] = [self.vm1, self.vm2]
        self.rack1['server'] = [self.server1, self.server2]
        self.idc1['rack'] = [self.rack1, self.rack2]

    def test1(self):
        data, err = IdcSchema().load(self.idc1)
        print(data, err)
