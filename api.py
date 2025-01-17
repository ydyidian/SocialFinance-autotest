# coding=utf8

import json
from enum import Enum
from json import JSONDecodeError
from typing import Dict
from urllib import parse
import urllib3

import requests
from common.config import config
from common.logger import Logger
from common.rw_yaml import YamlData

urllib3.disable_warnings()
logger = Logger(logger="BaseAPI").getlog()


class RequestContentType(Enum):
    # 请求方式目前就是json格式  ｜  form表单
    JSON = "application/json; charset=UTF-8"
    FORM = "application/x-www-form-urlencoded; charset=UTF-8"
    FILE = "multipart/form-data; charset=UTF-8"


class Request(object):
    @staticmethod
    def get_headers(token: str, content_type: str = None):
        """
        获取请求头部信息
        """
        headers = {
            "Accept": "application/json,text/plain, */*",
            "token": token
        }
        content_type_obj = RequestContentType.__members__.get(content_type)
        if content_type_obj:
            headers.update({"Content-Type": content_type_obj.value})
        return headers

    @classmethod
    def request(
            cls,
            method: str,
            url: str,
            *,
            session: requests.Session = None,
            expect_status_code: int = 200,
            expect_errcode: int = 0,
            expect_msg: str = None,
            validate_type: str = "equal",
            **kwargs,
    ):
        """
        获取请求响应
        :param method: 请求方式
        :param url: url
        :param session: session对象
        :param kwargs: 其他入参
        :return: 响应是否为json， 请求响应
        """
        if session and isinstance(session, requests.Session):
            resp = session.request(method, url, **kwargs)
        else:
            resp = requests.request(method, url, **kwargs)
        is_json, ret = cls.validate_response(resp, expect_status_code, expect_errcode, expect_msg, validate_type)
        return is_json, ret

    def validate_response(self, response, expect_status_code, expect_errcode, expect_msg, validate_type):
        """
        校验响应信息
        :param response: 响应对象
        :param expect_status_code: 预期接口返回状态码
        :param expect_errcode: 预期接口返回错误码
        :param expect_msg: 预期错误信息
        :param validate_type: 错误信息校验类型 「equal | contains」
        """
        assert (
                response.status_code == expect_status_code
        ), f"接口响应状态码与预期不符：预期「{expect_status_code}」，实际状态码「{response.status_code}」"
        try:
            resp_data = response.json()
            is_json = True
        except JSONDecodeError:
            resp_data = response.content.decode()
            is_json = False
        if is_json:
            resp_data = response.json()
            if expect_errcode is not None:
                assert (
                        resp_data["errcode"] == expect_errcode
                ), f"接口报文错误码与预期不符：预期「{expect_errcode}」，实际「{resp_data['errcode']}」"
            if expect_msg is not None:
                if validate_type == "contains":
                    assert (
                            expect_msg in resp_data["errmsg"]
                    ), f"接口报文错误信息与预期不符：预期「{expect_msg}」，实际「{resp_data['errmsg']}」"
                elif expect_msg is not None and validate_type == "equal":
                    assert (
                            resp_data["errmsg"] == expect_msg
                    ), f"接口报文错误信息与预期不符：预期「{expect_msg}」，实际「{resp_data['errmsg']}」"
                elif validate_type not in ("equal", "contains"):
                    raise ValueError("请传入正确的错误提示校验类型：equal｜contains")
        return is_json, resp_data

    @staticmethod
    def urlencode(query: Dict, doseq=False, safe="", encoding=None, errors=None, quote_via=parse.quote):
        """
        修改urlencode，以适应True -> true, None -> null
        :param query: query参数，可传入字典或者列表元组类型的数据
        :param doseq:
        :param safe:
        :param encoding: 加密方式，默认None
        :param errors: 错误
        :param quote_via: 转码方式，默认单层quote
        :return: query参数
        """
        if hasattr(query, "items"):
            query = query.items()
        elif len(query) and not isinstance(query[0], tuple):
            raise TypeError("not a valid non-string sequence or mapping object")

        return parse.urlencode(
            [(k, v if isinstance(v, str) else json.dumps(v)) for k, v in query],
            doseq,
            safe,
            encoding,
            errors,
            quote_via,
        )


