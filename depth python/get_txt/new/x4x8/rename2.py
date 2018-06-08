import numpy as np

f = open('data2.txt','r')
f1 = open('data8.txt','a+')

for j in range(343568):
    line = f.readline()
    for i in range(100):
        if line[i] == '_' and line[i+1] == '2':
            #print 'kkkkk'
            f1.write('depth-data8/data_8' + line[i+2:])
            break
f.close()
f1.close()
