from pymysql import connect
import traceback


class SynchronizeData:

    def __init__(self, hisense_conf_dict, sqyn_sc_dict, logger):
        self._logger = logger
        hisense_conf_dict['port'] = int(hisense_conf_dict['port'])
        sqyn_sc_dict['port'] = int(sqyn_sc_dict['port'])
        if 'url' in hisense_conf_dict:
            del hisense_conf_dict['url']
        if 'url' in sqyn_sc_dict:
            del sqyn_sc_dict['url']
        logger.info(f'hisense配置{hisense_conf_dict}')
        self.hisense_conn = connect(**hisense_conf_dict)
        logger.info('hisense连接成功')
        logger.info(f'sqyn_sc配置{sqyn_sc_dict}')
        self.sqyn_sc_conn = connect(**sqyn_sc_dict)
        logger.info('sqyn_sc连接成功')

    def mysql_operation(self, select_sql, insert_sql, sqyn_sc_table):
        page = 1
        query_rows = 1000
        while True:
            # 查询数据
            start_index = (page - 1) * query_rows
            with self.hisense_conn.cursor() as cur:
                count = cur.execute(select_sql, [start_index, query_rows])
                if not count:
                    self._logger.info('没有查询到数据')
                    return
                self._logger.info('查询到{}条数据'.format(count))
                rows = cur.fetchall()
            # 写入数据
            self._logger.info('{}开始写入数据'.format(sqyn_sc_table))
            with self.sqyn_sc_conn.cursor() as cur:
                try:
                    cur.executemany(insert_sql, rows)
                    self.sqyn_sc_conn.commit()
                except:
                    self._logger.error('{}写入数据异常{}'.format(sqyn_sc_table, traceback.format_exc()))
                    self.sqyn_sc_conn.rollback()
                    return
                else:
                    self._logger.info('{}写入数据成功'.format(sqyn_sc_table))
                    # 小于1000终止循环
                    if count < query_rows:
                        return
                    page += 1
