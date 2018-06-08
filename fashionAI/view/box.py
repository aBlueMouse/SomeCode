import csv
import numpy as np

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


def _get_box(ann):
    kpt = np.zeros((24, 3))
    for i in range(2, len(ann)):
        str = ann[i]
        [x_str, y_str, vis_str] = str.split('_')
        kpt[i - 2, 0], kpt[i - 2, 1], kpt[i - 2, 2] = int(x_str), int(y_str), int(vis_str)
    inds = np.where(kpt[:, -1] == -1)
    kpt = np.delete(kpt, inds, axis = 0)
    left = min(kpt[:, 0])
    right = max(kpt[:, 0])
    top = min(kpt[:, 1])
    down = max(kpt[:, 1])
    if down == 512:
        print ann[0]
    return left, right, top, down

def main():
    info, anns = read_csv('train.csv')
    num_imgs = len(anns)
    min_x = []
    max_x = []
    min_y = []
    max_y = []
    for i in xrange(num_imgs):
        left, right, top, down = _get_box(anns[i])
        min_x.append(left)
        max_x.append(right)
        min_y.append(top)
        max_y.append(down)
    print 'min_x = ', min(min_x)
    print 'max_x = ', max(max_x)
    print 'min_y = ', min(min_y)
    print 'max_y = ', max(max_y)

if __name__ == '__main__':
    main()