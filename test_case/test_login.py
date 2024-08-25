import allure
import pytest
from common.config import config
from common.api_core import ReqDataSend
from common.rw_yaml import YamlData
from common.logger import Logger
from common.aitd_login import Request

yaml_data = YamlData("user_name.yaml")


@allure.epic("社交金融")
@allure.feature("登录模块03")
class TestRegister(object):

    @classmethod
    def setup_class(self):
        self.longin = ReqDataSend('register.yaml')
        # self.longin = ReqDataSend('login.yaml')
        self.url = config.getUrl_BaseInfo("base_url")
        self.read_yaml = YamlData
        self.logger = Logger("测试").getlog()
        self.request = Request()

    def teardown_class(self):
        pass

    @allure.title("第一个测试用例")
    @pytest.mark.parametrize("api_name", ("register",))
    def test_regist_001(self, api_name):
        api_data = self.longin.get_conf_yaml(api_name)
        # print(api_name)
        # print(api_data)
        # print(self.url)
        self.logger.info(f"url地址为：{self.url}")
        self.logger.info(f"请求参数为：{api_data}")

        # api_conf, resp = self.longin.update_conf_resend_msg(self.url, api_name, None, headers=self.header)

    @allure.title("第3个测试用例")
    @pytest.mark.parametrize("data", yaml_data.read_yaml())
    def test_uaer_name_001(self, data):
        # print(data)
        allure.dynamic.title(data["desc"])

        self.logger.info(f"请求参数为：{data}")
        allure.step(f"请求参数：{data}")
        assert 4 == 3


if __name__ == '__main__':
    pytest.main()
