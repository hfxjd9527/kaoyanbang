# -*- coding: utf-8 -*-
# @AuThor  : frank_lee
import requests

PROXY_POOL_URL = 'http://localhost:5555/random'


def get_proxy():
    try:
        response = requests.get(PROXY_POOL_URL)
        if response.status_code == 200:
            return response.text
    except ConnectionError:
        return None


def judge_ip():
    # 判断ip是否可用
    ip = get_proxy()
    print(ip)
    http_url = "http://www.baidu.com"
    proxy_url = "http://{0}".format(ip)
    try:
        proxy_dict = {
            "http": proxy_url,
        }
        response = requests.get(http_url, proxies=proxy_dict)
    except Exception as e:
        print("invalid ip and port")
        return False
    else:
        code = response.status_code
        if code >= 200 and code < 300:
            print("effective ip")
            return proxy_dict
        else:
            print("invalid ip and port")
            return False
