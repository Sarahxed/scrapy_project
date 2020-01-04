# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapydownloadertestItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class ImageItem(scrapy.Item):
    collection = table = "images"
    id = scrapy.Field()   # id
    url = scrapy.Field()  # 链接
    title = scrapy.Field()  # 标题
    thumb = scrapy.Field()  # 缩率图
