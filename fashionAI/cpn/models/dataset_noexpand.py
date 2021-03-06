import os
import numpy as np
import cv2
from config import cfg
import random
import time

def data_augmentation(trainData, trainLabel, trainValids, segms=None):
    trainSegms = segms
    tremNum = cfg.nr_aug - 1
    aug = random.randint(0, 5)
    trainData = np.array(trainData)[0]
    if trainSegms is not None:
        trainSegms = np.array(trainSegms)[0]
    trainLabel = np.array(trainLabel)[0]
    trainValids = np.array(trainValids)[0]
    if aug <= 1:
        ori_img = trainData.transpose(1, 2, 0)
        if trainSegms is not None:
            ori_segm = trainSegms.copy()
        annot = trainLabel.copy()
        annot_valid = trainValids.copy()
        height, width = ori_img.shape[0], ori_img.shape[1]
        center = (width / 2., height / 2.)
        n = cfg.nr_skeleton

        # affrat = random.uniform(0.75, 1.25)
        affrat = random.uniform(0.7, 1.35)
        halfl_w = min(width - center[0], (width - center[0]) / 1.25 * affrat)
        halfl_h = min(height - center[1], (height - center[1]) / 1.25 * affrat)
        # img = cv2.resize(ori_img[int(center[0] - halfl_w) : int(center[0] + halfl_w + 1), int(center[1] - halfl_h) : int(center[1] + halfl_h + 1)], (width, height))
        img = cv2.resize(ori_img[int(center[1] - halfl_h): int(center[1] + halfl_h + 1),
                         int(center[0] - halfl_w): int(center[0] + halfl_w + 1)], (width, height))
        if trainSegms is not None:
            segm = cv2.resize(ori_segm[int(center[1] - halfl_h): int(center[1] + halfl_h + 1),
                              int(center[0] - halfl_w): int(center[0] + halfl_w + 1)], (width, height))
        for i in range(n):
            annot[i << 1] = (annot[i << 1] - center[0]) / halfl_w * (width - center[0]) + center[0]
            annot[i << 1 | 1] = (annot[i << 1 | 1] - center[1]) / halfl_h * (height - center[1]) + center[1]
            annot_valid[i] *= (
            (annot[i << 1] >= 0) & (annot[i << 1] < width) & (annot[i << 1 | 1] >= 0) & (annot[i << 1 | 1] < height))

        trainData = img.transpose(2, 0, 1)
        if trainSegms is not None:
            trainSegms = segm
        trainLabel = annot
        trainValids = annot_valid

    # flip augmentation
    elif aug >= 2 and aug <= 3:
        ori_img = trainData.transpose(1, 2, 0)
        if trainSegms is not None:
            ori_segm = trainSegms.copy()
        annot = trainLabel.copy()
        annot_valid = trainValids.copy()
        height, width = ori_img.shape[0], ori_img.shape[1]
        center = (width / 2., height / 2.)
        n = cfg.nr_skeleton

        # affrat = random.uniform(0.75, 1.25)
        affrat = random.uniform(0.7, 1.35)
        halfl_w = min(width - center[0], (width - center[0]) / 1.25 * affrat)
        halfl_h = min(height - center[1], (height - center[1]) / 1.25 * affrat)
        # img = cv2.resize(ori_img[int(center[0] - halfl_w) : int(center[0] + halfl_w + 1), int(center[1] - halfl_h) : int(center[1] + halfl_h + 1)], (width, height))
        img = cv2.resize(ori_img[int(center[1] - halfl_h): int(center[1] + halfl_h + 1),
                         int(center[0] - halfl_w): int(center[0] + halfl_w + 1)], (width, height))
        if trainSegms is not None:
            segm = cv2.resize(ori_segm[int(center[1] - halfl_h): int(center[1] + halfl_h + 1),
                              int(center[0] - halfl_w): int(center[0] + halfl_w + 1)], (width, height))
        for i in range(n):
            annot[i << 1] = (annot[i << 1] - center[0]) / halfl_w * (width - center[0]) + center[0]
            annot[i << 1 | 1] = (annot[i << 1 | 1] - center[1]) / halfl_h * (height - center[1]) + center[1]
            annot_valid[i] *= (
                    (annot[i << 1] >= 0) & (annot[i << 1] < width) & (annot[i << 1 | 1] >= 0) & (
                        annot[i << 1 | 1] < height))

        newimg = cv2.flip(img, 1)
        if trainSegms is not None:
            newsegm = cv2.flip(segm, 1)
        cod = []
        allc = []
        for i in range(n):
            x, y = annot[i << 1], annot[i << 1 | 1]
            if x >= 0:
                x = width - 1 - x
            cod.append((x, y))
        if trainSegms is not None:
            trainSegms = newsegm
        trainData = newimg.transpose(2, 0, 1)

        # **** the joint index depends on the dataset ****
        for (q, w) in cfg.symmetry:
            cod[q], cod[w] = cod[w], cod[q]
        for i in range(n):
            allc.append(cod[i][0])
            allc.append(cod[i][1])
        trainLabel = np.array(allc)
        allc_valid = annot_valid.copy()
        for (q, w) in cfg.symmetry:
            allc_valid[q], allc_valid[w] = allc_valid[w], allc_valid[q]
        trainValids = np.array(allc_valid)


    # rotated augmentation
    elif aug >= 4:
        ori_img = trainData.transpose(1, 2, 0)
        if trainSegms is not None:
            ori_segm = trainSegms.copy()
        annot = trainLabel.copy()
        annot_valid = trainValids.copy()
        height, width = ori_img.shape[0], ori_img.shape[1]
        center = (width / 2., height / 2.)
        n = cfg.nr_skeleton

        # affrat = random.uniform(0.75, 1.25)
        affrat = random.uniform(0.7, 1.35)
        halfl_w = min(width - center[0], (width - center[0]) / 1.25 * affrat)
        halfl_h = min(height - center[1], (height - center[1]) / 1.25 * affrat)
        # img = cv2.resize(ori_img[int(center[0] - halfl_w) : int(center[0] + halfl_w + 1), int(center[1] - halfl_h) : int(center[1] + halfl_h + 1)], (width, height))
        img = cv2.resize(ori_img[int(center[1] - halfl_h): int(center[1] + halfl_h + 1),
                         int(center[0] - halfl_w): int(center[0] + halfl_w + 1)], (width, height))
        if trainSegms is not None:
            segm = cv2.resize(ori_segm[int(center[1] - halfl_h): int(center[1] + halfl_h + 1),
                              int(center[0] - halfl_w): int(center[0] + halfl_w + 1)], (width, height))
        for i in range(n):
            annot[i << 1] = (annot[i << 1] - center[0]) / halfl_w * (width - center[0]) + center[0]
            annot[i << 1 | 1] = (annot[i << 1 | 1] - center[1]) / halfl_h * (height - center[1]) + center[1]
            annot_valid[i] *= (
                    (annot[i << 1] >= 0) & (annot[i << 1] < width) & (annot[i << 1 | 1] >= 0) & (
                    annot[i << 1 | 1] < height))

        angle = random.uniform(0, 45)
        if random.randint(0, 1):
            angle *= -1
        rotMat = cv2.getRotationMatrix2D(center, angle, 1.0)
        newimg = cv2.warpAffine(img, rotMat, (width, height))
        if trainSegms is not None:
            newsegm = cv2.warpAffine(segm, rotMat, (width, height))
        allc = []
        allc_valid = []
        for i in range(n):
            x, y = annot[i << 1], annot[i << 1 | 1]
            coor = np.array([x, y])
            if x >= 0 and y >= 0:
                R = rotMat[:, : 2]
                W = np.array([rotMat[0][2], rotMat[1][2]])
                coor = np.dot(R, coor) + W
            allc.append(coor[0])
            allc.append(coor[1])
            allc_valid.append(
                annot_valid[i] * ((coor[0] >= 0) & (coor[0] < width) & (coor[1] >= 0) & (coor[1] < height)))
        newimg = newimg.transpose(2, 0, 1)
        trainData = newimg
        if trainSegms is not None:
            trainSegms = newsegm
        trainLabel = np.array(allc)
        trainValids = np.array(allc_valid)
    if trainSegms is not None:
        return trainData, trainLabel, trainSegms
    else:
        return trainData, trainLabel, trainValids

