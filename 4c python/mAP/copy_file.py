# -*- coding: UTF-8 -*-
import os
import shutil

f_img = open('test_jpg.txt', 'r')
img_path = '/home/sxl/caffe-ssd/data/dianwang/gailujing/img/'

for line in f_img.readlines():
    shutil.copy(line[:-1], img_path)
f_img.close()

f_xml = open('test_xml.txt', 'r')
xml_path = '/home/sxl/caffe-ssd/data/dianwang/gailujing/label/'

for line in f_xml.readlines():
    shutil.copy(line[:-1], xml_path)
f_xml.close()
