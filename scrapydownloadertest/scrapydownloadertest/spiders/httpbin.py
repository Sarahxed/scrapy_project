# -*- coding: utf-8 -*-
import json
from urllib.parse import urlencode

import scrapy
from scrapy import Request

from scrapydownloadertest.items import ImageItem

"""
scrapy360美图前50页爬取
站点：images.so.com
存储：数据库(mysql/mongodb)存储图片信息：id 图片链接 标题 缩略图链接
     通过图片链接下载图片到本地
"""


class HttpbinSpider(scrapy.Spider):
    name = 'images360'
    allowed_domains = ['images.so.com', 'https://p0.ssl.qhimgs1.com/']
    start_urls = ['https://image.so.com/zjl?ch=art&sn=30&listtype=new&temp=1']

    def start_requests(self):
        """构造页码请求链接生成函数"""
        data = {'ch': 'photography', 'listtype': 'new'}
        base_url = 'https://image.so.com/zjl?'
        for page in range(1, self.settings.get('MAX_PAGE') + 1):
            data['sn'] = page * 30
            params = urlencode(data)
            url = base_url + params
            yield Request(url, self.parse)

    def parse(self, response):
        print(response)
        """解析信息"""
        result = json.loads(response.text)
        for image in result.get('list'):
            item = ImageItem()
            item['id'] = image.get("id")
            item['url'] = image.get("qhimg_url")
            item['title'] = image.get("title")
            item['thumb'] = image.get("qhimg_thumb")
            yield item



