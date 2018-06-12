#coding:utf8
import matplotlib.pyplot as plt
from multiprocessing import Pool
from PIL import Image 
import pandas as pd 
import glob
import imagehash


def cmpHash(hash1,hash2):
    n=0
    #hash长度不同则返回-1代表传参出错
    if len(hash1)!=len(hash2):
        return -1
    #遍历判断
    for i in range(len(hash1)):
        #不相等则n计数+1，n最终为相似度
        if hash1[i]!=hash2[i]:
            n=n+1
    return n

def check_hash():
    pool = Pool()
    sim = 1000
    sim_path = ''
    with open('check.csv', 'w') as f:
        train = glob.glob('datasets/train/*.jpg')
        hash = pool.map(get_hash, train)
        hash = dict(hash)
        hash_test = get_hash('test.jpg')
        print hash_test[0]
        print type(hash_test[0])
        for im_hash, path in hash.items():
            cha = cmpHash(str(im_hash), str(hash_test[0]))
            if cha < sim:
                sim = cha
                sim_path = path
        print sim
        print sim_path
        f.write('{},{}\n'.format(sim_path, hash_test[1]))

def get_hash(path):
    im_hash = imagehash.average_hash(Image.open(path))
    return (im_hash, path)


def view():
    text = pd.read_csv('check.csv', header=-1)
    for path1, path2 in text.values:
        plt.figure()
        im1 = plt.imread(path1)
        im2 = plt.imread(path2)
        plt.subplot(1,2,1)
        plt.imshow(im1)
        plt.subplot(1,2,2)
        plt.imshow(im2)
        plt.show()
        # break



if __name__ == '__main__':
    check_hash()
    #view()