# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import time

from fake_useragent import UserAgent
from scrapy.http import HtmlResponse

from XueshuSpider.tools.crawl_xici_ip import GetIp


class RandomUserAgentMiddleware(object):
    # 随机更换User-Agent

    def __init__(self, crawler):
        super(RandomUserAgentMiddleware, self).__init__()
        self.ua = UserAgent()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_request(self, request, spider):
        request.headers.setdefault('User-Agent', self.ua.random)


class RandomProxyMiddleware(object):
    # 动态ip代理
    @classmethod
    def process_request(cls, request, spider):
        get_ip = GetIp
        request.meta['proxy'] = get_ip.get_random_ip(GetIp())
        print(request.meta['proxy'])


class JSPageMiddleware(object):
    @classmethod
    def process_request(cls, request, spider):
        if spider.name == 'xueshu':
            spider.browser.get(request.url)
            time.sleep(3)

            return HtmlResponse(url=spider.browser.current_url, body=spider.browser.page_source, encoding='utf-8',
                                request=request)  # 遇到HtmlResponse，scrapy不会再下载网页