class BaseAPI(object):
    # 公共缓存变量，用于存放用户登录token信息
    LOGIN_CACHE = {}

    def __init__(
            self,
            username: str = None,
            password: str = None,
            client_type: str = "android",
            domain: str = config.getUrl_BaseInfo("base_url")
    ):
        """
        初始化接口访问基类属性
        :param username: 用户名, 默认值: None
        :param password: 登录密码, 默认值: None
        """
        self.client_type = client_type
        self.domain = domain
        self.album_id, self.token = self.login(username, password)

    def login(self, username: str, password: str, ticket: str = "123456"):
        """
        用户登录
        :param username: 用户名，手机号
        :param password: 登录密码
        :param ticket: 验证码
        :return: 返回token信息
        """
        login_key = f"{username}@{password}"
        if login_key in BaseAPI.LOGIN_CACHE:
            user_dic = BaseAPI.LOGIN_CACHE.get(login_key)
            return user_dic["album_id"], user_dic["token"]
        else:
            url = f"{self.domain}/album/api/v1/user/loginByCellphone"
            data = {"phone_number": username, "password": password, "ticket": ticket}
            params = {"client_type": self.client_type}
            # is_json, resp = Request.request("post", url, json=data, verify=False)
            is_json, resp = Request.request("post", url, params=params, json=data, verify=False)
            if is_json:
                album_id = resp["result"]["albumId"]
                token = resp["result"]["token"]
                BaseAPI.LOGIN_CACHE[login_key] = {"token": token, "album_id": album_id}
                self.token = token
                return album_id, token
            else:
                raise ValueError("Token信息获取失败")

    def get(
            self,
            uri: str = None,
            *,
            params: dict = None,
            data: dict = None,
            file=None,
            json: dict = None,
            content_type: str = None,
            expect_status_code: int = 200,
            expect_errcode: int = 0,
            expect_msg: str = None,
            validate_type: str = "equal",
    ):
        """
        GET请求
        :param uri: uri地址，默认为null（读取url_params）
        :param params: params请求参数, 传入字典类型
        :param data: data请求参数, 传入字典类型
        :param file: 上传文件，默认为None（不上传）
        :param json: json数据「application/json」
        :param content_type: content-type类型名称：JSON | FORM
        :param params: query参数
        :param expect_status_code: 预期接口返回状态码
        :param expect_errcode: 预期接口返回错误码
        :param expect_msg: 预期错误信息
        :param validate_type: 错误信息校验类型 「equal | contains」
        :return: 请求响应对象
        """
        url = f"{self.domain}{uri}"
        headers = Request.get_headers(self.token, self.client_type, content_type)
        logger.info(self._assemble_msg("GET", url, headers, params, data, json), desc="GET接口请求")
        _, response = Request.request(
            "get",
            url,
            params=params,
            data=data,
            json=json,
            headers=headers,
            files=file,
            verify=False,
            timeout=30,
            expect_status_code=expect_status_code,
            expect_errcode=expect_errcode,
            expect_msg=expect_msg,
            validate_type=validate_type,
        )
        logger.info(("接口返回信息：", response))
        return response

    def post(
            self,
            uri: str = None,
            *,
            data: str = None,
            file=None,
            json: dict = None,
            params: dict = None,
            content_type: str = None,
            expect_status_code: int = 200,
            expect_errcode: int = 0,
            expect_msg: str = None,
            validate_type: str = "equal",
    ):
        """
        POST请求
        :param uri: uri地址，默认为null（读取url_params）
        :param data: data请求参数, 传入字符串类型
        :param file: 上传文件，默认为None（不上传）
        :param json: json数据「application/json」
        :param params: query参数
        :param content_type: content-type类型名称：JSON | FORM
        :param expect_status_code: 预期接口返回状态码
        :param expect_errcode: 预期接口返回错误码
        :param expect_msg: 预期错误信息
        :param validate_type: 错误信息校验类型 「equal | contains」
        :return: 请求响应对象
        """
        url = f"{self.domain}{uri}"
        headers = Request.get_headers(self.token, self.client_type, content_type)
        logger.info(self._assemble_msg("POST", url, headers, params, data, json), desc="POST接口请求")
        _, response = Request.request(
            "post",
            url,
            params=params,
            data=data.encode("utf-8") if data is not None else data,
            json=json,
            headers=headers,
            files=file,
            verify=False,
            timeout=30,
            expect_status_code=expect_status_code,
            expect_errcode=expect_errcode,
            expect_msg=expect_msg,
            validate_type=validate_type,
        )
        logger.info(("接口返回信息：", response))
        return response

    def put(
            self,
            uri: str = None,
            *,
            data=None,
            file=None,
            json: dict = None,
            params: dict = None,
            content_type: str = None,
            expect_status_code: int = 200,
            expect_errcode: int = 0,
            expect_msg: str = None,
            validate_type: str = "equal",
    ):
        """
        PUT请求
        :param uri: uri地址，默认为null（读取url_params）
        :param data: data请求参数
        :param file: 上传文件，默认为None（不上传）
        :param json: json数据「application/json」
        :param params: query参数
        :param content_type: content-type类型名称：JSON | FORM
        :param expect_status_code: 预期接口返回状态码
        :param expect_errcode: 预期接口返回错误码
        :param expect_msg: 预期错误信息
        :param validate_type: 错误信息校验类型 「equal | contains」
        :return: 请求响应对象
        """
        url = f"{self.domain}{uri}"
        headers = Request.get_headers(self.token, self.client_type, content_type)
        logger.info(self._assemble_msg("PUT", url, headers, params, data, json), desc="PUT接口请求")
        _, response = Request.request(
            "post",
            url,
            params=params,
            data=data,
            json=json,
            headers=headers,
            files=file,
            verify=False,
            timeout=30,
            expect_status_code=expect_status_code,
            expect_errcode=expect_errcode,
            expect_msg=expect_msg,
            validate_type=validate_type,
        )
        logger.info(("接口返回信息：", response))
        return response

    def delete(
            self,
            uri: str = None,
            *,
            data: str = None,
            file=None,
            json: dict = None,
            params: dict = None,
            content_type: str = None,
            expect_status_code: int = 200,
            expect_errcode: int = 0,
            expect_msg: str = None,
            validate_type: str = "equal",
    ):
        """
        POST请求
        :param uri: uri地址，默认为null（读取url_params）
        :param data: data请求参数, 传入字符串类型
        :param file: 上传文件，默认为None（不上传）
        :param json: json数据「application/json」
        :param params: query参数
        :param content_type: content-type类型名称：JSON | FORM
        :param expect_status_code: 预期接口返回状态码
        :param expect_errcode: 预期接口返回错误码
        :param expect_msg: 预期错误信息
        :param validate_type: 错误信息校验类型 「equal | contains」
        :return: 请求响应对象
        """
        url = f"{self.domain}{uri}"
        headers = Request.get_headers(self.token, self.client_type)
        logger.info(self._assemble_msg("DELETE", url, headers, params, data, json), desc="DELETE接口请求")
        _, response = Request.request(
            "post",
            url,
            params=params,
            data=data,
            json=json,
            headers=headers,
            files=file,
            verify=False,
            timeout=30,
            expect_status_code=expect_status_code,
            expect_errcode=expect_errcode,
            expect_msg=expect_msg,
            validate_type=validate_type,
        )
        logger.info(("接口返回信息：", response))
        return response

    def _assemble_msg(self, method, url, headers, params, data, json):
        """
        组装请求响应日志内容
        :param method: 请求方式
        :param url: 请求地址
        :param headers: 头部信息
        :param params: query参数
        :param data: data参数
        :param json: json参数
        :return: 信息列表
        """
        messages = [f"[{method.upper()}] {url}", "请求头部信息：", f"{headers}", "\n请求报文："]
        if params:
            messages.extend(("\n  param参数：", params, "\n"))
        if data:
            messages.extend(("\n  data参数：", data, "\n"))
        if json:
            messages.extend(("\n  body参数：", json, "\n"))
        return messages


if __name__ == "__main__":
    # c = BaseAPI("13510547953", "19850406", client_type="miniapp")
    # print(c.album_id, c.token)
    r = Request()
    print(r.get_headers("kkdkdk", "1233555"))
