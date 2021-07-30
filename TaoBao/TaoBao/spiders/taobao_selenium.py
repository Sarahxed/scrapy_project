import time

import scrapy
from urllib.parse import quote

from scrapy import Request
from TaoBao.items import TaobaoItem


class TaobaoSeleniumSpider(scrapy.Spider):
    name = 'taobao_selenium'
    allowed_domains = ['www.taobao.com']
    base_url = 'https://s.taobao.com/search?q={}'

    def start_requests(self):
        for keyword in self.settings.get('KEYWORDS'):
            time.sleep(1)
            for page in range(1, self.settings.get('MAX_PAGE') + 1):
                time.sleep(3)
                url = self.base_url.format(quote(keyword))
                yield Request(url=url, callback=self.parse, meta={'page': 'page'}, dont_filter=True)

    def parse(self, response, **kwargs):
        time.sleep(2000)
        products = response.xpath("//div[@class='items'][1]//div[contains(@class, 'item')]")
        for product in products:
            item = TaobaoItem()
            item["price"] = "".join(product.xpath(".//div[contains(@class, 'price')]//text()").extract()).strip()
            item["title"] = "".join(product.xpath(".//div[contains(@class, 'title')]//text()").extract()).strip()
            item["shop"] = "".join(product.xpath(".//div[contains(@class, 'shop')]//text()").extract()).strip()
            item["image"] = "".join(product.xpath(".//div[contains(@class, 'image')]//text()").extract()).strip()
            item["deal"] = product.xpath(".//div[contains(@class, 'deal-cnt')]//text()").extract_first()
            item["location"] = product.xpath(".//div[contains(@class, 'location')]//text()").extract_first()
            yield item



