# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
from twisted.enterprise import adbapi


class XueshuspiderPipeline(object):
    def process_item(self, item, spider):
        return item


class MysqlTwistedPipeline(object):
    # 将数据存入数据库
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = (dict(host=settings['MYSQL_HOST'], db=settings['MYSQL_DBNAME'], user=settings['MYSQL_USER'],
                        password=settings['MYSQL_PASSWORD'], charset='utf8',
                        cursorclass=MySQLdb.cursors.DictCursor, use_unicode=True))

        dbpool = adbapi.ConnectionPool('MySQLdb', **dbparms)

        return cls(dbpool)

    def process_item(self, item, spider):
        # 使用twisted 异步mysql
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error)  # 处理异常

    @classmethod
    def handle_error(cls, failure):
        # 处理异步插入的异常
        print(failure)

    @classmethod
    def do_insert(cls, cursor, item):
        # 执行具体插入
        insert_sql = """
        insert into paper
        (title, author, publication, cited, summary, key_word, organization, date_year, url, is_down) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        (cursor.execute(insert_sql, (item['title'], item['author'], item['publication'], item['cited'],
                                     item['summary'], ','.join(item['key_word']), item['organization'],
                                     item['date_year'], item['url'], item['is_down'],)))


class DefaultValuesPipeline(object):
    # 设置 item默认值
    def process_item(self, item, spider):
        item.setdefault('summary', 'None')
        item.setdefault('key_word', 'None')
        item.setdefault('organization', 'None')
        # ...
        return item