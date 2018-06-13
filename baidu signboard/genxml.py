#coding:utf8
import csv
import cv2
import numpy as np
from lxml import etree, objectify
import os

def read_txt(ann_file):
    anns = []
    with open(ann_file, 'rb') as f:
        line = f.readline()
        while line:
            line = line.split('\n')[0]
            line = line.split(' ')
            anns.append(line)
            line = f.readline()
    return anns

def toXml(filename, width, height, depth, name, left, top, right, down):
    E = objectify.ElementMaker(annotate=False)
    anno_tree = E.annotation(
        E.folder('VOC2007'),
        E.filename(filename),
        E.size(
            E.width(str(width)),
            E.height(str(height)),
            E.depth(str(depth))
        ),
        E.segmented('0'),
        E.object(
            E.name(str(name)),
            E.pose('Unspecified'),
            E.truncated('0'),
            E.difficult('0'),
            E.bndbox(
                E.xmin(str(left)),
                E.ymin(str(top)),
                E.xmax(str(right)),
                E.ymax(str(down))
            )
        )
    )
    return anno_tree

def editXml(xml_path, name, left, top, right, down):
    anno_tree = objectify.parse(xml_path).getroot()
    E = objectify.ElementMaker(annotate=False)
    anno_tree_son = E.object(
        E.name(str(name)),
        E.pose('Unspecified'),
        E.truncated('0'),
        E.difficult('0'),
        E.bndbox(
            E.xmin(str(left)),
            E.ymin(str(top)),
            E.xmax(str(right)),
            E.ymax(str(down))
        )
    )
    anno_tree.append(anno_tree_son)
    return anno_tree

def main():
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    result = cur_dir + '/datasets/train.txt'
    anns = read_txt(result)
    save_path = cur_dir + '/datasets/Annotations/'
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    for i in range(len(anns)):
        image = cv2.imread(cur_dir+ '/datasets/train/' + anns[i][0])
        height, width, depth = image.shape[0], image.shape[1], image.shape[2]
        filename = anns[i][0]
        name = str(anns[i][1])
        left = int(anns[i][2])
        top = int(anns[i][3])
        right = int(anns[i][4])
        down = int(anns[i][5])

        xml_path = save_path + filename.split('.')[0] + '.xml'

        if i == 0:
            anno_tree = toXml(filename, width, height, depth, name, left, top, right, down)
        else:
            if anns[i][0] == anns[i-1][0]:
                anno_tree = editXml(xml_path, name, left, top, right, down)
            else:
                anno_tree = toXml(filename, width, height, depth, name, left, top, right, down)
        etree.ElementTree(anno_tree).write(xml_path, pretty_print=True)

        print '%s/%s' % (str(i+1), str(len(anns)))

if __name__ == '__main__':
    main()