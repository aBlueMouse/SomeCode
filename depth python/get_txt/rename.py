import numpy as np

f = open('label.txt','r')
f1 = open('rgb.txt','a+')

for j in range(235360):
    line = f.readline()
    for i in range(100):
        if line[i] == 'i' and line[i+1] == 'm':
            #print 'kkkkk'
            f1.write('rgb - data/rgb_rgb' + line[i+2:])
            break
f.close()
f1.close()
