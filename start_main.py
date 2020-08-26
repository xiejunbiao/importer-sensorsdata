import multiprocessing
from importerdata_mian import InitAndUpdate
from log_w import log_logger

# logger = logging.getLogger()    # initialize logging class
# logger.setLevel(logging.INFO)

# argv=sys.argv[1:]
# confPath=para_set(argv)

logger = log_logger()
# print('init pickle')

logger.info('multi tasks')

iasu = InitAndUpdate(logger)

"""
多进程
"""
#
# def task1():
#     logger.info('I am task1--initing')
#     """
#     定时任务
#     """
#     logger.info('I am task1--start initing import data')
#     iasu.init_data()


def task2():
    logger.info('I am task1--initing')
    iasu.init_data()

    logger.info('I am task2--start scheduler update data')
    iasu.scheduler_update()


# p1 = multiprocessing.Process(target=task1)  # multiprocessing.Process创建了子进程对象p1
p2 = multiprocessing.Process(target=task2)  # multiprocessing.Process创建了子进程对象p2
# p1.start()  # 子进程p1启动
p2.start()  # 子进程p2启动
print("I am main task")  # 这是主进程的任务
