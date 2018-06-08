import numpy as np

f = open('test_1.txt','r')
f1 = open('test_3.txt','a+')

for j in range(343568):
    line = f.readline()
    for i in range(100):
        if line[i] == '_' and line[i+1] == 'd':
            #print 'kkkkk'
            f1.write('rgb-data/rgb_rgb' + line[i+6:])
            break
f.close()
f1.close()
