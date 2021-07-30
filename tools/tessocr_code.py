# encoding: utf-8
"""
@author: Sarah
@time: 2021/4/29 16:15
@file: tessocr_code.py
@desc: 
"""
import re
from collections import defaultdict, Counter

import PIL
import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r'D:\\Tesseract-OCR\\tesseract.exe '


class TessOcr:
    def get_threshold_detail(self, image: PIL.Image.Image):
        """
        获取图片背景颜色，同时识别验证码干扰线并清除
        :param image: 图片对象
        :return:
        """
        pixel_dict = defaultdict(lambda: {'count': 0, 'x': [], 'y': []})
        rows, cols = image.size  # 80, 22
        for i in range(rows):
            for j in range(cols):
                pixel = image.getpixel((i, j))  # 获取点（x, y）的像素RGB值
                pixel_dict[pixel]['count'] += 1
                pixel_dict[pixel]['x'].append(i)
                pixel_dict[pixel]['y'].append(j)
        back_color = self.get_back(pixel_dict)
        line_list = self.get_line_point(pixel_dict, back_color)
        for point in line_list:
            image.putpixel(point, back_color)
        return back_color

    def get_back(self, pixel_dict: dict):
        """获取图片的背景色"""
        count_max = max([i.get('count') for i in pixel_dict.values()])
        pixel_dict_reverse = {v.get('count'): k for k, v in pixel_dict.items()}
        back_color = pixel_dict_reverse[count_max]
        return back_color

    def get_line_point(self, pixel_dict, back_color):
        """
        获取干扰线的坐标点
        干扰线的特征：X坐标分布广，几乎不重复
        原理：获取所有颜色的点坐标，除背景颜色外，x坐标大于20个且重复最少的两个颜色，为干扰线颜色，返回干扰线不重复的x坐标的点
        缺点：当数字或字母与干扰线的颜色相同时，不能很好地清除干扰线，会在相同颜色的字体处保留干扰线
        :param pixel_dict:
        :return:
        """
        new_dict = defaultdict(list)
        need_list = []
        for k, v in pixel_dict.items():
            x_ = v.get('x')  # 获取每种颜色像素点的所有X坐标
            # 如果该颜色像素点的x坐标去重后大于20个，且重复最少，则为干扰线
            if len(set(x_)) > 20 and k != back_color:
                y_ = v.get('y')
                # 这里可能存在干扰线和验证字符同一种颜色的情况，那么需要额外加一层判断：
                # 如果该像素点X坐标的值只出现一次才视为干扰线(因为干扰线的xy坐标值线性的很少重复)
                point_data = [(x_[i], y_[i]) for i in range(len(x_)) if x_.count(x_[i]) == 1]
                new_dict[len(x_) - len(set(x_))].append({'color': k, 'data': point_data})
        while len(need_list) < 2 and new_dict.items():
            min_ = min(new_dict.keys())
            need_list += new_dict[min_]
            new_dict.pop(min_)
        line_point_list = []
        for each in need_list:
            line_point_list += each.get('data')
        return line_point_list

    def get_bin_table(self, threshold, rate=0.27):
        return [1 if threshold * (1 - rate) <= i <= threshold * (1 + rate) else 0 for i in range(256)]

    def top_counter(self, need_list, index=2):
        return [i[0] for i in Counter(need_list).most_common(index)]

    def image2string(self, image_path):
        """
        从图片中识别出验证码，同时使用2种识别模型
        :param image_path: 验证码图片路径
        :return: 【enm识别结果，eng识别结果】
        """
        image = Image.open(image_path)
        image = image.convert('RGB')
        print(type(image), image)
        max_pixel = self.get_threshold_detail(image)  # 获取背景颜色
        image = image.convert('L')  # 二值化，黑白
        table = self.get_bin_table(max_pixel[0])
        out = image.point(table, '1')
        result_enm = pytesseract.image_to_string(out, lang='enm')  # 识别
        result_eng = pytesseract.image_to_string(out, lang='eng')
        return [result_enm, result_eng]

    def do_tess(self, result_list):
        """
        清洗模型识别的结果，按照策略输出候选结果：出现次数最多的前3，和每个位置出现最多的前2的组合
        :param result_list: 模型识别的结果列表
        :return: 候选结果列表
        """
        pass_dict = defaultdict(list)
        for each in result_list:
            each = re.sub('\s|\W', '', each)
            if len(each) == 4:
                pass_dict['all'].append(each)
                pass_dict['1'].append(each[0])
                pass_dict['2'].append(each[1])
                pass_dict['3'].append(each[2])
                pass_dict['4'].append(each[3])
        all_list = pass_dict.get('all')
        top_all = self.top_counter(all_list, index=3)
        tess_list = list(top_all)
        for i in self.top_counter(pass_dict.get('1')):
            for j in self.top_counter(pass_dict.get('2')):
                for k in self.top_counter(pass_dict.get('3')):
                    for z in self.top_counter(pass_dict.get('4')):
                        now_ = ''.join([i, j, k, z])
                        if now_ not in tess_list:
                            tess_list.append(now_)
        return tess_list

    def do(self, image_path):
        result_list = self.image2string(image_path)
        tess_list = self.do_tess(result_list)
        return tess_list


if __name__ == '__main__':
    image_path = r"xxxxx"
    tess = TessOcr()
    tess.do(image_path)
