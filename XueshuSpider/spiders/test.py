"""

@Author  : dilless
@Time    : 2018/6/24 15:20
@File    : test.py
"""
import re
from urllib import parse

import requests

from XueshuSpider.spiders.xueshu import XueshuSpider


def test_get_real_link():
    url = 'http://xueshu.baidu.com/s?wd=paperuri%3A%2835c7834e9fb712d2397790c8b9d33a6e%29&filter=sc_long_sign&tn=SE_xueshusource_2kduw22v&sc_vurl=http%3A%2F%2Fwww.cqvip.com%2FQK%2F98258X%2F201715%2F672817447.html&ie=utf-8&sc_us=2506184860150569255'

    xs = XueshuSpider()
    print(xs.get_real_link(url))


def parse_url():
    parsed_url = parse.unquote('http://common.wanfangdata.com.cn/download/download.do?type=perio&resourceId=kxyxxh201724025&resourceTitle=%E7%AE%80%E8%BF%B0%E5%88%A9%E7%94%A8Python%E7%BD%91%E7%BB%9C%E7%88%AC%E8%99%AB%E5%AE%9E%E7%8E%B0%E5%A4%9A%E4%B8%8B%E8%BD%BD%E7%AB%99%E8%BD%AF%E4%BB%B6%E6%90%9C%E7%B4%A2%E5%8F%8A%E4%B8%8B%E8%BD%BD%E5%9C%B0%E5%9D%80%E6%8F%90%E5%8F%96&transaction=%7B%22id%22%3Anull%2C%22transferOutAccountsStatus%22%3Anull%2C%22transaction%22%3A%7B%22id%22%3A%221011248927208398848%22%2C%22status%22%3A1%2C%22createDateTime%22%3Anull%2C%22payDateTime%22%3A1529935507000%2C%22authToken%22%3A%22TGT-2092747-2gcYLfjpMTRHQvYhwJL5xXV1mbZ5GIi9JOdUi1lwDXLeeEsriY-my.wanfangdata.com.cn%22%2C%22user%22%3A%7B%22accountType%22%3A%22Group%22%2C%22key%22%3A%22cddzkjdx%22%7D%2C%22transferIn%22%3A%7B%22accountType%22%3A%22Income%22%2C%22key%22%3A%22PeriodicalFulltext%22%7D%2C%22transferOut%22%3A%7B%22GTimeLimit.cddzkjdx%22%3A3.0%7D%2C%22turnover%22%3A3.0%2C%22productDetail%22%3A%22perio_kxyxxh201724025%22%2C%22productTitle%22%3Anull%2C%22userIP%22%3A%22221.237.82.114%22%2C%22organName%22%3Anull%2C%22memo%22%3Anull%2C%22webTransactionRequest%22%3Anull%2C%22signature%22%3A%22gCb7rqoAmsgiIQ3qAKlEHDxlZsvWwuiGjr2YRRMJJiZiYxAqL5tDgXuI1O5eJ1vANv64hOjWFRnn%5CnWC53XpVvIciyEOqQpMEvZVOyokEaE7Dry90lu56TBYmWsH8HJBlfjtNwmcUPK%2FMUw%2B4hwpXD1Ls6%5CnR7%2Fzw1jvtwhwFmzbBt8%3D%22%2C%22delete%22%3Afalse%7D%2C%22isCache%22%3Afalse%7D')
    print(parsed_url)


def get_cqvip_url():
    complex_url = 'http://xueshu.baidu.com/s?wd=paperuri%3A%2835c7834e9fb712d2397790c8b9d33a6e%29&filter=sc_long_sign&tn=SE_xueshusource_2kduw22v&sc_vurl=http%3A%2F%2Fwww.cqvip.com%2FQK%2F98258X%2F201715%2F672817447.html&ie=utf-8&sc_us=2506184860150569255'
    simple_url = parse.unquote(complex_url)
    cqvip_url = re.match(r'.*sc_vurl=(http.*)&ie.*', simple_url)
    print(cqvip_url.group(1))


def get_cqvip_html():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/67.0.3396.87 Safari/537.36'}
    url = 'http://www.cqvip.com/QK/98258X/201715/672817447.html&ie=utf-8&sc_us=2506184860150569255'
    response =  requests.get(url, headers=headers)
    with open('test.html', 'w', encoding='utf8') as f:
        f.write(response.text)


if __name__ == '__main__':
    # test_get_real_link()
    # get_cqvip_url()
    # get_cqvip_html()
    parse_url()
