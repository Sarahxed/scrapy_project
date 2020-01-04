# -*- coding: utf-8 -*-
"""
@Time: 2019/12/22 21:56
@Auth: v_mzhulliu
@File: start.py
@IDE: PyCharm
@Motto: ABC(Always Be Coding)

"""
from scrapy import cmdline

# cmdline.execute(["scrapy", "crawl", "quotes"])


if __name__ == '__main__':
    import requests
    res = requests.get("http://www.baidu.com")
    print(res.status_code)