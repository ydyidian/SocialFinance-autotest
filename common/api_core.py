#!/usr/bin/env python
# encoding: utf-8

import json

import allure
import requests
from requests import adapters, exceptions

# from api import data
from common import common_base
import yaml_data

data = yaml_data.__path__[0]


class API(object):
    """接口对象：读取Yaml文件接口数据"""

    def __init__(self, api_file, path=data):
        # self.login = LoginProduct.login_way('mock')
        self.api_file = api_file  # 接口yaml文件名称, xx.yaml
        self.api_info = {}
        self.headers = None
        self.session = requests.Session()
        self.path = path
        print(self.path, self.api_file)

    def get_conf_yaml(self, api_name):
        """
        读取配置文件
        :param api_name: 接口名
        :return: yaml文件配置的接口信息
        """
        res = common_base.load_yaml_data(self.path, self.api_file).get(api_name)
        self.api_info = res
        return res

    def get_api_uri(self, api_name):
        """
        获取接口uri
        :param api_name：接口名称
        :return:
        """
        r = common_base.load_yaml_data(self.path, self.api_file)
        res = r.get(api_name)["uri"]
        return res

    def get_api_url(self, environment, api_name):
        """
        获取接口url
        :param environment:
        :param api_name:  接口名称
        :return: 完整Url
        """
        base_url = environment.get('base_url')
        uri = self.get_api_uri(api_name)
        api_url = base_url + uri
        return api_url

    @staticmethod
    def special_req_url(url, body):
        """
        特殊的请求url， 需要跟请求参数拼接
        :param url: 请求url
        :param body: 参数字典
        :return: 拼接后的url
        """
        param = "?"
        for k, v in body.items():
            p = str(k) + "=" + str(v) + " &"
            param += p
        url = url + param
        return url[:-1]

    def send_http_request(self, method, url,
                          params=None, data=None, headers=None, cookies=None, files=None,
                          auth=None, timeout=None, allow_redirects=True, proxies=None,
                          hooks=None, stream=None, verify=None, cert=None, json=None):
        """
        构造一个:class: ' Request <Request> '，准备并发送它。
        :param method: 请求方法 POST/GET
        :param url:  请求URL
        :param params: (可选)在查询中发送的字典或字节
        :param data: (可选)字典、元组、字节或类似文件的列表
        :param headers:  (可选)要发送的HTTP标头的字典
        :param cookies:  (可选)Dict或CookieJar对象一起发送
        :param files:  (可选)“文件名”字典: 用于多部分编码上传。
        :param auth: (可选)Auth元组或可调用以启用
        :param timeout: (可选)等待服务器发送多长时间  float or tuple
        :param allow_redirects:  (可选)默认设置为True。  bool
        :param proxies:  (可选)字典映射协议或协议和 主机名到代理的URL。
        :param hooks:
        :param stream: (可选)是否立即下载响应 内容。默认为“假”。
        :param verify:  是否验证 服务器的TLS证书
        :param cert: (可选)如果字符串，路径到ssl客户端证书文件(.pem)。
        :param json: (可选)json来发送 类:“请求”
        :return: 返回:class: ' Response <Response> '对象。
        """
        try:
            resp = self.session.request(method=method.upper(),
                                        url=url,
                                        headers=headers,
                                        files=files,
                                        data=data or {},
                                        json=json,
                                        params=params or {},
                                        auth=auth,
                                        cookies=cookies,
                                        hooks=hooks,
                                        timeout=timeout,
                                        allow_redirects=allow_redirects,
                                        proxies=proxies,
                                        stream=stream,
                                        verify=verify,
                                        cert=cert,
                                        )
        except exceptions.ConnectionError as e:
            raise e
        return resp


class ReqDataSend(API):
    """组装请求参数，发送数据"""

    def __init__(self, fn, path=data):
        API.__init__(self, fn, path=path)
        self.time = None  # 创建或更新数据库时间

    def update_api_request_body(self, api_name: str, conf: dict, body: str) -> dict:
        """
        更新请求参数 conf
        :param api_name:  # 自定义接口名
        :param conf: 配置参数 传入待更新的参数
        :param body: 'req_body'   # 待读取参数的请求字段，example (req, req_body, req_body_1 ……)
        :return: api_info
        """
        # 根据api_name 读取yaml文件接口配置信息
        api_info = self.get_conf_yaml(api_name)
        if conf:
            if isinstance(conf, dict):
                api_info.update({'phone': conf['phone']}) if 'phone' in conf else api_info  # 替换登录手机号
                common_base.replace_dict_data(conf, api_info[body])  # 替换
            elif isinstance(conf, list):
                if common_base.is_dict_list(conf):
                    for i in conf:
                        api_info[body][0].update(i)
                elif common_base.is_pure_list(conf):
                    api_info[body] = conf
            else:
                raise TypeError("传入待替换参数类型不支持")
        return api_info

    # 打印客户端接口请求参数
    def _print_client_req_params(self, api_name: str, api_info: dict, body: str):
        allure.attach(api_name, name="api_name: {}".format(api_name))
        allure.attach(json.dumps(api_info[body]), "请求参数", attachment_type=allure.attachment_type.TSV)
        if 'desc' in self.api_info:
            allure.attach(self.api_info.get('desc'), name="接口描述: {}".format(self.api_info['desc']))
        if 'version' in self.api_info:
            allure.attach(self.api_info.get('version'), name="版本新增: {}".format(self.api_info['version']))

    def update_conf_resend_msg(self, environment, api_name, cnf, headers, body='req_body', method='POST', args=None):
        """
        更新请求参数，发送下一个请求，该方法适用于多接口调用，通过session对象保持
        :type environment:
        :param args: get 方法拼接参数
        :param api_name: 接口名
        :param cnf:   要替换的参数字典
        :param headers:  请求头部
        :param method:  请求方法
        :param body:    真实请求参数
        :return:
        """
        # 更新请求参数体
        self.api_info = self.update_api_request_body(api_name, cnf, body)
        url = self.get_api_url(environment, api_name)
        self._print_client_req_params(api_name, self.api_info, body)  # 打印请求参数

        if 'method' in self.api_info:
            method = self.api_info['method']
            allure.attach(self.api_info['method'], name=self.api_info['method'])

        adapters.DEFAULT_RETRIES = 5  # 连接次数
        self.session.keep_alive = False

        try:
            if method == 'POST':
                resp = self.session.request(method, url=url, data=json.dumps(self.api_info[body]), headers=headers)
            elif method == 'GET':
                if args is not None:
                    url = url + str(args)
                if type(self.api_info[body]) is list:
                    resp = self.session.request(method, url=url, json=self.api_info[body], headers=headers)
                else:
                    resp = self.session.request(method, url=url, params=self.api_info[body], headers=headers)
            else:
                return

        except requests.exceptions.ConnectionError as e:
            raise e
        self.time = resp.headers['Date']
        allure.attach(str(url), "请求url", attachment_type=allure.attachment_type.URI_LIST)
        allure.attach(resp.text, "请求响应", attachment_type=allure.attachment_type.JSON)
        return self.api_info, resp


if __name__ == '__main__':
    api = API('register.yaml')
    print(api.api_file)

    print(api.__str__())
    # res = api.get_conf_yaml("register")
    url = "https://appc.baidu.com/appsrv?action=appdistributionlog&native_api=1"
    data = {"host": 6, "scene": 6001, "category": 6001001, "pkgname": "", "appname": "<em>YY</em>语音", "event": 100,
            "ext": {}}
    res = api.send_http_request("POST", url=url, params=data)
    print(res.status_code)
    print(res.text)
