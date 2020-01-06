# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class UniversalItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class NewsItem(scrapy.Item):
    title = scrapy.Field()  # 标题
    url = scrapy.Field()  # 链接
    text = scrapy.Field()  # 正文
    datetime = scrapy.Field()  # 发布时间
    source = scrapy.Field()  # 来源
    website = scrapy.Field()  # 站点名称
