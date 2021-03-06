import os
import numpy as np
import cv2
from config import cfg
import random
import time

def data_augmentation(trainData, trainLabel, trainValids, segms=None):
    trainSegms = segms
    tremNum = cfg.nr_aug - 1
    num1 = len(trainData)
    trainData = np.append(trainData, [trainData[0] for i in range(tremNum * len(trainData))], axis=0)
    if trainSegms is not None:
        gotSegm = trainSegms.copy()
        trainSegms = np.append(trainSegms, [trainSegms[0] for i in range(tremNum * len(trainSegms))], axis=0)
    trainLabel = np.append(trainLabel, [trainLabel[0] for i in range(tremNum * len(trainLabel))], axis=0)
    trainValids = np.append(trainValids, [trainValids[0] for i in range(tremNum * len(trainValids))], axis=0)
    counter = num1
    for lab in range(num1):
        ori_img = trainData[lab].transpose(1, 2, 0)
        if trainSegms is not None:
            ori_segm = gotSegm[lab].copy()
        annot = trainLabel[lab].copy()
        annot_valid = trainValids[lab].copy()
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

        trainData[lab] = img.transpose(2, 0, 1)
        if trainSegms is not None:
            trainSegms[lab] = segm
        trainLabel[lab] = annot
        trainValids[lab] = annot_valid

        # flip augmentation
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
            trainSegms[counter] = newsegm
        trainData[counter] = newimg.transpose(2, 0, 1)

        # **** the joint index depends on the dataset ****
        for (q, w) in cfg.symmetry:
            cod[q], cod[w] = cod[w], cod[q]
        for i in range(n):
            allc.append(cod[i][0])
            allc.append(cod[i][1])
        trainLabel[counter] = np.array(allc)
        allc_valid = annot_valid.copy()
        for (q, w) in cfg.symmetry:
            allc_valid[q], allc_valid[w] = allc_valid[w], allc_valid[q]
        trainValids[counter] = np.array(allc_valid)
        counter += 1

        # rotated augmentation
        for times in range(tremNum - 1):
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
            trainData[counter] = newimg
            if trainSegms is not None:
                trainSegms[counter] = newsegm
            trainLabel[counter] = np.array(allc)
            trainValids[counter] = np.array(allc_valid)
            counter += 1
    aug = random.randint(0, 3)
    if trainSegms is not None:
        return trainData[aug], trainLabel[aug], trainSegms[aug]
    else:
        return trainData[aug], trainLabel[aug], trainValids[aug]

def joints_heatmap_gen(data, label, tar_size=cfg.output_shape, ori_size=cfg.data_shape, points=cfg.nr_skeleton,
                       return_valid=False, gaussian_kernel=cfg.gaussain_kernel):
    if return_valid:
        valid = np.ones(points, dtype=np.float32)
    ret = np.zeros((points, tar_size[0], tar_size[1]), dtype='float32')
    for j in range(points):
        if label[j << 1] < 0 or label[j << 1 | 1] < 0:
            continue
        label[j << 1 | 1] = min(label[j << 1 | 1], ori_size[0] - 1)
        label[j << 1] = min(label[j << 1], ori_size[1] - 1)
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
    ori_height, ori_width, ori_channel = img.shape

    #hack(multiprocessing data provider)
    while img is None:
        print('read none image')
        time.sleep(np.random.rand() * 5)
        img = cv2.imread(os.path.join(d['imgpath']))
    '''add = max(img.shape[0], img.shape[1])
    bimg = cv2.copyMakeBorder(img, add, add, add, add, borderType=cv2.BORDER_CONSTANT,
                              value=cfg.pixel_means.reshape(-1))

    bbox = np.array(d['bbox']).reshape(4, ).astype(np.float32)
    bbox[:2] += add'''

    if 'joints' in d:
        joints = np.array(d['joints']).reshape(cfg.nr_skeleton, 3).astype(np.float32)
        #joints[:, :2] += add
        inds = np.where(joints[:, -1] == 0)
        joints[inds, :2] = -1000000

    '''crop_width = bbox[2] * (1 + cfg.imgExtXBorder * 2)
    crop_height = bbox[3] * (1 + cfg.imgExtYBorder * 2)
    objcenter = np.array([bbox[0] + bbox[2] / 2., bbox[1] + bbox[3] / 2.])

    if stage == 'train':
        crop_width = crop_width * (1 + 0.25)
        crop_height = crop_height * (1 + 0.25)

    if crop_height / height > crop_width / width:
        crop_size = crop_height
        min_shape = height
    else:
        crop_size = crop_width
        min_shape = width
    crop_size = min(crop_size, objcenter[0] / width * min_shape * 2. - 1.)
    crop_size = min(crop_size, (bimg.shape[1] - objcenter[0]) / width * min_shape * 2. - 1)
    crop_size = min(crop_size, objcenter[1] / height * min_shape * 2. - 1.)
    crop_size = min(crop_size, (bimg.shape[0] - objcenter[1]) / height * min_shape * 2. - 1)

    min_x = int(objcenter[0] - crop_size / 2. / min_shape * width)
    max_x = int(objcenter[0] + crop_size / 2. / min_shape * width)
    min_y = int(objcenter[1] - crop_size / 2. / min_shape * height)
    max_y = int(objcenter[1] + crop_size / 2. / min_shape * height)'''

    x_ratio = float(width) / ori_width
    y_ratio = float(height) / ori_height

    if 'joints' in d:
        #joints[:, 0] = joints[:, 0] - min_x
        #joints[:, 1] = joints[:, 1] - min_y

        joints[:, 0] *= x_ratio
        joints[:, 1] *= y_ratio
        label = joints[:, :2].copy()
        valid = joints[:, 2].copy()

    img = cv2.resize(img, (width, height))

    if stage != 'train':
        details = np.asarray([x_ratio, y_ratio])

    if cfg.use_seg is True and 'segmentation' in d:
        seg = get_seg(ori_img.shape[0], ori_img.shape[1], d['segmentation'])
        add = max(seg.shape[0], seg.shape[1])
        bimg = cv2.copyMakeBorder(seg, add, add, add, add, borderType=cv2.BORDER_CONSTANT, value=(0, 0, 0))
        seg = cv2.resize(bimg[min_y:max_y, min_x:max_x], (width, height))
        segms.append(seg)

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
