from utils.tools import get_api_conf


class TestGetApiConf:
    def test1(self):
        res = get_api_conf('/home/zhr/work/cmcc/scmdb/configs/conf')
        print(res)
