import matplotlib.pyplot as plt
from multiprocessing import Pool
from PIL import Image 
import pandas as pd 
import glob
import imagehash


def check_hash():
    
    style_list = ['blouse', 'dress', 'outwear', 'skirt', 'trousers']
    pool = Pool()
    with open('check.csv', 'w') as f:
        for style in style_list: 

            train1 = glob.glob('train/Images/{}/*.jpg'.format(style))
            train2 = glob.glob('train2/Images/{}/*.jpg'.format(style))

            hash1 = pool.map(get_hash, train1)
            hash2 = pool.map(get_hash, train2)

            hash1 = dict(hash1)
            hash2 = dict(hash2)

            for im_hash, path in hash1.items():
                if im_hash in hash2:
                    f.write('{},{}\n'.format(path, hash2[im_hash]))





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
    view()