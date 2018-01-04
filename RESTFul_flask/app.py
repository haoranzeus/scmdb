# coding=utf-8
"""
synopsis: flask app.
author: haoranzeus@gmail.com (zhanghaoran)
"""
import logging
import os
from flask import Flask
from flask_restful import Api, Resource

from . import flask_handles
from utils.context import Context


app = Flask(__name__)
api = Api(app)
_log = logging.getLogger(__name__)
context = Context()


class Hello(Resource):
    def get(self):
        print(context.conf_dict['scmdb']['url_root'])
        return {'hello': 'name'}


def app_init():
    """
    集中设置路由
    """
    url_base = context.conf_dict['scmdb']['url_root']
    routers = [
        (Hello, 'hello/'),
        (flask_handles.idc_list, 'idc_list/')
    ]

    # 路由注册
    for handle, url in routers:
        api.add_resource(handle, os.path.join(url_base, url))


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
