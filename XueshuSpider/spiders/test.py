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
    parsed_url = parse.unquote('http://xueshu.baidu.com/s?wd=python+%E7%88%AC%E8%99%AB&rsv_bp=0&tn=SE_baiduxueshu_c1gjeupa&rsv_spt=3&ie=utf-8&f=8&rsv_sug2=0&sc_f_para=sc_tasktype%3D%7BfirstSimpleSearch%7D')
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
