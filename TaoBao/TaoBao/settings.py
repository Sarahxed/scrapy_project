
BOT_NAME = 'TaoBao'
SPIDER_MODULES = ['TaoBao.spiders']
NEWSPIDER_MODULE = 'TaoBao.spiders'

ROBOTSTXT_OBEY = False
DOWNLOAD_DELAY = 3

DEFAULT_REQUEST_HEADERS = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
  'Accept-Language': 'en',
  # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
}


ITEM_PIPELINES = {
   'TaoBao.pipelines.MongoPipeline': 300,
}

DOWNLOADER_MIDDLEWARES = {
   'TaoBao.middlewares.SeleniumMiddleware': 543,
}
SELENIUM_TIMEOUT = 10
USERNAME = 'xxx'
PASSWORD = 'xxx'

KEYWORDS = ['xxx']
MAX_PAGE = 3
MONGO_URI = 'localhost'
MONGO_DB = 'taobao'

