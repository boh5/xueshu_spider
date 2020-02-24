# xueshu_spider
> A spider to crawl papers by xueshu.baidu.com, and download papers <br>
> 本爬虫可根据提供的关键词爬取百度学术搜索到的相关论文信息，并下载这些论文

### 使用方法
1. 配置 `xueshu_spider/XueshuSpider/settings.py` 文件最下方的 MySQL URI 和 用户名、密码等信息
2. 配置 `xueshu_spider/XueshuSpider/spiders/xueshu.py` 脚本中 `key_word` 变量，提供关键字，若有多个关键字使用 '+' 分隔
3. 运行 `main.py` 脚本，开始爬取论文信息
4. 配置 `xueshu_spider/XueshuSpider/tools/paper_download.py` 脚本中的数据库连接、论文下载路径和浏览器驱动（如 chromedriver.exe）路径
5. 运行 `paper_download.py` 脚本，开始下载论文
