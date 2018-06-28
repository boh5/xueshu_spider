# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
import datetime
import re

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join, Compose


class XueshuspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


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
    title = scrapy.Field()
    author = scrapy.Field()
    publication = scrapy.Field()
    cited = scrapy.Field()
    summary = scrapy.Field(input_processor=MapCompose(get_cnkn_summary))
    key_word = scrapy.Field(output_processor=MapCompose(get_key_word))
    organization = scrapy.Field()
    date_year = scrapy.Field()
    url = scrapy.Field()
    is_down = scrapy.Field()
