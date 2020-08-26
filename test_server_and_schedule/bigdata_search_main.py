# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 10:52:40 2020

@author: lijiangman
"""

import sys,logging,multiprocessing
from server.bigdata_search_goods_multi_executors import start
from searchmatch.dianshang_seg_lib import para_set, initPickle 
from searchhotmain.index_create import init_hot_search_test
from searchhotmain.index_schedule import hot_search_schedule
from searchmatch.index_update_cre import iu
from searchmatch.index_schedule_cre import incre_update_schedule

logger = logging.getLogger()    # initialize logging class
logger.setLevel(logging.INFO)

# argv=sys.argv[1:]
# confPath=para_set(argv)

logger.info('initing es index')
iu.index_my_mysql(clean=True)

"""
多进程
"""
logger.info('multi tasks')


def task1():
    logger.info('I am task1--initing hotwords')
    init_hot_search_test()
    """
    定时任务
    """
    logger.info('I am task1--start schedule of initing hotwords--waiting for 1 hour')
    hot_search_schedule()


def task2():
    """
    web服务
    """
    logger.info('I am task2--start web service')
    start()


def task3():
    """
    定时任务
    """
    logger.info('I am task3--start schedule of incremental update search--waiting for 30 min')
    incre_update_schedule()


p1 = multiprocessing.Process(target=task1)  # multiprocessing.Process创建了子进程对象p1
p2 = multiprocessing.Process(target=task2)  # multiprocessing.Process创建了子进程对象p2
p3 = multiprocessing.Process(target=task3)  # multiprocessing.Process创建了子进程对象p3
p1.start()  # 子进程p1启动
p2.start()  # 子进程p2启动
p3.start()  # 子进程p3启动
print("I am main task")  # 这是主进程的任务











