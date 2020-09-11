#!/usr/bin/python3
# -*- encoding: utf-8 -*-
"""
@desc  : 
@author: Sarah
@file  : __init__.py.py
@time  : 2020/9/7 23:02
"""
import pymysql
from pymysql.cursors import DictCursor


class DataBase():
    def __init__(self):
        self.conn = pymysql.Connection(
            host='localhost',
            port=3306,
            user='root',
            password='root',
            db='qidian',
            charset='utf8',
            cursorclass=DictCursor
        )

    def __enter__(self):
        return self.conn.cursor(cursor=DictCursor)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.conn.rollback()
        else:
            self.conn.commit()
        return True

    def close(self):
        self.conn.close()


class BaseDao:
    def __init__(self):
        self.db = DataBase()

    def save(self, table_name, **item):
        sql = 'insert into %s(%s) value (%s)'
        fields = ",".join(item.keys())
        fields_placeholds = ','.join(['%%(%s)s' %key for key in item])

        with self.db as cursor:
            cursor.execute(sql % (table_name, fields, fields_placeholds), item)

            # 判断是否执行成功：看表中被修改的行数是否>0
            if cursor.rowcount > 0:
                return True
        return False