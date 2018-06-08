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

def _get_keypoints(ann):
    kpt = np.zeros((24, 3))
    for i in range(2, len(ann)):
        str = ann[i]
        [x_str, y_str, vis_str] = str.split('_')
        kpt[i - 2, 0], kpt[i - 2, 1], kpt[i - 2, 2] = int(x_str), int(y_str), int(vis_str)
    return kpt

def main():
    result = './results/0501/submit_outwear.csv'
    info, anns = read_csv(result)
    for i in range(len(anns)):
        image = cv2.imread(anns[i][0])
        kpt = _get_keypoints(anns[i])
        for j in range(24):
            if kpt[j, 2] != -1 :
                cv2.circle(image, (int(kpt[j][0]), int(kpt[j][1])), 5, [0, 255, 0], thickness=-1)
        plt.imshow(image[:, :, [2, 1, 0]])
        plt.suptitle(anns[i][0].split('/')[2])
        plt.show()

if __name__ == '__main__':
    main()