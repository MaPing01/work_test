#coding:utf-8

import logging
import os
import json
import sys
import  logging.config


def setup_logging(default_path='logging.conf',default_level=logging.DEBUG):
    path = default_path
    if os.path.exists(path):
        with open(path,'r') as f:
            config = json.load(f)
            logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)




setup_logging(sys.path[0]+'/logconfig.conf')
logging.info('test')