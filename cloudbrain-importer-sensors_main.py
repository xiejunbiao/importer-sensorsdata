# -*- coding: utf-8 -*-
"""
Created on  6/20 12:58:38 2020

@author: xiejunbiao
"""

from server.cloudbrain_sensorsdata_web_server import start
    
import logging
logger = logging.getLogger()  # # initialize logging class
logger.setLevel(logging.INFO)

if __name__ == '__main__':
    logger.info("starting voice assistant service")
    start()
