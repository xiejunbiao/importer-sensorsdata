from apscheduler.schedulers.blocking import BlockingScheduler
from format_importer_1_13_2.init_main import data_init_start
from format_importer_1_13_2.update_main import data_update_start
from format_importer_1_13_2.modify_conf import ModifyConfFile
import datetime
from sc_data_sync.update_data_handler import UpdateDataHandler
from sc_data_sync.initialize_data_handler import InitDataHandler
import traceback


class InitAndUpdate(object):
    def __init__(self, logger):
        # 根据环境修改配置文件,并实例化该类
        self.logger = logger
        mcf = ModifyConfFile(logger)
        two_mysql = mcf.return_argv()
        self.hisense_mysql = two_mysql['hisense_mysql']
        self.sqyn_mysql = two_mysql['sqyn_mysql']

    def init_data(self):
        # '--------------------------'
        self.logger.info('开始初始化 hisense_to_sqyn')
        try:
            InitDataHandler(self.hisense_mysql, self.sqyn_mysql, self.logger).init_start()
        except Exception as e:
            self.logger.error('初始化 hisense_to_sqyn 异常:', traceback.print_exc())
        else:
            self.logger.info('初始化 hisense_to_sqyn 成功')

        self.logger.info('开始初始化 sqyn_to_sc')
        try:
            data_init_start()
        except Exception as e:
            self.logger.error('初始化 sqyn_to_sc 异常:', traceback.print_exc())
        else:
            self.logger.info('初始化 sqyn_to_sc 成功')

    def update_data(self):
        # '--------------------------'
        self.logger.info('开始更新 hisense_to_sqyn')
        try:
            UpdateDataHandler(self.hisense_mysql, self.sqyn_mysql, self.logger).update_start()
        except Exception as e:
            self.logger.error('更新 hisense_to_sqyn 异常', traceback.print_exc())
        else:
            self.logger.info('更新 hisense_to_sqyn_sc 成功')

        self.logger.info('开始更新 sqyn_to_sc')
        try:
            data_update_start()
        except Exception as e:
            self.logger.error('更新 sqyn_to_sc 异常', traceback.print_exc())
        else:
            self.logger.info('更新 sqyn_to_sc 成功')

    def scheduler_update(self):
        scheduler = BlockingScheduler()
        # 采用阻塞的方式
        print("start incre_update-at %s------------------------") % datetime.time()
        # 采用固定时间（cron）的方式，每天在固定时间执行
        scheduler.add_job(self.update_data(), trigger='cron', hour=5, minute=30)

        scheduler.start()


if __name__ == '__main__':
    pass
