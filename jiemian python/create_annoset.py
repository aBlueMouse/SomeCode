# -*- coding: UTF-8 -*-
from __future__ import unicode_literals, print_function
import argparse
import os
import shutil
import subprocess
import sys
import random
import time
import commands
import  xml.dom.minidom
import chardet

from caffe.proto import caffe_pb2
from google.protobuf import text_format

def createFileList(root_dir):
    #打开图片列表清单txt文件
    txt_save_path = root_dir + 'train.txt'
    fw = open(txt_save_path,"w")
    #查看图片目录下的文件,相当于shell指令ls
    images_path = root_dir + 'img/'
    images_name = os.listdir(images_path)
    #遍历所有文件名
    list = []
    for eachname in images_name:
        #按照规则将内容写入txt文件中
        #fw.write(images_path + eachname + ' ' + labels_path + eachname[:-4] + '.xml\n')
        list.append('img/' + eachname + ' ' + 'label/' + eachname[:-4] + '.xml\n')
    #打乱顺序
    random.shuffle(list)
    for l in list:
        fw.write(l)
    #打印成功信息
    print("生成txt文件成功".encode("utf-8"))
    sys.stdout.flush()
    #关闭fw
    fw.close()


time_start = time.time();

# time.sleep(10)

received = raw_input()
file_temp = open("result2.xml", "w+")
file_temp.write(received)
file_temp.close()

dom = xml.dom.minidom.parse('result2.xml')
root = dom.documentElement

root_dir_1 = dom.getElementsByTagName('Test_Dir')
root_dir_2 = root_dir_1[0]
root_dir = root_dir_2.firstChild.data

labelmap_file_1 = dom.getElementsByTagName('LabelMap_File')
labelmap_file_2 = labelmap_file_1[0]
labelmap_file = labelmap_file_2.firstChild.data

root_dir = root_dir.encode('unicode-escape').decode('string_escape')
labelmap_file = labelmap_file.encode('unicode-escape').decode('string_escape')

# file_temp = open("test.txt", "w+")
# file_temp.write(root_dir)
# file_temp.close()

#root_dir = "E:\\4C\\0622"
if root_dir[-1] != "/":
    root_dir += "/"

list_file = root_dir + 'train.txt'
out_dir = root_dir + "train_lmdb"
#  example_dir = args.exampledir

createFileList(root_dir)

    #redo = args.redo
anno_type = "detection"
# label_map_file = "E:\\4C\\4c_windows\\labelmap_voc.prototxt"
min_dim = 0
max_dim = 0
resize_height = 0
resize_width = 0
shuffle = False
#check_label = "--encode-type=jpg --encoded --redo"
check_label = True
label_type = "xml"
backend = "lmdb"
check_size = False
encode_type = "jpg"
encoded = True
gray = False

# check list file format is correct
with open(list_file, "r") as lf:
    for line in lf.readlines():
        img_file, anno = line.strip("\n").split(" ")
        #print root_dir + img_file
        if not os.path.exists(root_dir + img_file):
            print("image file: {} does not exist".format(root_dir + img_file).encode("utf-8"))
            sys.stdout.flush()
        if anno_type == "classification":
            if not anno.isdigit():
                print("annotation: {} is not an integer".format(anno).encode("utf-8"))
                sys.stdout.flush()
        elif anno_type == "detection":
            if not os.path.exists(root_dir + anno):
                print("annofation file: {} does not exist".format(root_dir + anno).encode("utf-8"))
                sys.stdout.flush()
                sys.exit()
        break
# check if label map file exist

if anno_type == "detection":
    label_map = caffe_pb2.LabelMap()
    lmf = open(labelmap_file, "r")
    try:
        text_format.Merge(str(lmf.read()), label_map)
    except:
        print("Cannot parse label map file: {}".format(labelmap_file).encode("utf-8"))
        sys.stdout.flush()
        sys.exit()
out_parent_dir = os.path.dirname(out_dir)

if not os.path.exists(out_parent_dir):
    os.makedirs(out_parent_dir)
if os.path.exists(out_dir):
    shutil.rmtree(out_dir)

# get caffe root directory
caffe_root = "E:\\4C\\caffe-windows"
if anno_type == "detection":
    cmd = "{}\\Build\\x64\\Release\\convert_annoset" \
        " --anno_type={}" \
        " --label_type={}" \
        " --label_map_file={}" \
        " --check_label={}" \
        " --min_dim={}" \
        " --max_dim={}" \
        " --resize_height={}" \
        " --resize_width={}" \
        " --backend={}" \
        " --shuffle={}" \
        " --check_size={}" \
        " --encode_type={}" \
        " --encoded={}" \
        " --gray={}" \
        " {} {} {}" \
        .format(caffe_root, anno_type, label_type, labelmap_file, check_label,
            min_dim, max_dim, resize_height, resize_width, backend, shuffle,
            check_size, encode_type, encoded, gray, root_dir, list_file, out_dir)
elif anno_type == "classification":
    cmd = "{}\\Build\\x64\\Release\\convert_annoset" \
        " --anno_type={}" \
        " --min_dim={}" \
        " --max_dim={}" \
        " --resize_height={}" \
        " --resize_width={}" \
        " --backend={}" \
        " --shuffle={}" \
        " --check_size={}" \
        " --encode_type={}" \
        " --encoded={}" \
        " --gray={}" \
        " {} {} {}" \
        .format(caffe_root, anno_type, min_dim, max_dim, resize_height,
            resize_width, backend, shuffle, check_size, encode_type, encoded,
            gray, root_dir, list_file, out_dir)
print(cmd.encode("utf-8"))
sys.stdout.flush()
process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
output = process.communicate()[0]
# process = subprocess.Popen(cmd.split())
# process.wait()
# process.wait()
# if process.returncode != 0:
#     print "Error."
#print output
# status, output = commands.getstatusoutput(cmd)
# print output
# if (status == 0):
#     print "lmbd文件生成成功"
# os.system(cmd)
time_end = time.time()
print((str(time_end - time_start) + 's').encode("utf-8"))
sys.stdout.flush()

"""
  if not os.path.exists(example_dir):
    os.makedirs(example_dir)
  link_dir = os.path.join(example_dir, os.path.basename(out_dir))
  if os.path.exists(link_dir):
    os.unlink(link_dir)
  os.symlink(out_dir, link_dir)
"""