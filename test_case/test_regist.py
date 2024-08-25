# from api.api_core import *
import json
import os

import allure
import pytest
import requests
from common.config import config
from common.api_core import ReqDataSend
from common.rw_yaml import YamlData
from common.logger import Logger
from common.aitd_login import Request
from env.config_data import *
from common.aitd_login import *

# yaml_data = YamlData("user_name.yaml")
yaml_data = YamlData("tc.yaml")
getDiscoveryArticle = YamlData("getDiscoveryArticle.yaml")


@pytest.fixture(scope="session", autouse=True)
def my_fixture():
    login()


@allure.epic("社交金融")
@allure.feature("登录模块01")
class TestRegister(object):

    @classmethod
    def setup_class(cls):
        cls.longin = ReqDataSend('register.yaml')
        # self.longin = ReqDataSend('login.yaml')
        cls.url = config.getUrl_BaseInfo("base_url")
        cls.read_yaml = YamlData
        cls.logger = Logger("测试").getlog()
        cls.request = Request()

    def teardown_class(self):
        pass

    @pytest.mark.skip
    @pytest.mark.parametrize("api_name", ("register",))
    def test_register_001(self, api_name):
        api_data = self.longin.get_conf_yaml(api_name)
        self.logger.info(f"url地址为：{self.url}")
        self.logger.info(f"请求参数为：{api_data}")

        # api_conf, resp = self.longin.update_conf_resend_msg(self.url, api_name, None, headers=self.header)

    # @pytest.mark.skip
    @pytest.mark.parametrize("data", yaml_data.read_yaml())
    def test_user_name_001(self, data):
        allure.dynamic.title(data["desc"])

        self.logger.info(f"请求参数为：{data}")
        allure.step(f"请求参数：{data}")
        assert 4 == 4

    @pytest.mark.parametrize("data", getDiscoveryArticle.read_yaml())
    def test_page(self, data):
        allure.dynamic.title(data["desc"])
        res = self.request.send_request(**data)
        print(res)
        print(HEADERS["token"])

    # @pytest.mark.skip
    def test_page01(self):
        data = {"pageAble": "1", "userId": "fe9cba1cec6144acbb4c7ef9c4a3e693"}
        res = requests.request("POST", url=URL["test_url"] + "/SocialFinance/sys/msg/page", headers=HEADERS, json=data)
        print(res.text)
        print(HEADERS)
        self.logger.info(f"page接口响应参数为：{res.text}")


if __name__ == '__main__':
    pytest.main()
    # os.system("allure generate -c ../temps -o ../report")
