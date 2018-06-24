# -*- coding: utf-8 -*-
import re
from urllib import parse
from scrapy.http.request import Request

import scrapy
from scrapy.loader import ItemLoader

from XueshuSpider.items import PaperItem, PaperItemLoader


class XueshuSpider(scrapy.Spider):
    name = 'xueshu'
    allowed_domains = ['xueshu.baidu.com','kns.cnki.net', 'd.wanfangdata.com.cn', 'cqvip.com', 'cdmd.cnki.com.cn', 'www.wanfangdata.com.cn']
    baidu_xueshu_page = 0
    start_urls = ['http://xueshu.baidu.com/s?wd=python%20%E7%88%AC%E8%99%AB&pn={0}&tn=SE_baiduxueshu_c1gjeupa&ie=utf-8&sc_f_para=sc_tasktype%3D%7BfirstSimpleSearch%7D&sc_hit=1&rsv_page=1'.format(baidu_xueshu_page)]


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
            publication = info_div.css('span:nth-child(2) a::text').extract_first('').strip()
            date_year = info_div.css('span:nth-child(3)::text').extract_first('').strip()
            cited_selector = info_div.css('span:nth-child(4) a::text')
            if cited_selector:
                cited = int(cited_selector.extract_first())
            else:
                cited = 0

            meta_info = {'title': title, 'author': author, 'publication': publication, 'date_year': date_year, 'cited': cited}

            link_nodes = post_node.css('.sc_allversion .v_item_span')
            complex_link = ''
            for link_node in link_nodes:
                # if '万方' in link_node.css('a::attr(title)').extract_first():
                #     meta_info['site'] = '万方'
                #     complex_link = link_node.css('a::attr(href)').extract()[0]
                #     break
                # if '知网' in link_node.css('a::attr(title)').extract_first():
                #     complex_link = link_node.css('a::attr(href)').extract()[0]
                #     break
                # todo 维普
                if '维普' in link_node.css('a::attr(title)').extract_first():
                    complex_link = link_node.css('a::attr(href)').extract()[0]
                    break

            real_link = self.get_real_link(complex_link)
            if re.match(r'^(http://cdmd).*', real_link):
                meta_info['site'] = '知网空间'
            if re.match(r'^(http://kns).*', real_link):
                meta_info['site'] = '知网期刊'
            if re.match(r'^(http://www.cqvip.com).*', real_link):
                meta_info['site'] = 'www维普'
            if re.match(r'^(http://qikan.cqvip.com).*', real_link):
                meta_info['site'] = 'qikan维普'
            if real_link != '':
                yield Request(url=real_link, meta=meta_info, callback=self.parse_detail, dont_filter=True)

        self.baidu_xueshu_page += 10
        next_link = 'http://xueshu.baidu.com/s?wd=python%20%E7%88%AC%E8%99%AB&pn={0}&tn=SE_baiduxueshu_c1gjeupa&ie=utf-8&sc_f_para=sc_tasktype%3D%7BfirstSimpleSearch%7D&sc_hit=1&rsv_page=1'.format(self.baidu_xueshu_page)
        yield Request(url=parse.unquote(next_link), callback=self.parse)

        pass


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
        print(response.url)
        item_loader.add_value('url', response.url)

        # todo file_path
        item_loader.add_value('file_path', 'file_path')

        if site == '万方':
            item_loader.add_css('summary', '#see_alldiv::text')
            item_loader.add_css('key_word', '.info > li:nth-child(1) > div:nth-child(2) a::text')
            item_loader.add_css('organization', '.info > li:nth-child(3) > div:nth-child(2) > a:nth-child(1)::text')

        if site == '知网空间':
            item_loader.add_css('summary', 'div.xx_font:nth-child(4) > font:nth-child(1)::text')
            item_loader.add_value('key_word', '')
            item_loader.add_css('organization', 'div.xx_font:nth-child(5)::text')

        if site == '知网期刊':
            item_loader.add_css('summary', '#ChDivSummary::text')
            item_loader.add_css('key_word', '.wxBaseinfo > p:nth-child(3) a::text')
            item_loader.add_css('organization', '.orgn > span:nth-child(1) > a:nth-child(1)::text')



        # todo 维普item
        if site == 'qikan维普':
            item_loader.add_css('summary', 'p.abstrack:nth-child(5)::text')
            item_loader.add_css('key_word', 'p.subject .tip a::text')
            item_loader.add_css('organization', 'p.organ > span:nth-child(2) > a:nth-child(2)::text')

        if site == 'www维普':
            item_loader.add_css('summary', '.sum::text')
            item_loader.add_css('key_word', 'table.datainfo:nth-child(3) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(2) a::text')
            item_loader.add_css('organization', '.detailtitle > strong:nth-child(2) > i:nth-child(1) > a:nth-child(3)::text')

        paper_item = item_loader.load_item()
        yield paper_item
