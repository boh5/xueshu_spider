"""

@Author  : dilless
@Time    : 2018/6/25 22:46
@File    : paper_download.py
"""
import re
import time

import MySQLdb
from selenium import webdriver


class MySQLAccess(object):
    def __init__(self):
        self.conn = MySQLdb.connect('127.0.0.1', 'root', 'root', 'xueshu_spider', charset='utf8', use_unicode=True)
        self.cursor = self.conn.cursor()

    def update_file_path(self, file_path, url):
        sql = "update paper set file_path = '{0}' where url = '{1}'".format(file_path, url)
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            print(e)

    def get_urls(self):
        """

        :return: urls tuple in tuple
        """
        sql = "select url from paper where is_down = 0"
        try:
            self.cursor.execute(sql)
            urls = self.cursor.fetchall()
            return urls
        except Exception as e:
            print(e)

    def update_is_down_status(self, url):
        sql = "update paper set is_down = 1 where url = '{0}'".format(url)
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            print(e)


class DownloadPaper():
    def __init__(self):
        options = webdriver.ChromeOptions()
        prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': 'D:\Files\PythonProject\XueshuSpider\down_papers'}
        options.add_experimental_option('prefs', prefs)
        self.browser = webdriver.Chrome(executable_path='D:\Files\PythonProject\chromedriver.exe', chrome_options=options)
        self.browser.implicitly_wait(5)

    def download_paper(self, url):
        self.browser.get(url)
        if re.match(r'^(http://kns.cnki.net).*', url):
            # 知网期刊
            self.browser.find_element_by_css_selector('#pdfDown').click()
        if re.match(r'^(http://http://cdmd.cnki.com.cn).*', url):
            # 知网空间
            self.browser.find_element_by_css_selector('#ty_caj > a:nth-child(1)').click()
        if re.match(r'^(http://cpfd.cnki.com.cn).*', url):
            # cpfd知网
            self.browser.find_element_by_css_selector('#ty_pdf > a:nth-child(1)').click()
        if re.match(r'^(http://www.wanfangdata.com.cn).*', url):
            # 万方
            self.browser.find_element_by_css_selector('#ddownb').click()


if __name__ == '__main__':
    db = MySQLAccess()
    down = DownloadPaper()
    # db.update_file_path('test_path', 'http://kns.cnki.net/KCMS/detail/detail.aspx?filename=dzru201722018&dbname=CJFD&dbcode=CJFQ')
    urls = db.get_urls()
    for url in urls:
        page_url = url[0]
        down.download_paper(page_url)
        db.update_is_down_status(page_url)
