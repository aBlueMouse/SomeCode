#coding:utf8
import csv
import cv2
import numpy as np
from lxml.etree import Element, SubElement, tostring

def read_csv(ann_file):
    info = []
    anns = []
    with open(ann_file, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            anns.append(row)
    info = anns[0]
    anns = anns[1:]
    return info, anns

def _get_keypoints(ann):
    kpt = np.zeros((len(ann) - 2, 3))
    for i in range(2, len(ann)):
        str = ann[i]
        [x_str, y_str, vis_str] = str.split('_')
        kpt[i - 2, 0], kpt[i - 2, 1], kpt[i - 2, 2] = int(x_str), int(y_str), int(vis_str)
    return kpt

def toXml(filename, width, height, depth, left, top, right, down):
    node_root = Element('annotation')

    node_folder = SubElement(node_root, 'folder')
    node_folder.text = 'VOC2007'

    node_filename = SubElement(node_root, 'filename')
    node_filename.text = filename

    node_size = SubElement(node_root, 'size')
    node_width = SubElement(node_size, 'width')
    node_width.text = str(width)

    node_height = SubElement(node_size, 'height')
    node_height.text = str(height)

    node_depth = SubElement(node_size, 'depth')
    node_depth.text = str(depth)

    node_object = SubElement(node_root, 'object')
    node_name = SubElement(node_object, 'name')
    node_name.text = 'blouse'
    node_pose = SubElement(node_object, 'pose')
    node_pose.text = 'Unspecified'
    node_truncated = SubElement(node_object, 'truncated')
    node_truncated.text = '0'
    node_difficult = SubElement(node_object, 'difficult')
    node_difficult.text = '0'
    node_bndbox = SubElement(node_object, 'bndbox')
    node_xmin = SubElement(node_bndbox, 'xmin')
    node_xmin.text = str(left)
    node_ymin = SubElement(node_bndbox, 'ymin')
    node_ymin.text = str(top)
    node_xmax = SubElement(node_bndbox, 'xmax')
    node_xmax.text = str(right)
    node_ymax = SubElement(node_bndbox, 'ymax')
    node_ymax.text = str(down)

    xml = tostring(node_root, pretty_print=True)
    return xml

def main():
    cloth = 'blouse'
    img_path = 'C:\\Users\\lanhao\\Desktop\\fashion\\key_point\\[update] warm_up_train_20180222\\train/'
    result = './%s/train_%s.csv' %(cloth, cloth)
    info, anns = read_csv(result)
    for i in range(len(anns)):
        image = cv2.imread(img_path + anns[i][0])
        height, width, depth = image.shape[0], image.shape[1], image.shape[2]
        kpt = _get_keypoints(anns[i])

        inds = np.where(kpt[:, 2] == -1)
        kpt_n = np.delete(kpt, inds, axis=0)
        left = min(kpt_n[:, 0])
        top = min(kpt_n[:, 1])
        right = max(kpt_n[:, 0])
        down = max(kpt_n[:, 1])

        bounding = 20
        left = int(max(left - bounding, 0))
        top = int(max(top - bounding, 0))
        right = int(min(right + bounding, width - 1))
        down = int(min(down + bounding, height - 1))

        filename = anns[i][0].split('/')[2]

        xml = toXml(filename, width, height, depth, left, top, right, down)

        #with open('test.xml', 'w', encoding="UTF-8") as f:
        save_path = './%s/Annotations/' % (cloth)
        with open(save_path + filename.split('.')[0] + '.xml', 'w') as f:
            f.write(xml)

        print '%s/%s' % (str(i+1), str(len(anns)))

if __name__ == '__main__':
    main()