import os
import random

trainval_percent = 1
train_percent = 0.999
cur_dir = os.path.dirname(os.path.abspath(__file__))
xmlfilepath = cur_dir + '/datasets/Annotations/'
txtsavepath = cur_dir + '/datasets/ImageSets/Main/'
if not os.path.exists(txtsavepath):
    os.makedirs(txtsavepath)
total_xml = os.listdir(xmlfilepath)

num=len(total_xml)
list=range(num)
tv=int(num*trainval_percent)
tr=int(tv*train_percent)
trainval= random.sample(list,tv)
train=random.sample(trainval,tr)

ftrainval = open(txtsavepath + 'trainval.txt', 'w')
ftest = open(txtsavepath + 'test.txt', 'w')
ftrain = open(txtsavepath + 'train.txt', 'w')
fval = open(txtsavepath + 'val.txt', 'w')

for i in list:
    name=total_xml[i][:-4]+'\n'
    if i in trainval:
        ftrainval.write(name)
        if i in train:
            ftrain.write(name)
        else:
            fval.write(name)
    else:
        ftest.write(name)

ftrainval.close()
ftrain.close()
fval.close()
ftest .close()