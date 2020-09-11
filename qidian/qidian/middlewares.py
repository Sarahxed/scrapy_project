# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

from qidian.cookies_ import get_cookie


# useful for handling different item types with a single interface


class QidianSpiderMiddleware:
    """监控爬虫类与引擎之间的交付数据（请求，request，相应，response，数据ITEM）以及异常情况"""

    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        """启动爬虫时用于创建爬虫中间键类的实例对象"""
        # This method is used by Scrapy to create your spiders.
        s = cls()  # cls是当前类对象
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)  # 接收信号
        return s

    def process_spider_input(self, response, spider):
        """流程第六步:引擎将请求响应的数据输入给spider的时候调用的"""
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        """流程中第七步：由spider类解析response数据之后产生结果输出给engin时，调用此方法"""
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        """解析数据出现异常时，用此方法"""
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        """流程中的第一步:爬虫发起第一个请求的时候,调用此方法，即从spider-》engin时"""
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class QidianDownloaderMiddleware:
    """下载中间件是引擎engin和下载中间件和下载器downloader之间的中间件，可以拦截请求和响应以及请求处理的异常"""

    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        """创建当前中间键类实例对象"""
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        """"""
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        # 设置代理
        # request.meta['proxy'] = "https://27.152.91.211:9999"
        # 设置cookie
        # request.cookies: dict
        request.cookies = get_cookie()
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
