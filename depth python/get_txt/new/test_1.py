import numpy as np

f = open('test2.txt','r')
f1 = open('test_1.txt','a+')
f2 = open('test_2.txt','a+')

for j in range(343568):
    line = f.readline()
    for i in range(100):
        if line[i] == '1' and line[i+1] == '@':
            #print 'kkkkk'
            f1.write(line[:i+1] + '\n')
            f2.write(line[i+2:])
            break
f.close()
f1.close()
f2.close()
