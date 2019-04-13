# -*- coding: utf-8 -*-
# @AuThor  : frank_lee
import requests
import MySQLdb.cursors
conn = MySQLdb.connect(
    host="127.0.0.1",
    user="root",
    passwd="",
    db="ip_pool",
    charset="utf8")
cursor = conn.cursor()


class Get_Ip(object):

    def delete_ip(self, ip):
        delete_sql = """
           delete from iptable where ip_addr = '{0}'
        """.format(ip)
        cursor.execute(delete_sql)
        conn.commit()
        return True

    def judge_ip(self, ip, port):
        # 判断一个ip是否可用
        http_url = "http://www.baidu.com"
        proxy_url = "http://{0}:{1}".format(ip, port)
        try:
            proxy_dict = {
                "http": proxy_url,
            }
            response = requests.get(http_url, proxies=proxy_dict)
        except Exception as e:
            print("invalid ip and port")
            self.delete_ip(ip)
            return False
        else:
            code = response.status_code
            if (code >= 200) and (code < 300):
                print("effective ip")
                return proxy_dict
            else:
                print("invalid ip and port")
                self.delete_ip(ip)
                return False

    def get_random_ip(self):
        # 从数据库中随机取出一个可用的ip
        random_sql = """
            SELECT ip_addr, ip_port FROM iptable ORDER BY RAND() LIMIT 1
        """
        cursor.execute(random_sql)
        for ip_info in cursor.fetchall():
            ip = ip_info[0]
            port = ip_info[1]
            judgeip = self.judge_ip(ip, port)
            if judgeip:
                # return "http://{0}:{1}".format(ip, port)
                return judgeip
            else:
                return self.get_random_ip()
