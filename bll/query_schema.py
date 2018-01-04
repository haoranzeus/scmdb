# coding=utf-8
"""
synopsis: query paramaters schema
author: haoranzeus@gmail.com (zhanghaoran)
"""
from marshmallow import Schema, fields, validates

from .exceptions import QueryParameterError


class NestedQuerySchema(Schema):
    precise = fields.Dict()
    fuzzy = fields.Dict()


class NestedSortSchema(Schema):
    sort = fields.String()
    sort_field = fields.String(required=True)
    priority = fields.Integer(required=True)

    @validates('sort')
    def validate_sort(self, value):
        if value not in ['asc', 'desc']:
            raise QueryParameterError('sort must be "asc" or "desc"')


class PageQueryBaseSchema(Schema):
    index = fields.Integer()
    size = fields.Integer()
    sorts = fields.Nested('NestedSortSchema', many=True)
    query = fields.Nested('NestedQuerySchema')
