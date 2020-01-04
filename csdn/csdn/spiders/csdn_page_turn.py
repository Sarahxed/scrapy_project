# -*- coding: utf-8 -*-
import re

import scrapy
import requests

from lxml import etree
from csdn.items import CsdnItem

"""
scrapy实现自动翻页爬取信息
站点：https://edu.csdn.net/lecturer?&page=0
存储信息：讲师名字 课程数 学生数 简介

"""


class CsdnPageTurnSpider(scrapy.Spider):
    name = 'csdn_page_turn'
    allowed_domains = ['edu.csdn.net']
    start_urls = ['https://edu.csdn.net/lecturer?&page=0']
    offset = 1

    def __init__(self):
        self.pages = self.page_numbers(self.start_urls[0])

        super().__init__()

    @staticmethod
    def page_numbers(url):
        sess = requests.session()
        resp = sess.get(url=url, verify=False, timeout=15).content.decode("utf-8", errors="ignore")
        etree_obj = etree.HTML(resp)
        mytext = etree_obj.xpath('//span[@class="text"][last()]/text()')[1]
        regex = re.compile("\d+", re.IGNORECASE)
        lines = eval(regex.findall(mytext)[0])
        if lines % 20 == 0:
            pages = lines // 20
        else:
            pages = lines // 20 + 1

        return pages

    def parse(self, response):
        mytree = response
        nodedata = mytree.xpath("//*[@class=\"panel-body\"]//dl/dd/p/text()").extract()
        nodename = mytree.xpath("//*[@class=\"panel-body\"]//dl/dd/ul//li[1]/a/text()").extract()
        nodelessions = mytree.xpath("//*[@class=\"panel-body\"]//dl/dd/ul//li[2]/span/text()").extract()
        nodestudents = mytree.xpath("//*[@class=\"panel-body\"]//dl/dd/ul//li[3]/span/text()").extract()
        for i in range(len(nodedata)):
            csdnitem = CsdnItem()
            csdnitem["name"] = nodename[i]
            csdnitem["lessons"] = nodelessions[i]
            csdnitem["students"] = nodestudents[i]
            csdnitem["introduction"] = nodedata[i]
            yield csdnitem
        if self.offset <= 20:
            self.offset += 1
        new_url = "http://edu.csdn.net/lecturer?&page=" + str(self.offset)
        yield scrapy.Request(new_url, self.parse)
