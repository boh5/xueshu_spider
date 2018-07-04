"""

@Author  : dilless
@Time    : 2018/6/23 22:26
@File    : crawl_xici_ip.py
"""
import MySQLdb
import requests
from scrapy.selector import Selector

conn = MySQLdb.connect(host='127.0.0.1', user='root', password='root', database='xueshu_spider', charset='utf8')
cursor = conn.cursor()


def crawl_xici_ips():
    # 爬取西刺的ip代理

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/67.0.3396.87 Safari/537.36'}
    for i in range(1, 3000):
        re = requests.get('http://www.xicidaili.com/nn/{0}'.format(i), headers=headers)

        selector = Selector(text=re.text)
        all_trs = selector.css('#ip_list tr')

        ip_list = []
        for tr in all_trs[1:]:
            speed_str = tr.css('.bar::attr(title)').extract()[0]
            if speed_str:
                speed = float(speed_str.split('秒')[0])
            else:
                speed = 0

            all_texts = tr.css('td::text').extract()

            ip = all_texts[0]
            port = all_texts[1]
            if 'HTTP' in all_texts[4]:
                proxy_type = all_texts[4]
            else:
                proxy_type = all_texts[5]

            if proxy_type == 'HTTPS':
                ip_list.append((ip, port, proxy_type, speed))

        for ip_info in ip_list:
            try:
                cursor.execute(
                    "insert into proxy_ips(ip, port, proxy_type, speed) values('{0}', '{1}', '{2}', {3})".format(
                        ip_info[0], ip_info[1], ip_info[2], ip_info[3]
                    )
                )
                conn.commit()
            except Exception as e:
                print(e)


class GetIp(object):
    @classmethod
    def delete_ip(cls, ip):
        delete_sql = "delete from proxy_ips where ip='{0}'".format(ip)
        cursor.execute(delete_sql)
        conn.commit()
        return True

    def judge_ip(self, ip, port):
        # 判断ip是否可用
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                 'Chrome/67.0.3396.87 Safari/537.36'}
        http_url = 'https://xueshu.baidu.com'
        proxy_url = 'https://{0}:{1}'.format(ip, port)
        proxy_dict = {
            'https': proxy_url
        }
        try:
            response = requests.get(http_url, proxies=proxy_dict, headers=headers, timeout=2)
            print(response.text)
        except Exception as e:
            print(e)
            print(proxy_url)
            print('invalid ip and port')
            self.delete_ip(ip)
            return False
        else:
            code = response.status_code
            if 200 <= code < 300:
                print('effective ip')
                return True
            else:
                print('invalid ip and port')
                print(proxy_url)
                self.delete_ip(ip)
                return False

    def get_random_ip(self):
        # 从数据库随机取一个ip
        random_sql = 'select ip, port from proxy_ips order by RAND() LIMIT 1'
        cursor.execute(random_sql)
        for ip_info in cursor.fetchall():
            ip = ip_info[0]
            port = ip_info[1]

            judge_result = self.judge_ip(ip, port)
            if judge_result:
                return 'https://{0}:{1}'.format(ip, port)
            else:
                return self.get_random_ip()


if __name__ == '__main__':
    # crawl_xici_ips()
    get_ip = GetIp()
    print(get_ip.get_random_ip())
