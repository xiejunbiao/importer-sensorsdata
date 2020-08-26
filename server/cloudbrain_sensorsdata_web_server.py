# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 15:01:02 2019

@author: lijiangman
"""
import json

"""
多线程
增加  @run_on_executor
"""

import traceback
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.httpclient
import tornado.web
import tornado.gen
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor
# from analyse.analyzer import chat_with_you
# from format_importer_1_13_2.update_main import data_update_start
# from format_importer_1_13_2.init_main import data_init_start
from importerdata_mian import InitAndUpdate

import logging
logging.basicConfig()


def getLogger():
    logger = logging.getLogger("SENSORSDATA_IMPORTER")
    logger.propagate = False

    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger


logger = getLogger()
iasu = InitAndUpdate(logger)


class SynMysqlDataInitHandler(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(20)

    def initialize(self, logger):
        self.__logger = logger

    @tornado.gen.coroutine
    def get(self):

        """get请求"""
        # query = self.get_argument('inputTxt', default='')
        # areaCode = self.get_argument('areaCode', default='')
        # ownerCode = self.get_argument('ownerCode', default='')
        page_dict = yield self.get_query_answer()
        page_json = json.dumps(page_dict, ensure_ascii=False)
        self.write(page_json)

    @run_on_executor
    def get_query_answer(self):

        """把异常写进日志"""
        code = 200
        message = '初始化调用成功'
        try:
            # self.__logger.info("query-" + query)  # #用query-作为分隔符
            # intention_json = iasu.update_data()
            iasu.init_data()
            self.__logger.info('初始化成功')

        except Exception as e:
            code = 500
            message = '初始化调用失败'
            self.__logger.info("error:")
            self.__logger.info(e)
            self.__logger.info("traceback My:")
            self.__logger.info(traceback.format_exc())  # #返回异常信息的字符串，可以用来把信息记录到log里
        result_json = {
            'resultCode': code,
            'msg': message,
            'data': []
        }
        return result_json


class SynMysqlDataUpdateHandler(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(2)

    def initialize(self, logger):
        self.__logger = logger

    @tornado.gen.coroutine
    def get(self):

        """get请求"""
        # query = self.get_argument('inputTxt')
        result_dict = yield self.get_query_answer()
        page_json = json.dumps(result_dict, ensure_ascii=False)
        self.write(page_json)

    @run_on_executor
    def get_query_answer(self):

        """把异常写进日志"""
        code = 200
        message = '更新调用成功'
        try:
            # self.__logger.info("query-" + query)  # #用query-作为分隔符
            # intention_json = iasu.update_data()
            iasu.update_data()
            self.__logger.info('更新成功')

        except Exception as e:
            code = 500
            message = '更新调用失败'
            self.__logger.info("error:")
            self.__logger.info(e)
            self.__logger.info("traceback My:")
            self.__logger.info(traceback.format_exc())  # #返回异常信息的字符串，可以用来把信息记录到log里
        result_json = {
            'resultCode': code,
            'msg': message,
            'data': []
        }
        return result_json


def start():

    port = 6607
    app = tornado.web.Application(handlers=[
        (r"/cloudbrain-sensors/sensorsdata-import/init", SynMysqlDataInitHandler,  dict(logger=logger)),
        (r"/cloudbrain-sensors/sensorsdata-import/update", SynMysqlDataUpdateHandler,  dict(logger=logger))
    ])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.bind(port)
    http_server.start(2)
    tornado.ioloop.IOLoop.instance().start()

    """
        (r"/cloudbrain/sqyn_to_sc/init_data", SynMysqlDataInitHandler,  dict(logger=logger)),
        (r"/cloudbrain/sqyn_to_sc/update_data", SynMysqlDataUpdateHandler,  dict(logger=logger))
    """
  
    """
    请求url:
    http://10.18.222.105:6603/cloudbrain-assistant/assistant/intentionparse?inputTxt=我要报修&ownerCode=a
    http://10.18.222.105:6603/cloudbrain-assistant/assistant/intentionparse?inputTxt=报修
    http://10.18.222.105:6603/bigdata-assistant/assistant/answerOfquery_test1?query=报修
    /bigdata-assistant/assistant/intentionparse
    http://10.18.226.58:6603/cloudbrain-assistant/assistant/intentionparse?inputTxt=我要报修&ownerCode=a
    """
    """
    http://10.18.222.105:6607/cloudbrain-sensors/sensorsdata-import/init
    http://10.18.222.105:6607/cloudbrain-sensors/sensorsdata-import/update
    /cloudbrain/sqyn_to_sc/update_data
    """


if __name__ == "__main__":
    print('the main is not this path')
