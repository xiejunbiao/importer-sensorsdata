import sys
import os
import getopt
import configparser
import copy
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(os.path.split(rootPath)[0])
sys.path.append(rootPath)


def para_set(argv):
    ip = ''
    port = ''
    conf = ''
    try:
        opts, args = getopt.getopt(argv, "hc:l:d", ["conf=", "log=", "db="])
    except getopt.GetoptError:
        print('test.py -i <inputfile> -p <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        print(opt, arg)
        if opt == '-h':
            print('test.py -i <inputfile> -p <outputfile>')
            sys.exit()
        elif opt in ("-c", "--conf"):
            conf = arg
        elif opt in ("-l", "--log"):
            log = arg
        elif opt in ("-d", "--db"):
            db = arg

    #   self.__logger.info('输入的文件为：', ip)
    #   self.__logger.info('输出的文件为：', port)
    #   self.__logger.info('db:',db)
    # return (conf,log)
    return conf


class ConfigValue:
    """
    配置文件类
    """
    # 项目路径
    # rootDir = os.path.split(os.path.realpath(__file__))[0]
    # config.ini文件路径
    # configFilePath = os.path.join(rootDir, 'config.ini')
    def __init__(self, rootdir):
        configfilepath = os.path.join(rootdir, 'config.ini')
        self.config = configparser.ConfigParser()
        self.config.read(configfilepath)

    def get_config_values(self, section_argv, arglist=None):
        """
        根据传入的section获取对应的value
        :param section_argv: ini配置文件中用[]标识的内容
        :return:
        """
        # return config.items(section=section)
        if arglist is None:
            arglist = ['host', 'user', 'password', 'db', 'port', 'url']

        # if section_argv == 'dbtable':
        #     arglist = ['order_table', 'rec_table', 'filter_table']
        config_result = {}
        for option in arglist:
            if option == 'envIp':
                section = 'storeinterface'
            else:
                section = '%s' % section_argv
            config_result[option] = self.config.get(section=section, option=option)
        return config_result

    def get_config_values_list(self, section_argv, arglist) -> list:
        """
        获得某个配置文件中指定section(section_argv),和指定option列表(arglist)对应的值
        """
        config_result = []
        for option in arglist:
            if option == 'envIp':
                section = 'storeinterface'
            else:
                section = '%s' % section_argv
            config_result = config_result + str(self.config.get(section=section, option=option)).split(',')

        return config_result

    def get_sections_all(self) -> list:
        """
        获得某个配置文件的所有section
        """
        return self.config.sections()

    def get_option(self, section):
        """
        获得某个section的所有option
        """
        return self.config.options(section)

    def get_key_values(self, section):
        return self.config.items(section)


cmd_argv = sys.argv[1:]


class ModifyConfFile(object):
    def __init__(self, logger):
        self.logger = logger
        try:
            self._file_path_argv = para_set(cmd_argv)
            # print(self._file_path_argv)
            self._config_Value = ConfigValue(self._file_path_argv)
            self._sqyn_mysql = self._config_Value.get_config_values('sqyn_mysql')
            self._hisense_mysql = self._config_Value.get_config_values('hisense_mysql')
            # self.logger.info(str(self._sqyn_mysql) + '\n' + str(self._hisense_mysql))
        except Exception as e:
            self.logger.debug(e)
        self._modify_conf()
        # self._modify_list = ['host', 'user', 'password', 'port', 'db', 'url']

    def _modify_conf(self):

        path = os.path.abspath(os.path.dirname(__file__))
        try:
            init_return_sku1 = os.path.join(path, 'conf/mysql_event_init_return_sku.conf')
            self.logger.info('配置文件路径为%s' % init_return_sku1)
            self._modify_file(init_return_sku1)

            init_return_sku2 = os.path.join(path, 'conf/mysql_event_init_sale_order.conf')
            self.logger.info('配置文件路径为%s' % init_return_sku2)
            self._modify_file(init_return_sku2)

            init_return_sku3 = os.path.join(path, 'conf/mysql_event_update_area_data_set.conf')
            self.logger.info('配置文件路径为%s' % init_return_sku3)
            self._modify_file(init_return_sku3)

            init_return_sku4 = os.path.join(path, 'conf/mysql_event_update_goods_area_count.conf')
            self.logger.info('配置文件路径为%s' % init_return_sku4)
            self._modify_file(init_return_sku4)

            init_return_sku5 = os.path.join(path, 'conf/mysql_event_update_owner_binding_area_count.conf')
            self.logger.info('配置文件路径为%s' % init_return_sku5)
            self._modify_file(init_return_sku5)

            init_return_sku6 = os.path.join(path, 'conf/mysql_event_update_sale_order.conf')
            self.logger.info('配置文件路径为%s' % init_return_sku6)
            self._modify_file(init_return_sku6)

            init_return_sku7 = os.path.join(path, 'conf/mysql_event_update_sale_return_sku.conf')
            self.logger.info('配置文件路径为%s' % init_return_sku7)
            self._modify_file(init_return_sku7)

        except Exception as e:
            self.logger.debug('配置文件修改异常')
        else:
            self.logger.info('修改配置文件成功')

    def _modify_file(self, path):
        file_data = ""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and line[0] == '#':
                        continue
                    old_line = copy.deepcopy(line)
                    key = line.split(':')[0]
                    if key in self._sqyn_mysql.keys():
                        file_data = file_data + '%s:%s' % (key, self._sqyn_mysql[key]) + '\n'
                    else:
                        file_data = file_data + old_line + '\n'
            with open(path, "w", encoding="utf-8") as f:
                f.write(file_data)
        except Exception as e:
            self.logger.debug(e)

    def return_argv(self):
        return {'hisense_mysql': self._hisense_mysql, 'sqyn_mysql': self._sqyn_mysql}


# E:\Document\project\cloudbrain-importer-sensorsdata\importer-sensorsdata\format_importer_1_13_2\conf
if __name__ == '__main__':
    pass
    # mcf = ModifyConfFile()
    # dict = mcf.return_argv()
    # for key in dict.keys():
    #     print(dict[key])
