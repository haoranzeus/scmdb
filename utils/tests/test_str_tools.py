# coding=utf-8
from datetime import datetime
from nose.tools import assert_equal

from utils.str_tools import datetime_format
from utils.str_tools import now_format


class TestDatetimeFormat:
    def test1(self):
        res = datetime_format(datetime.now(), 'mysql')
        print(res)


class TestNowFormat:
    def test1(self):
        res = now_format('mysql')
        print(res)
