# -*- coding: utf-8 -*-
import re
from urllib import parse

from pydispatch import dispatcher
from pyvirtualdisplay import Display
from scrapy import signals
from scrapy.http.request import Request

import scrapy
from scrapy.loader import ItemLoader
from selenium import webdriver

from XueshuSpider.items import PaperItem, PaperItemLoader


class XueshuSpider(scrapy.Spider):
    name = 'xueshu'
    allowed_domains = ['xueshu.baidu.com','kns.cnki.net', 'd.wanfangdata.com.cn', 'cqvip.com', 'cdmd.cnki.com.cn', 'www.wanfangdata.com.cn', 'cpfd.cnki.com.cn']
    # allowed_domains = ['d.wanfangdata.com.cn', 'www.wanfangdata.com.cn', 'xueshu.baidu.com']
    baidu_xueshu_page = 0
    key_word = 'python+爬虫'
    start_urls = ['http://xueshu.baidu.com/s?wd={0}'.format(key_word)]

    # def __init__(self):
    #     # # 无界面
    #     # display = Display(visible=0, size=(800, 600))
    #     # display.start()
    #
    #     # 打开chrome
    #     self.browser = webdriver.Chrome(executable_path='D:\Files\PythonProject\chromedriver.exe')
    #     super(XueshuSpider, self).__init__()
    #
    #     # 爬虫关闭时关闭
    #     dispatcher.connect(self.spider_closed, signals.spider_closed)

    # def spider_closed(self, spider):
    #     # 爬虫退出时，关闭chrome
    #     print('spider closed')
    #     self.browser.quit()

    def get_real_link(self, complex_link):
        # 通过a标签下的链接，返回文献的真实链接
        real_link = ''
        if complex_link == '':
            return real_link
        if re.match(r'.*(http://d.wanfangdata.com.cn).*', complex_link):
            real_link = complex_link.strip()
        elif 'www.cqvip.com' in complex_link:  # 除了维普的url，加上最后的‘&ie=utf-8&sc_us=15241318161589336391’就不会被重定向
            complex_link = parse.unquote(complex_link)
            real_link_group = re.match(r'.*sc_vurl=(http.*)$', complex_link)
            if real_link_group:
                real_link = real_link_group.group(1)
        else:
            complex_link = parse.unquote(complex_link)
            real_link_group = re.match(r'.*sc_vurl=(http.*)&ie.*', complex_link)
            if real_link_group:
                real_link = real_link_group.group(1)
        return real_link

    def parse(self, response):
        # with open('test.html', 'w', encoding='utf-8') as f:
        #     f.write(response.text)
        # link = response.xpath('//*[@id="2"]/div[1]/div[2]/div/span[4]/a/@href')
        # url = parse.unquote(link.extract()[0])
        # cnki_link_re = re.match(r'.*sc_vurl=(http:.*dbcode=CJFQ)&ie.*', url)
        # if cnki_link_re:
        #     cnki_link = cnki_link_re.group(1)
        #     print(cnki_link)
        post_nodes = response.css('#bdxs_result_lists .result')
        for post_node in post_nodes:
            meta_info = {}
            title_redundant = ''.join(post_node.css('.c_font a').extract()).replace('<em>', '').replace('</em>', '')
            title_re = re.match(r'.*target="_blank">(.*)</a>', title_redundant)
            if title_re:
                title = title_re.group(1)
            else:
                title = ''

            info_div = post_node.css('.sc_info')
            author = ','.join(info_div.css('span:nth-child(1) a::text').extract())
            publication_test = info_div.css('span:nth-child(2) a::text').extract_first('None').strip()
            if publication_test != 'None':
                publication = publication_test
            else:
                publication = info_div.css('span:nth-child(2)::text').extract_first('None').strip()
            date_year_cache = info_div.css('.sc_time::attr(data-year)').extract_first('0').strip()
            if date_year_cache != '0':
                date_year = int(date_year_cache)
            else:
                date_year = 0
            if date_year == publication:
                publication = 'None'
            cited_selector = info_div.css('span:last-child a::text')
            if cited_selector:
                cited = int(cited_selector.extract_first())
            else:
                cited = 0

            meta_info = {'title': title, 'author': author, 'publication': publication, 'date_year': date_year, 'cited': cited}

            link_nodes = post_node.css('.sc_allversion .v_item_span')
            complex_link = ''
            # todo 万方first
            for link_node in link_nodes:
                if '万方' in link_node.css('a::attr(title)').extract_first():
                    meta_info['site'] = '万方'
                    complex_link = link_node.css('a::attr(href)').extract()[0]
                    break
                if '知网' in link_node.css('a::attr(title)').extract_first():
                    complex_link = link_node.css('a::attr(href)').extract()[0]
                    break
                # todo 维普
                # if '维普' in link_node.css('a::attr(title)').extract_first():
                #     complex_link = link_node.css('a::attr(href)').extract()[0]
                #     break

            real_link = self.get_real_link(complex_link)
            if re.match(r'^(http://cdmd).*', real_link):
                meta_info['site'] = '知网空间'
            if re.match(r'^(http://kns).*', real_link):
                meta_info['site'] = '知网期刊'
            if re.match(r'^(http://cpfd).*', real_link):
                meta_info['site'] = 'cpfd知网'

            # todo judge cqvip url
            # if re.match(r'^(http://www.cqvip.com).*', real_link):
            #     meta_info['site'] = 'www维普'
            # if re.match(r'^(http://qikan.cqvip.com).*', real_link):
            #     meta_info['site'] = 'qikan维普'
            if real_link != '':
                yield Request(url=real_link, meta=meta_info, callback=self.parse_detail)

        next_page_node = response.css('#page a:last-child')
        if next_page_node.css('::text').extract_first('').replace('>', '') == '下一页':
            sub_next_link = next_page_node.css('::attr(href)').extract_first('')
            next_link = parse.urljoin(response.url, sub_next_link)
            yield Request(url=parse.unquote(next_link), callback=self.parse)
        else:
            return

    def parse_detail(self, response):
        title = response.meta.get('title')
        author = response.meta.get('author')
        publication = response.meta.get('publication')
        date_year = response.meta.get('date_year')
        cited = response.meta.get('cited')
        site = response.meta.get('site')
        # item_loader
        item_loader = PaperItemLoader(item=PaperItem(), response=response)
        item_loader.add_value('title', title)
        item_loader.add_value('author', author)
        item_loader.add_value('publication', publication)
        item_loader.add_value('date_year', date_year)
        item_loader.add_value('cited', cited)
        item_loader.add_value('url', response.url)
        item_loader.add_value('is_down', 0)

        if site == '万方':
            item_loader.add_css('summary', '#see_alldiv::text')
            # key_word_node = response.css('ul.info')
            # if key_word_node.css('li:nth-child(1) .info_left::text').extract_first('').strip() == '关键词：':
            #     key_word = key_word_node.css('li:nth-child(1) .info_right a::text').extract()
            # else:
            #     key_word = key_word_node.css('li:nth-child(2) .info_right a::text').extract()
            # item_loader.add_value('key_word', key_word)
            # item_loader.add_css('organization', '.info > li:nth-child(3) > div:nth-child(2) > a:nth-child(1)::text')

            info_nodes = response.css('ul.info li')
            key_word = ['']
            organization = ''
            for info_node in info_nodes:
                info_left = info_node.css('.info_left::text').extract_first('')
                if info_left == '关键词：':
                    key_word = info_node.css('.info_right a::text').extract()
                if info_left == '作者单位：' or info_left == '学位授予单位：':
                    organization = info_node.css('.info_right a::text').extract_first('')
            item_loader.add_value('key_word', key_word)
            item_loader.add_value('organization', organization)

        if site == '知网空间':
            item_loader.add_css('summary', 'div[style="text-align:left;word-break:break-all"]::text')
            item_loader.add_value('organization', publication.replace('《', '').replace('》', ''))

            key_word_cache = response.css('head meta[name="keywords"]::attr(content)').extract_first('None')
            item_loader.add_value('key_word', key_word_cache.split())

        if site == '知网期刊':
            item_loader.add_css('summary', '#ChDivSummary::text')
            item_loader.add_css('key_word', '.wxBaseinfo a[onclick*="TurnPageToKnet(\'kw\'"]::text')
            item_loader.add_css('organization', '.orgn > span:nth-child(1) > a:nth-child(1)::text')

        if site == 'cpfd知网':
            item_loader.add_css('summary', 'div.xx_font:nth-child(4)::text')
            item_loader.add_css('organization', 'div.xx_font:nth-child(5) > a:nth-child(2)::text')

            key_word_cache = response.css('head meta[name="keywords"]::attr(content)').extract_first('None')
            item_loader.add_value('key_word', key_word_cache.split())



        # todo 维普item
        # if site == 'qikan维普':
        #     item_loader.add_css('summary', 'p.abstrack:nth-child(5)::text')
        #     item_loader.add_css('key_word', 'p.subject .tip a::text')
        #     item_loader.add_css('organization', 'p.organ > span:nth-child(2) > a:nth-child(2)::text')
        #
        # if site == 'www维普':
        #     item_loader.add_css('summary', '.ditailinfo .datainfo .sum:nth-child(2)::text')
        #     item_loader.add_css('key_word', 'table.datainfo:nth-child(3) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(2) a::text')
        #     item_loader.add_css('organization', '.detailtitle > strong:nth-child(2) > i:nth-child(1) > a:nth-child(3)::text')

        paper_item = item_loader.load_item()
        yield paper_item
