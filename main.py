"""

@Author  : dilless
@Time    : 2018/6/23 1:01
@File    : main.py
"""

import os
import sys

from scrapy.cmdline import execute

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(['scrapy', 'crawl', 'xueshu'])
