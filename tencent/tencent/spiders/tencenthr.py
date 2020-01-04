# -*- coding: utf-8 -*-
from scrapy.spider import CrawlSpider
from scrapy.spider import Rule  # 提取超链接的规则
from scrapy.linkextractor import LinkExtractor  # 提取超链接
from tencent.items import TencentItem

"""
CrawlSpider按照规则深度提取链接
站点：hr.tencent.com
存储：职位名，详情链接， 职位类别， 招聘人数， 工作地点， 发布时间
"""


class TencenthrSpider(CrawlSpider):
    name = 'tencenthr'
    allowed_domains = ['hr.tencent.com']
    start_urls = ['https://careers.tencent.com/search.html?&start=10#a']

    # 提取超链接
    page_links = LinkExtractor(allow=("start=\d+"))
    # 按照提取规则提取链接，返回datalist类型,follow:True 一直提取下去  callback:回调处理函数
    rules = [Rule(page_links, callback="parse_tencent", follow=True)]

    def parse_tencent(self, response):
        for each in response.xpath("//tr[@class='even'] | //tr[@class='odd']"):
            item = TencentItem()
            # 职位名称
            item['positionname'] = each.xpath("./td[1]/a/text()").extract()[0]
            # 详情连接
            item['positionlink'] = each.xpath("./td[1]/a/@href").extract()[0]
            # 职位类别
            item['positionType'] = each.xpath("./td[2]/text()").extract()[0]
            # 招聘人数
            item['peopleNum'] = each.xpath("./td[3]/text()").extract()[0]
            # 工作地点
            item['workLocation'] = each.xpath("./td[4]/text()").extract()[0]
            # 发布时间
            item['publishTime'] = each.xpath("./td[5]/text()").extract()[0]
            yield item