# -*- coding: utf-8 -*-
# @AuThor  : frank_lee
import requests
import json
import pymongo


class Kaoyanbang():
    def __init__(self):
        self.conn = pymongo.MongoClient(host="localhost", port=27017)
        self.db = self.conn['kaoyanbang']

    def handle_requests(self, url):
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
        response = requests.get(url, headers=headers)
        return response

    def handle_index(self):
        for i in range(6):
            url = "https://mapi.kyboye.com/club/thread/list?fid=136&type=1&typeid=0&skip=" + \
                str(26 + i * 20) + "&psize=20"
            response = self.handle_requests(url)
            response_dict = json.loads(response.text)
            for dataline in response_dict['res']['list']:
                friends_info = {}
                friends_info['uid'] = dataline['uid']
                friends_info['uname'] = dataline['uname']
                friends_info['title'] = dataline['title']
                friends_info['icon'] = dataline['icon']
                friends_info['content'] = dataline['content']
                friends_info['pics'] = dataline['pics']
                self.save_to_mongo(friends_info)
                print(friends_info)

    def save_to_mongo(self, result):
        if self.db['friends'].insert(result):
            print("保存成功")


if __name__ == '__main__':
    k = Kaoyanbang()
    k.handle_index()
