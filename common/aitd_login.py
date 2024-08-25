import json

import requests
from env.config_data import *


class Request:
    def __init__(self):
        self.header = HEADERS
        self.url = URL["test_url"]

    def send_request(self, **kwargs):
        if kwargs["method"] == "GET":
            res = requests.request(kwargs["method"], self.url + kwargs["uri"], params=kwargs["req_body"],
                                   headers=self.header)
            return res.json()
        else:
            res = requests.request(kwargs["method"], self.url + kwargs["uri"], json=kwargs["req_body"],
                                   headers=self.header)
            return res.json()



def login():
    header = {
        "Content-Type": "application/json; charset=UTF-8",
        "encry": "ro0gJwGZX/HWAWpqZuSz5jPj4mPMoj8XmauuC+ySaFmioY3kXqpyNK7Bv1BNH6AR7Hkua5zWFwXZp1h42SctJYezYUKfZxPACMEZH23f6BlOq3RWvQ9DvAAiSRi+CUim9UkWUYbHaDP4WVqSRFrSLmAEfR70fIjQTp5dpEdDspM="
    }
    uri = "/SocialFinance/user/v2/login"
    data = {
        "data": "5SbjEzxTr/CNacs4YsvrKx1DxFsDTeMxJsQMIy7I8PtvX1Zp6sjye/P+f2SSwyWCm56i+kzDpg3EKWzPY8s0HztyNhmQZ3U0MG+lTzIrg/bNP2rwZ4PiQrDfAEfW/eshMA/l3qR3mODDxUfDq8ELuEgUZbhzwSXQ90g5dxKjbpveSjevq5J96l3VuQ/u2ER3j214DSuyc/F+JQzsppFHMvoKu1qZ6s+uEfbhTSUGt/w="
    }
    res = requests.request("POST", url=URL["test_url"] + uri, headers=header, json=data)
    HEADERS["token"] = res.json()["data"]["token"]

    return HEADERS


if __name__ == '__main__':
    print(login())
