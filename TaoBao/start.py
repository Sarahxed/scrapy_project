# encoding: utf-8
"""
@author: Sarah
@time: 2020/6/26 17:19
@file: start.py
@desc: 
"""
import sys
import os

from scrapy.cmdline import execute

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(['scrapy', 'crawl', 'taobao_selenium'])