def joints_heatmap_gen(data, label, tar_size=cfg.output_shape, ori_size=cfg.data_shape, points=cfg.nr_skeleton,
                       return_valid=False, gaussian_kernel=cfg.gaussain_kernel):
    if return_valid:
        valid = np.ones(points, dtype=np.float32)
    ret = np.zeros((points, tar_size[0], tar_size[1]), dtype='float32')
    for j in range(points):
        if label[j << 1] < 0 or label[j << 1 | 1] < 0 or label[j << 1] > (ori_size[1] - 1) or label[j << 1 | 1] > (ori_size[0] - 1):
            continue
        #label[j << 1 | 1] = min(label[j << 1 | 1], ori_size[0] - 1)
        #label[j << 1] = min(label[j << 1], ori_size[1] - 1)
        ret[j][int(label[j << 1 | 1] * tar_size[0] / ori_size[0])][
        int(label[j << 1] * tar_size[1] / ori_size[1])] = 1
    for j in range(points):
        ret[j] = cv2.GaussianBlur(ret[j], gaussian_kernel, 0)
    for j in range(cfg.nr_skeleton):
        am = np.amax(ret[j])
        if am <= 1e-8:
            if return_valid:
                valid[j] = 0.
            continue
        ret[j] /= am / 255
    if return_valid:
        return ret, valid
    else:
        return ret

