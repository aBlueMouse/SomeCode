import numpy as np
import os
import csv
import cv2

class AllJoints(object):
    def __init__(self, img_dir, ann_path):
        self.kp_names = ['neckline_left','neckline_right','center_front','shoulder_left','shoulder_right',
                         'armpit_left','armpit_right','waistline_left','waistline_right','cuff_left_in',
                         'cuff_left_out','cuff_right_in','cuff_right_out','hemline_left','hemline_right']
        self.max_num_joints = 15
        self.color = np.random.randint(0, 256, (self.max_num_joints, 3))

        self.img_dir = img_dir
        self.anns = []
        self.info = []
        with open(ann_path, 'rb') as f:
            reader = csv.reader(f)
            for row in reader:
                self.anns.append(row)
        self.info.append(self.anns[0])
        self.anns = self.anns[1:]
		
        self.mpi = []
        self.test_mpi = []
        for ann in self.anns:
            imgname = ann[0]
            rect = np.array([0, 0, 1, 1], np.int32)
            joints = _get_keypoints(ann)
            imgname = self.img_dir + '/' + imgname
            keypointsData = dict(joints = joints, imgpath = imgname)
            self.mpi.append(keypointsData)

    def load_data(self, min_kps = 1):
        return self.mpi, self.test_mpi



def _get_keypoints(ann):
    kpt = np.zeros((15, 3))
    for i in range(2, len(ann)):
        str = ann[i]
        [x_str, y_str, vis_str] = str.split('_')
        kpt[i - 2, 0], kpt[i - 2, 1], kpt[i - 2, 2] = int(x_str), int(y_str), int(vis_str)
    kpt = kpt.reshape(-1).tolist()
    for i in range(2, len(kpt), 3):
        kpt[i] += 1
    return kpt