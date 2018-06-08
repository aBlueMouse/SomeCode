import sys
import numpy as np
sys.path.append('/home/sxl/caffe-master/python')
sys.path.append('/home/sxl/caffe-master/python/caffe')
import caffe
import matplotlib.pyplot as plt
#from PIL import Image
#import matplotlib.pyplot as plt
#import mahotas
#import scipy
from scipy import misc
import time

caffe.set_device(0)
caffe.set_mode_gpu()

start = time.clock()

hei = 1080
wid = 1320
h = 545
w = 665
zong = np.zeros((hei, wid))

for i in range(1,5):
    root='/home/sxl/caffe-master/'   
    deploy=root + 'examples/lanhao/zong/255_bi_with10y_deploy_' + str(i) + '.prototxt'    
    caffe_model=root + 'examples/lanhao/snapshot_x8/bi_with10y_test_iter_150000.caffemodel'  
    #deploy=root + 'examples/lanhao/mid/mid_deploy.prototxt'    
    #caffe_model=root + 'examples/lanhao/mid/snapshot_x8/bi_with10y_test_iter_150000.caffemodel'    
    img=root+'examples/lanhao/paper/art/8/bds_8_' + str(i) + '.png'        
    #labels_filename = root + 'mnist/test/labels.txt' 

    net = caffe.Net(deploy,caffe_model,caffe.TEST)   


    transformer = caffe.io.Transformer({'data1': net.blobs['data1'].data.shape})  
    transformer.set_transpose('data1', (2,0,1))

    #start = time.clock()
    
    im=caffe.io.load_image(img, color = False)                  
    net.blobs['data1'].data[...] = transformer.preprocess('data1',im)   
 
    #im=caffe.io.load_image(img, color = False) 
    #im_input=im[np.newaxis,:,:,:].transpose(0,3,1,2) 
    #net.blobs['data1'].reshape(*im_input.shape)
    #net.blobs['data1'].data[...] = im_input        


    out = net.forward()

    #sr = out['conv7']
    sr = net.blobs['sum'].data[0].transpose(1,2,0)
    #print sr.shape
    #print(type(sr))

    #sr = sr.transpose(2, 3, 1, 0)
    lh = sr[: ,: ,0]

    lh[lh < 0] = 0
    lh[lh > 1] = 1

    #end = time.clock()
    #print('Running time: %s Seconds'%(end-start))

    #lh = lh*255
    #lh = np.uint8(lh)
    #print lh.shape
    #print(type(lh))
    #plt.imshow(lh)
    #misc.imsave('examples/lanhao/sr100000.png', lh)
    if i == 1:
        zong[0 : (hei/2), 0 : (wid/2)] = lh[0 : (hei/2), 0 : (wid/2)]
    elif i == 2:
        zong[0 : (hei/2), (wid/2) : wid] = lh[0 : (hei/2), 5 : w]
    elif i == 3:
        zong[(hei/2) : hei, 0 : (wid/2)] = lh[5 : h, 0 : (wid/2)]
    elif i == 4:
        zong[(hei/2) : hei, (wid/2) : wid] = lh[5 : h, 5 : w]
        break

end = time.clock()
print('Running time: %s Seconds'%(end-start))
misc.toimage(zong, cmin=0.0, cmax=1.0).save('examples/lanhao/sr150000_x8.png')
