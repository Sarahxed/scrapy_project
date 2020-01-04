# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

from scrapy.exceptions import DropItem


class TutorialPipeline(object):
    def process_item(self, item, spider):
        return item


class TextPipeline(object):
    """筛选掉长度大于50的text"""

    def __init__(self):
        self.limit = 50

    def process_item(self, item, spider):
        if item["text"]:
            if len(item["text"]) > self.limit:
                item["text"] = item["text"][0: self.limit].rstrip() + "..."
            return item
        else:
            # 如果不存在抛出DropItem异常
            return DropItem("Miss Text")


class MongoPipline(object):
    def __init__(self, mongo_uri, mongo_db):
        """配置mongodb数据库"""
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        """通过crawler拿到全局的配置的每个配置信息"""
        return cls(
            mongo_uri=crawler.settings.get("MONGO_URI"),
            mongo_db=crawler.settings.get("MONGO_DB")
        )

    def open_spider(self, spider):
        """初始化操作"""
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        name = item.__class__.__name__
        self.db[name].insert(dict(item))
        return item

    def close_spider(self, spider):
        """关闭数据库连接"""
        self.client.close()
