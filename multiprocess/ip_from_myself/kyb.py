# -*- coding: utf-8 -*-
# @AuThor  : frank_lee
# 使用自己ip池，并实现多线程爬虫
import requests
import json
import pymongo
from ip_from_myself.ip_judge import Get_Ip
from multiprocessing import Pool
import time

conn = pymongo.MongoClient(host="localhost", port=27017)
db = conn['kaoyanbang']


def handle_requests(url):
    headers = {
        "Host": "mapi.kyboye.com",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "KY-APPVER": "3.2.9",
        "KY-APPCHG": "ky_kaoyan",
        "KY-SPEID": "10081255",
        "KY-APPTYPE": "2",
        "KY-SCHID": "1000",
        "KY-APPVERS": "86",
        "KY-SYSVER": "5.1.1",
        "KY-YEAR": "2020",
        "KY-SYSDEV": "OPPO++OPPO+R11",
        "KY-TOKEN": "316061c6cdcff2c9e411b96791a86042",
        "KY-UUID": "f341f084e029c53543d3714555b2658c",
        "User-Agent": "KaoYanBang AipBot/1.0 (KaoYanClub-Android/3.2.9; android/5.1.1; OPPO++OPPO+R11)",

    }
    # 使用ip代理，以防访问过多而封号
    get_ip = Get_Ip()
    proxy = get_ip.get_random_ip()
    # 判断一下，自建ip代理池成功率70%，如果失败，使用自己本机的ip
    if isinstance(proxy, dict):
        response = requests.get(url, headers=headers, proxies=proxy)
    else:
        print("代理根本不能用，大傻子！")
        response = requests.get(url, headers=headers)
    return response


def handle_index(url):
    response = handle_requests(url)
    response_dict = json.loads(response.text)
    for dataline in response_dict['res']['list']:
        friends_info = {}
        friends_info['uid'] = dataline['uid']
        friends_info['uname'] = dataline['uname']
        friends_info['title'] = dataline['title']
        friends_info['icon'] = dataline['icon']
        friends_info['content'] = dataline['content']
        friends_info['pics'] = dataline['pics']
        save_to_mongo(friends_info)
        print(friends_info)


def save_to_mongo(result):
    if db['friends'].insert(result):
        print("保存成功")


if __name__ == '__main__':
    start = time.time()
    url = "https://mapi.kyboye.com/club/thread/list?fid=136&type=1&typeid=0&skip="
    pg_url = [url + '{}&psize=20'.format(str(26 + i * 20)) for i in range(6)]
    p = Pool()
    p.map(handle_index, pg_url)
    p.close()
    p.join()
    end = time.time()
    print("共计用时%.4f秒" % (end - start))
