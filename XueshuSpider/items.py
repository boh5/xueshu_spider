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


def date_convert(value):
    try:
        create_date = datetime.datetime.strptime(value, '%Y').date()
    except Exception as e:
        create_date = datetime.datetime.now().date()
        print(e)
    return create_date


def get_key_word(value):
    return value.replace('\r\n', '').replace(' ', '').replace(';', '')


class PaperItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


class PaperItem(scrapy.Item):
    title = scrapy.Field()
    author = scrapy.Field()
    publication = scrapy.Field()
    cited = scrapy.Field()
    summary = scrapy.Field()
    key_word = scrapy.Field(output_processor=MapCompose(get_key_word))
    organization = scrapy.Field()
    date_year = scrapy.Field(input_processor=MapCompose(date_convert))
    url = scrapy.Field()
    is_down = scrapy.Field()