def Preprocessing(d, stage='train'):
    height, width = cfg.data_shape
    imgs = []
    labels = []
    valids = []

    vis = False
    img = cv2.imread(os.path.join(d['imgpath']))
    # ori_height, ori_width, ori_channel = img.shape

    while img is None:
        print('read none image')
        time.sleep(np.random.rand() * 5)
        img = cv2.imread(os.path.join(d['imgpath']))

    bbox = np.array(d['bbox']).reshape(4, ).astype(np.float32)

    if 'joints' in d:
        joints = np.array(d['joints']).reshape(cfg.nr_skeleton, 3).astype(np.float32)
        inds = np.where(joints[:, -1] == 0)
        joints[inds, :2] = -1000000

    min_x = int(bbox[0])
    max_x = int(bbox[2])
    min_y = int(bbox[1])
    max_y = int(bbox[3])

    x_ratio = float(width) / (max_x - min_x + 1)
    y_ratio = float(height) / (max_y - min_y + 1)

    if 'joints' in d:
        joints[:, 0] = joints[:, 0] - min_x
        joints[:, 1] = joints[:, 1] - min_y

        joints[:, 0] *= x_ratio
        joints[:, 1] *= y_ratio
        label = joints[:, :2].copy()
        valid = joints[:, 2].copy()

    img = cv2.resize(img[min_y:max_y+1, min_x:max_x+1, :], (width, height))

    if stage != 'train':
        details = np.asarray([x_ratio, y_ratio, min_x, min_y])

    if vis:
        img2 = img.copy()
        from visualization import draw_skeleton
        draw_skeleton(img, label.astype(int))
        cv2.imshow('1', ori_img)
        cv2.imshow('2', img2)
        cv2.imshow('', img)
        cv2.waitKey()
        # from vis_detection import visualize
        # visualize(ori_img, np.array(d['bbox']).reshape(4,))
        # visualize(img, keypoints=joints)

    #img = img - cfg.pixel_means
    if cfg.pixel_norm:
        img = img / 255.
    img = img.transpose(2, 0, 1)
    imgs.append(img)
    if 'joints' in d:
        labels.append(label.reshape(-1))
        valids.append(valid.reshape(-1))

    if stage == 'train':
        imgs, labels, valids = data_augmentation(imgs, labels, valids)
        heatmaps15 = joints_heatmap_gen(imgs, labels, cfg.output_shape, cfg.data_shape, return_valid=False,
                                        gaussian_kernel=cfg.gk15)
        heatmaps11 = joints_heatmap_gen(imgs, labels, cfg.output_shape, cfg.data_shape, return_valid=False,
                                        gaussian_kernel=cfg.gk11)
        heatmaps9 = joints_heatmap_gen(imgs, labels, cfg.output_shape, cfg.data_shape, return_valid=False,
                                       gaussian_kernel=cfg.gk9)
        heatmaps7 = joints_heatmap_gen(imgs, labels, cfg.output_shape, cfg.data_shape, return_valid=False,
                                       gaussian_kernel=cfg.gk7)

        return [imgs.astype(np.float32).transpose(1, 2, 0),
                heatmaps15.astype(np.float32).transpose(1, 2, 0),
                heatmaps11.astype(np.float32).transpose(1, 2, 0),
                heatmaps9.astype(np.float32).transpose(1, 2, 0),
                heatmaps7.astype(np.float32).transpose(1, 2, 0),
                valids.astype(np.float32)]
    else:
        return [np.asarray(imgs).astype(np.float32), details]
