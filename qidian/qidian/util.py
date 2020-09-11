#!/usr/bin/python3
# -*- encoding: utf-8 -*-
"""
@desc  : 
@author: Sarah
@file  : util.py
@time  : 2020/9/6 22:38
"""
from fontTools.ttLib import TTFont
import traceback


def font_test():
    # font_file = TTFont(r'C:\Users\18170\Downloads\qd_iconfont.f9a3f.woff')  # 加载字体文件
    font_file = TTFont(r'C:\Users\18170\Downloads\ccw.ttf')
    font_list = [' ', '9', '8', '3', '4', '7', '5']
    #           [                                    'TWO'                                         ]
    print(font_file.getGlyphOrder())  # 注释

    font_dict = dict(zip(font_file.getGlyphOrder()[:16], font_list))  # {注释：图形}
    real = {}
    for k, v in font_file['cmap'].getBestCmap().items():
        print(k, v)  # {编码： 注释}
        print(chr(k), v)

        real[chr(k)] = font_dict.get(v, '')
    # real = {chr(k): font_dict[v] for k, v in font_file['cmap'].getBestCmap().items()}
    print(real)
    t = '123'
    print(''.join(real.get(i, i) for i in t))


if __name__ == '__main__':
    font_test()
