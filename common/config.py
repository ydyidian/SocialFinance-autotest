# sys.path.append(os.path.split(os.path.dirname(os.path.abspath(__file__)))[0])
import configparser
import os

from common.file_path import fp


class ReadConfig(object):
    def __init__(self, path=fp.config_file_path()):
        self.path = path
        self.config = configparser.ConfigParser()
        res = self.config.read(self.path)  # 读取配置文件
        if not res:
            raise FileNotFoundError("文件路径填写错误或文件不存在！请检查路径是否正确！")

    # 读取配置文件
    def get_option_value(self, section, option):
        return self.config.get(section, option)

    # 修改配置文件
    def add_option_value(self, section, option, data):
        self.config.set(section, option, data)
        self.config.write(open(self.path, "w"))

    def get_MysqlDB(self, name):
        return self.get_option_value("DBINFO", name)

    def get_MongoDB(self, name):
        return self.get_option_value("MONGODBINFO", name)

    def get_RedisDB(self, name):
        return self.get_option_value("REDISINFO", name)

    def getUrl_BaseInfo(self, name):
        return self.get_option_value("TQXD", name)

    def getEmail(self, name):
        return self.get_option_value("Email", name)

    def get_AuthInfo(self, name):
        return self.get_option_value("Auth", name)

    def get_TokenInfo(self, name):
        return self.get_option_value("Token", name)

    def get_AlbumId(self, name):
        return self.get_option_value("AlbumId", name)

    def get_UserId(self, name):
        return self.get_option_value("UserId", name)

    def get_GoodsId(self, name):
        return self.get_option_value("GoodsId", name)


config = ReadConfig()

if __name__ == '__main__':
    # print(config.get_UserId('selfUserId'))
    # print(config.getUrl_BaseInfo("base_url"))
    # config.add_option_value("Token", "selfToken", "99999")
    print(config.getUrl_BaseInfo("base_url"))
