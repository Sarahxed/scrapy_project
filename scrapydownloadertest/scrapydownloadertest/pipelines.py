# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import time

import pymongo
import pymysql
from scrapy import Request

from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
from scrapy.utils.project import get_project_settings
from twisted.enterprise import adbapi


class ScrapydownloadertestPipeline(object):
    def process_item(self, item, spider):
        return item


class MongoPipline(object):
    """mongodb存储数据"""

    def __init__(self, mongo_uri, mongo_db):
        """初始化"""
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, clawler):
        """从配置中读取参数"""
        return cls(
            mongo_uri=clawler.settings.get('MONGO_URI'),
            mongo_db=clawler.settings.get('MONGO_DB'),
        )

    def open_spider(self, spider):
        """配置客户端"""
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        """处理item"""
        self.db[item.collection].insert(dict(item))
        return item

    def close_spider(self, spider):
        """关闭客户端"""
        self.client.close()


class MysqlPipeline(object):
    """mysql存储数据1"""

    def __init__(self, host, port, database, user, password):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('MYSQL_HOST'),
            port=crawler.settings.get('MYSQL_PORT'),
            database=crawler.settings.get('MYSQL_DATABASE'),
            user=crawler.settings.get('MYSQL_USER'),
            password=crawler.settings.get('MYSQL_PASSWORD'),
        )

    def open_spider(self, spider):
        self.db = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database,
                                  port=self.port, charset="utf8")
        self.cursor = self.db.cursor()

    def close_spider(self, spider):
        self.db.close()

    def process_item(self, item, spider):
        data = dict(item)
        keys = ','.join(data.keys())
        values = ','.join(['%s'] * len(data))
        sql = 'insert into %s (%s) values (%s)' % (item.table, keys, values)
        self.cursor.execute(sql, tuple(data.values()))
        self.db.commit()
        return item


class DBHelper(object):
    """mysql存储数据"""

    def __init__(self):
        settings = get_project_settings()  # 获取settings配置，设置需要的信息

        dbparams = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',  # 编码要加上，否则可能出现中文乱码问题
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=False,
        )
        # **表示将字典扩展为关键字参数,相当于host=xxx,db=yyy....
        dbpool = adbapi.ConnectionPool('pymysql', **dbparams)

        self.dbpool = dbpool

    def connect(self):
        return self.dbpool

    # 创建数据库
    def insert(self, item):
        data = dict(item)
        keys = ','.join(data.keys())
        values = ','.join(['%s'] * len(data))
        sql = 'insert into %s (%s) values (%s)' % (item.table, keys, values)
        # 调用插入的方法
        query = self.dbpool.runInteraction(self._conditional_insert, sql, item)
        # 调用异常处理方法
        query.addErrback(self._handle_error)
        return item

    # 写入数据库中
    def _conditional_insert(self, tx, sql, item):
        item['created_at'] = time.strftime('%Y-%m-%d %H:%M:%S',
                                           time.localtime(time.time()))
        params = (item["title"], item['image'], item['brief'],
                  item['course_url'], item['created_at'])
        tx.execute(sql, params)


class ImagePipeline(ImagesPipeline):
    """下载图片"""
    print('进入图片下载管道')

    def file_path(self, request, response=None, info=None):
        """获得保存文件名"""
        url = request.url
        file_name = url.split("/")[-1]
        print('*' * 100)
        print(url)
        print(file_name)
        return file_name

    def item_completed(self, results, item, info):
        """分析下载结果并提出下载失败的图片"""
        image_paths = [x['path'] for ok, x in results if ok]
        print('-' * 100)
        print(image_paths)
        if not image_paths:
            raise DropItem('Image Download Failed')
        return item

    def get_media_requests(self, item, info):
        """将图片链接加入到调度队列"""
        yield Request(item['url'])
