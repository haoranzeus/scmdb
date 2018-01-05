# coding=utf-8
"""
synopsis: sqlalchemy engine and session
author: haoranzeus@gmail.com (zhanghaoran)
"""
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from utils.context import Context
context = Context()


def sql_init():
    db_conf = context.conf_dict['scmdb']['cmdb_database']
    sql_alchemy_para = (
        'mysql+pymysql://{usr}:{pwd}@{host}:{port}/{schema}?charset={charset}'
    ).format(
            usr=db_conf['user'], pwd=db_conf['password'], host=db_conf['host'],
            port=3306, schema=db_conf['database'], charset=db_conf['charset']
    )
    context.engine = create_engine(sql_alchemy_para, echo=False)
    context.Session = sessionmaker(bind=context.engine)


@contextmanager
def session_scope():
    session = context.Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
