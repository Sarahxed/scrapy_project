# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

import os
from csv import DictWriter
from scrapy import Spider

from qidian.db import BaseDao
from qidian.items import BookItem, SegItem


class QidianPipeline:
    """存储到csv文件"""
    def __init__(self):
        self.book_csv = 'book.csv'
        self.seg_csv = 'seg.csv'
        self.seg_detail_csv = 'seg_detail.csv'

    def save_csv(self, item, filename):
        has_header = os.path.exists(filename)
        with open(filename, 'a', encoding="utf8") as f:
            writer = DictWriter(f, fieldnames=item.keys())
            if not has_header:
                writer.writeheader()
            writer.writerow(item)

    def process_item(self, item, spider: Spider):
        if isinstance(item, BookItem):
            self.save_csv(item, self.book_csv)
        elif isinstance(item, SegItem):
            self.save_csv(item, self.seg_csv)
        else:
            self.save_csv(item, self.seg_detail_csv)
        return item


class DBPipline:
    """存储到数据库"""
    def __init__(self):
        self.dao = BaseDao()
        self.book_table = 't_book'
        self.seg_table = 't_seg'
        self.seg_detail_table = 't_detail_seg'

    def process_item(self, item, spider):
        if isinstance(item, BookItem):
            item['tags'] = "|".join(item["tags"])
            self.dao.save(self.book_table, **item)
        elif isinstance(item, SegItem):
            self.dao.save(self.seg_table, **item)
        else:
            self.dao.save(self.seg_detail_table, **item)
        return item