# coding=utf-8
"""
synopsis: program entry
author: haoranzeus@gmail.com (zhanghaoran)
"""
import codecs
import getopt
import logging.config
import os
import sys
import yaml

from mysqldal.sql_engine import sql_init
from RESTFul_flask.app import app
from RESTFul_flask.app import app_init
from utils.context import Context


def usage():
    print('some usage information')


def main(argv):
    try:
        opts, args = getopt.getopt(
                argv, "c:", ["configure=", "help"])
    except getopt.GetoptError:
        usage()
        sys.exit()

    conf_path = os.path.join(os.path.abspath("."), 'configs/conf')
    for opt, arg in opts:
        if opt == '--help':
            usage()
            sys.exit()
        elif opt in ('-c', '--configure'):
            conf_path = arg
        else:
            usage()
            exit()

    def _exit_w_info(info):
        print('\n%s\n' % info)
        usage()
        exit()

    def _ok_conf(conf):
        def check_cfg(cfg):
            cpath = os.path.join(conf, cfg)
            return ((os.path.exists(cpath) and cpath)
                    or _exit_w_info('missing %s.' % cpath))
        return [check_cfg(cfg) for cfg in ('api.yaml', 'logging.yaml')]

    api_conf, logging_conf = _ok_conf(conf_path)
    app_conf = {}
    with codecs.open(logging_conf, 'r', 'utf-8') as logging_file:
        log_conf_dict = yaml.load(logging_file)
        logfile_path = os.path.split(
                log_conf_dict['handlers']['file']['filename'])[0]
        if not os.path.exists(logfile_path):
            os.makedirs(logfile_path)
        logging.config.dictConfig(log_conf_dict)
    with codecs.open(api_conf, 'r', 'utf-8') as conff:
        app_conf.update(yaml.load(conff))

    context = Context()
    context.init(app_conf)
    app_init()
    sql_init()
    app.run(host="0.0.0.0", debug=True)


if __name__ == '__main__':
    args = sys.argv[1:]
    main(args)
