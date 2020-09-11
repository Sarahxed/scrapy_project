#!/usr/bin/python3
# -*- encoding: utf-8 -*-
"""
@desc  : 
@author: Sarah
@file  : cookies_.py
@time  : 2020/9/9 21:26
"""
import random

cookie_text = [
    '_csrfToken=hNMcW0RIWseGy9DoWzJJuNdXAGhT4AWzitTp6K4R; qdrs=0%7C3%7C0%7C0%7C1; showSectionCommentGuide=1; qdgd=1; e1=%7B%22pid%22%3A%22qd_P_fin%22%2C%22eid%22%3A%22qd_B58%22%2C%22l1%22%3A5%7D; newstatisticUUID=1599487087_232362426; lrbc=107580%7C21213503%7C0%2C1013562540%7C447207327%7C0%2C1010177519%7C390638038%7C0; rcr=107580%2C1013562540%2C1012237441%2C2226569%2C1010868264%2C1010177519; _yep_uuid=6f2d636b-c42f-4e7e-7d36-4620d4179488; e2=%7B%22pid%22%3A%22qd_P_fin%22%2C%22eid%22%3A%22qd_B58%22%2C%22l1%22%3A5%7D'
]


def get_cookie():
    cookie = random.choice(cookie_text)
    return {
        c.split('=')[0]: c.split('=')[1]
        for c in cookie.split('; ')
    }

