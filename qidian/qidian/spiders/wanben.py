import json
import uuid

from scrapy.http import HtmlResponse

from qidian.items import *


class WanbenSpider(scrapy.Spider):
    name = 'wanben'
    allowed_domains = []
    start_urls = ['https://www.qidian.com/finish']
    token = ''

    def parse(self, response: HtmlResponse):
        self.token = dict(response.headers).get(b'Set-Cookie')[0].decode('utf-8').split(';')[0].split('=')[-1]

        print(self.token)
        print('sdddd')
        if response.status == 200:
            lis = response.css('.all-img-list li')
            for li in lis:
                item = BookItem()
                item['book_id'] = uuid.uuid4().hex
                a = li.xpath('.//div[@class="book-img-box"]/a')
                item['book_url'] = "https:{}".format(a.xpath('./@href').get())
                item['book_cover'] = "https:{}".format(a.xpath('./img/@src').get())
                item['book_name'] = li.xpath('.//div[2]/h4//text()').get()
                item['author'], *item['tags'] = li.css('.author a::text').extract()
                item['summary'] = li.css('.intro::text').get().strip()
                book_singal = item['book_url'].split('/')[-1]
                detail_url = "https://book.qidian.com/ajax/book/category?_csrfToken={}&bookId={}".format(self.token,
                                                                                                         book_singal)

                print(detail_url)
                # 请求详情页章节
                yield scrapy.Request(detail_url, callback=self.parse_info,
                                     meta={'book_id': item['book_id']})

                yield item
            next_page = response.css('.lbf-pagination-item-list').xpath('./li[last()]/a/@href').get()
            if next_page.find('javascript') == -1:  # 存在下一页
                yield scrapy.Request('https:{}'.format(next_page))

    def parse_info(self, response: HtmlResponse):
        """解析小说的详情页章节"""
        book_id = response.meta['book_id']
        chapters = json.loads(response.text).get("data").get('vs')

        for chapter in chapters:
            cs = chapter.get('cs')
            for data in cs:
                item = SegItem()
                item['seg_id'] = uuid.uuid4().hex
                item['book_id'] = book_id
                item['url'] = "https://read.qidian.com/chapter/{}".format(data.get('cU'))  # 章节详情标识
                item['title'] = data.get('cN')  # 章节标题
                yield scrapy.Request(item['url'], callback=self.parse_seg, meta={'seg_id': item['seg_id']})
                yield item

    def parse_seg(self, response):
        """解析章节的小说内容"""
        print("-" * 50, "进入章节内容", "-" * 50)
        item = SegDetailItem()
        item['seg_id'] = response.meta['seg_id']
        contents = "".join(response.css('.read-content p::text').extract())
        item['content'] = contents.replace('\u3000', '').replace('\n', '').strip()
        yield item
