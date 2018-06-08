import os

fileDir = "/home/sxl/caffe-ssd/data/VOCdevkit/VOC2007/Annotations/"

test_list = os.listdir(fileDir)

for test in test_list:
    #print test
    f = open(fileDir+test, 'r')
    lines = f.readlines()
    for line in lines:
        #print line[10]
        for j in range(100):
            if line[j] == '1' and line[j+1] == '<' and line[j+2] == '/' and line[j+3] == 'n':
            #if line[j] == 'a':
                print line
                print test
                break
            break
    f.close()
