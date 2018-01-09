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
        (flask_handles.idc_list, 'idc_list/'),
        (flask_handles.idc_add, 'idc_add/'),
        (flask_handles.idc_del, 'idc_del/'),
        (flask_handles.idc_update, 'idc_update/'),
        (flask_handles.rack_add, 'rack_add/'),
        (flask_handles.rack_del, 'rack_del/'),
        (flask_handles.rack_list, 'rack_list/'),
        (flask_handles.rack_update, 'rack_update/'),
        (flask_handles.server_add, 'server_add/'),
        (flask_handles.server_del, 'server_del/'),
        (flask_handles.server_list, 'server_list/'),
        (flask_handles.server_update, 'server_update/'),
        (flask_handles.vm_add, 'vm_add/'),
        (flask_handles.vm_del, 'vm_del/'),
        (flask_handles.vm_list, 'vm_list/'),
        (flask_handles.vm_update, 'vm_update/'),
    ]

    # 路由注册
    for handle, url in routers:
        api.add_resource(handle, os.path.join(url_base, url))


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
