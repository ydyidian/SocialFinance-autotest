# coding=utf-8
"""
日志文件
"""
import logging

from common.file_path import fp  # 导入文件路径


class Logger(object):  # 日志类
    def __init__(self, logger):
        """
        指定保存日志的文件路径，日志级别，以及调用文件
        将日志存入到指定的文件中
        """

        # 创建一个logger
        # self.logger = logging.getLogger(logger)  # 使用这种方式会导致同名logger打印多次的问题
        self.logger = logging.Logger(logger)
        self.logger.setLevel(logging.DEBUG)

        # 创建一个handler，用于写入日志文件
        log_name = fp.log_file_path()  # F:/DCH_AutoTest_Scripts/APIDdemo/logs/201811252121.log
        fh = logging.FileHandler(log_name, encoding="utf-8")
        fh.setLevel(logging.INFO)

        # 再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        # 定义handler的输出格式
        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(threadName)s - %(filename)s[%(lineno)d]: %(message)s"
        )
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # 给logger添加handler
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    def getlog(self):
        return self.logger


# logger = Logger("ddddd").getlog()

if __name__ == '__main__':
    l = Logger("ddddd").getlog()
    l.error("ddddddd")
    l.info("zhe是一个测试类")
