import os
import time


class FilePath(object):  # 文件路径类FilePath

    sep = os.path.altsep if os.name == "nt" else os.path.sep

    def __init__(self):  # 初始化方法
        """fileName为所在文件夹名+文件名"""
        self.basePath = os.path.dirname(os.path.dirname(__file__))
        # self.basePath = os.path.dirname(lib.__path__[0])
        self.logPath = f"{self.basePath}{self.sep}logs"
        self.dataFileName = "/yaml_data/"  # 测试数据

        # self.bpmdataFileName = "/data/bpmdata.xls"                           # 测试数据

        self.configFileName = "/env/config.ini"  # 配置文件路径
        self.configYamlFileName = "/env/configYaml.yaml"
        self.date = time.strftime("%Y-%m-%d", time.gmtime())  # 日期格式化
        self.now = time.strftime("%Y-%m-%d %H_%M_%S", time.localtime(time.time()))  # 日期、时间格式化
        # self.reportFileName='/report/{}_report.html'.format(self.now)                 # 测试报告路径
        self.reportpath = "/report/"
        self.rq = time.strftime("%Y%m%d%H%M", time.localtime(time.time()))  # 时间格式化
        self.logFileName = "/logs/{}.log".format(self.rq)  # 测试日志路径
        self.casePath = "/testcase/"  # 测试用例路径，包含case及case以下所有子目录
        self.excelImportPath = "/data/import/"

    def data_file_path(self):  # 测试数据文件路径方法
        filepath = self.basePath + self.dataFileName
        return filepath

    def data_file_path_yaml(self):
        return self.configYamlFileName

    # def bpmdata_file_path(self):                                  # 测试数据文件路径方法
    #     filepath = self.basePath + self.bpmdataFileName
    #     filepath = filepath.replace('\\', '/')
    #     return filepath

    def config_file_path(self):  # 配置文件config路径方法
        filepath = self.basePath + self.configFileName  # 项目路径 + 配置文件config路径及名称
        return filepath

    # def report_file_path(self):                                     # 测试报告路径方法
    #     filepath=self.basePath+self.reportFileName
    #     filepath=filepath.replace('\\','/')
    #     return filepath

    def report_path(self):
        reportpath = self.basePath + self.reportpath
        return reportpath

    def log_file_path(self):  # 测试日志路径方法
        filepath = self.basePath + self.logFileName
        return filepath

    def case_file_path(self):  # 测试用例路径1，总测试用例路径
        filepath = self.basePath + self.casePath
        return filepath

    def import_file_path(self, file_name):  # 导入文件方法
        filepath = self.basePath + self.excelImportPath + file_name
        return filepath

    def get_abspath_by_relation(self, abspath, relative_path):
        """
        根据参考文件的绝对路径 + 相对路径获取指定文件的绝对路径
            ➤ 主要解决yaml文件写入相对路径导致查询不到文件的问题「abspath传入__file__即可」
        :param abspath: 参考文件的绝对路径
        :param relative_path: 相对路径
        :return: 指定文件的绝对路径
        """
        return os.path.abspath(os.path.join(os.path.dirname(abspath), relative_path))


fp = FilePath()

if __name__ == "__main__":
    path = FilePath()  # 创建一个类的对象path
    print("项目路径:", path.basePath)  # 调用对象的方法，获取各个文件路径
    print("日志路径:", path.logPath)
    print("配置路径:", path.config_file_path())
    print("用例路径:", path.case_file_path())
    print("数据路径:", path.data_file_path())
    print("详细日志", path.log_file_path())
