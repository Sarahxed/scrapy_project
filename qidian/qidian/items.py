# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookItem(scrapy.Item):
    book_id = scrapy.Field()
    book_name = scrapy.Field()
    book_url = scrapy.Field()
    book_cover = scrapy.Field()
    author = scrapy.Field()
    summary = scrapy.Field()
    tags = scrapy.Field()


class SegItem(scrapy.Item):
    """章节"""
    seg_id = scrapy.Field()
    title = scrapy.Field()
    book_id = scrapy.Field()
    url = scrapy.Field()


class SegDetailItem(scrapy.Item):
    """章节详情"""
    seg_id = scrapy.Field()
    content = scrapy.Field()
