import matplotlib.pyplot as plt
import csv
from skimage import draw
import numpy as np
import cv2

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

def main():
    result = './bbox/blouse_with_bbox.csv'
    info, anns = read_csv(result)
    expand = 1.2
    for i in range(1473, len(anns)):
        image = cv2.imread(anns[i][0])
        ori_height, ori_width, _ = image.shape
        left = int(anns[i][2])
        top = int(anns[i][3])
        right = int(anns[i][4])
        down = int(anns[i][5])
		
        center_x = (left + right)/2.0
        center_y = (top + down)/2.0
        bbox_w = right - left + 1
        bbox_h = down - top + 1
        left = center_x - (bbox_w * expand / 2)
        right = center_x + (bbox_w * expand / 2)
        top = center_y - (bbox_h * expand / 2)
        down = center_y + (bbox_h * expand / 2)
        left = max(0, int(left))
        right = min(ori_width - 1, int(right))
        top = max(0, int(top))
        down = min(ori_height - 1, int(down))
		
        cv2.rectangle(image, (left, top), (right, down), (255, 0, 0), 1)
        plt.imshow(image[:, :, [2, 1, 0]])
        plt.suptitle(anns[i][0].split('/')[2])
        plt.show()

if __name__ == '__main__':
    main()