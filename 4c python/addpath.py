import numpy as np

f = open('1.txt','r')
f1 = open('train.txt','a+')

for j in range(1914):
    line = f.readline()
    f1.write('/home/sxl/caffe-ssd/data/dianwang/ImagesImages/' + line[0:])
f.close()
f1.close()
