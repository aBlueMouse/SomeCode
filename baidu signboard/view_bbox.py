import matplotlib.pyplot as plt
import csv
import numpy as np
import cv2
import os

def read_txt(ann_file):
    anns = []
    with open(ann_file, 'rb') as f:
        line = f.readline()
        while line:
            line = line.split(' ')
            anns.append(line)
            line = f.readline()
    return anns

def main():
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    result = cur_dir + '/datasets/train.txt'
    anns = read_txt(result)
    for i in range(len(anns)):
        image = cv2.imread(cur_dir+ '/datasets/train/' + anns[i][0])
        left = int(anns[i][2])
        top = int(anns[i][3])
        right = int(anns[i][4])
        down = int(anns[i][5])

        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.rectangle(image, (left, top), (right, down), (255, 0, 0), 6)
        # cv2.rectangle(image, (left, top), (left+100, top+50), (255, 0, 0), -1)
        cv2.putText(image, 'class:' + str(anns[i][1]), (left-6, top-6), font, 1.2, (0, 255, 0), 3)

        plt.imshow(image[:, :, [2, 1, 0]])
        plt.suptitle(anns[i][0])
        plt.show()

if __name__ == '__main__':
    main()