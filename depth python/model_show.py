import numpy as np
import matplotlib.pyplot as plt
import sys,os

sys.path.append('/home/sxl/caffe-master/python')
import caffe

caffe.set_mode_gpu()


#caffe.set_mode_cpu() # replace by caffe.set_mode_gpu() to run on a GPU
#net = caffe.Net('deploy.prototxt','noise_iter_100000.caffemodel', caffe.TEST)

root='/home/sxl/caffe-master/'   
deploy=root + 'examples/lanhao/255_bi_with10y_deploy.prototxt'    
caffe_model=root + 'examples/lanhao/snapshot255/bi_with10y_test_iter_10000.caffemodel'   
img=root+'examples/lanhao/test/19/bds2_19.png'       
net = caffe.Net(deploy,caffe_model,caffe.TEST) 

transformer = caffe.io.Transformer({'data1': net.blobs['data1'].data.shape})  
transformer.set_transpose('data1', (2,0,1))     
im=caffe.io.load_image(img, color = False)                  
net.blobs['data1'].data[...] = transformer.preprocess('data1',im)

net.forward()

def vis_square(data):  

        # normalize data for display  
        data = (data - data.min()) / (data.max() - data.min())  
      
        # force the number of filters to be square  
        n = int(np.ceil(np.sqrt(data.shape[0])))  
        padding = (((0, n ** 2 - data.shape[0]),  
               (0, 1), (0, 1))                 # add some space between filters  
               + ((0, 0),) * (data.ndim - 3))  # don't pad the last dimension (if there is one)  
        data = np.pad(data, padding, mode='constant', constant_values=1)  # pad with ones (white)  
      
        # tile the filters into an image  
        data = data.reshape((n, n) + data.shape[1:]).transpose((0, 2, 1, 3) + tuple(range(4, data.ndim + 1)))  
        data = data.reshape((n * data.shape[1], n * data.shape[3]) + data.shape[4:])  
      
        plt.imshow(data)  
        plt.show()  

print net.blobs['conv1'].data.shape
vis_square(net.blobs['conv1'].data[0])
vis_square(net.blobs['conv2'].data[0])
vis_square(net.blobs['conv3'].data[0])
vis_square(net.blobs['conv4'].data[0])
vis_square(net.blobs['conv5'].data[0])
vis_square(net.blobs['conv6'].data[0])
vis_square(net.blobs['conv7'].data[0])
vis_square(net.blobs['conv8'].data[0])
vis_square(net.blobs['conv9'].data[0])
vis_square(net.blobs['conv10'].data[0])
vis_square(net.blobs['conv11'].data[0])
vis_square(net.blobs['conv12'].data[0])
vis_square(net.blobs['conv13'].data[0])
vis_square(net.blobs['conv14'].data[0])
vis_square(net.blobs['conv15'].data[0])
vis_square(net.blobs['conv16'].data[0])
vis_square(net.blobs['conv17'].data[0])
vis_square(net.blobs['conv18'].data[0])
vis_square(net.blobs['conv19'].data[0])
vis_square(net.blobs['conv20'].data[0])

#vis_square(net.params['conv3'][0].data)
