import os
import sys


project_path = os.path.abspath(
    os.path.join(os.path.abspath(os.path.dirname(__file__)), "../.."))
sys.path.append(project_path)


# 加入工程环境
from mysqldal.sql_engine import sql_init

from bll import basic_interface
from mysqldal.models import Idc
from mysqldal.tests import fixture
from utils.context import Context
from utils.tools import get_api_conf


# 上下文初始化
conf_path = os.path.join(os.path.abspath("."), '../configs/conf')
api_conf = get_api_conf(conf_path)
context = Context()
context.init(api_conf)
sql_init()


class TestApiIdcList:
    def setup(self):
        self.session = context.Session()
        self.idc1 = Idc(**fixture.IDC1)
        self.session.add(self.idc1)
        self.session.commit()

    def teardown(self):
        self.session.delete(self.idc1)

    def test1(self):
        condiction_dict = {
            'auth': {},
            'action': {
                'index': 1,
                'size': 1,
                'query': {
                    'precise': {
                        'district': '上城区',
                        'stars': 5
                    },
                    'fuzzy': {
                        'name': '%红山%'
                    }
                },
                'sorts': [
                    {
                        'sort_field': 'stars',
                        'priority': 1
                    },
                    {
                        'sort_field': 'id',
                        'priority': 1
                    }
                ]
            }
        }
        res = basic_interface.api_idc_list(condiction_dict)
        print(res)
