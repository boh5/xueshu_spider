# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst


def get_key_word(value):
    return value.replace('\r\n', '').replace(' ', '').replace(';', '')


def get_cnkn_summary(value):
    simple_value = value.replace('\r\n', '').strip()
    if simple_value == '':
        return
    return value


class PaperItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


class PaperItem(scrapy.Item):
    """
    爬虫所需爬取的字段
    """
    title = scrapy.Field()  # 标题
    author = scrapy.Field()  # 作者
    publication = scrapy.Field()  # 出版机构
    cited = scrapy.Field()  # 被引用量
    summary = scrapy.Field(input_processor=MapCompose(get_cnkn_summary))  # 摘要
    key_word = scrapy.Field(output_processor=MapCompose(get_key_word))  # 关键词
    organization = scrapy.Field()  # 所属机构
    date_year = scrapy.Field()  # 出版年份
    url = scrapy.Field()  # 链接地址
    is_down = scrapy.Field()  # 是否已下载
