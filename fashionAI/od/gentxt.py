import os
import random

trainval_percent = 1
train_percent = 0.999
cloth = './blouse/'
xmlfilepath = cloth + 'Annotations'
txtsavepath = cloth + 'ImageSets/Main'
total_xml = os.listdir(xmlfilepath)

num=len(total_xml)
list=range(num)
tv=int(num*trainval_percent)
tr=int(tv*train_percent)
trainval= random.sample(list,tv)
train=random.sample(trainval,tr)

ftrainval = open(cloth + 'ImageSets/Main/trainval.txt', 'w')
ftest = open(cloth + 'ImageSets/Main/test.txt', 'w')
ftrain = open(cloth + 'ImageSets/Main/train.txt', 'w')
fval = open(cloth + 'ImageSets/Main/val.txt', 'w')

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