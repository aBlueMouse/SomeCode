
# coding: utf-8

# # Detection with SSD
# 
# In this example, we will load a SSD model and use it to detect objects.

# ### 1. Setup
# 
# * First, Load necessary libs and set up caffe and caffe_root

# In[40]:

from __future__ import division 
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy import misc
from PIL import Image
from skimage import exposure
import bisect
import shutil

#get_ipython().magic(u'matplotlib inline')


def imadjust(src, tol=1, vin=[0,255], vout=(0,255)):
    # src : input one-layer image (numpy array)
    # tol : tolerance, from 0 to 100.
    # vin  : src image bounds
    # vout : dst image bounds
    # return : output img

    dst = src.copy()
    tol = max(0, min(100, tol))

    if tol > 0:
        # Compute in and out limits
        # Histogram
        hist = np.zeros(256, dtype=np.int)
        for r in range(src.shape[0]):
            for c in range(src.shape[1]):
                hist[src[r,c]] += 1
        # Cumulative histogram
        cum = hist.copy()
        for i in range(1, len(hist)):
            cum[i] = cum[i - 1] + hist[i]

        # Compute bounds
        total = src.shape[0] * src.shape[1]
        low_bound = total * tol / 100
        upp_bound = total * (100 - tol) / 100
        vin[0] = bisect.bisect_left(cum, low_bound)
        vin[1] = bisect.bisect_left(cum, upp_bound)

    # Stretching
    scale = (vout[1] - vout[0]) / (vin[1] - vin[0])
    for r in range(dst.shape[0]):
        for c in range(dst.shape[1]):
            vs = max(src[r,c] - vin[0], 0)
            vd = min(int(vs * scale + 0.5) + vout[0], vout[1])
            dst[r,c] = vd
    return dst


plt.rcParams['figure.figsize'] = (50, 50)
plt.rcParams['image.interpolation'] = 'nearest'
plt.rcParams['image.cmap'] = 'gray'

# Make sure that caffe is on the python path:
caffe_root = '/home/sxl/caffe-ssd/'  # this file is expected to be in {caffe_root}/examples
import os
os.chdir(caffe_root)
import sys
sys.path.insert(0, 'python')

import caffe
#caffe.set_mode_cpu()
caffe.set_device(0)
caffe.set_mode_gpu()


# * Load LabelMap.

# In[41]:


from google.protobuf import text_format
from caffe.proto import caffe_pb2

# load PASCAL VOC labels
labelmap_file = caffe_root + 'data/VOC0712_old/labelmap_voc.prototxt'
file = open(labelmap_file, 'r')
labelmap = caffe_pb2.LabelMap()
text_format.Merge(str(file.read()), labelmap)

def get_labelname(labelmap, labels):
    num_labels = len(labelmap.item)
    labelnames = []
    if type(labels) is not list:
        labels = [labels]
    for label in labels:
        found = False
        for i in xrange(0, num_labels):
            if label == labelmap.item[i].label:
                found = True
                labelnames.append(labelmap.item[i].display_name)
                break
        assert found == True
    return labelnames


# * Load the net in the test phase for inference, and configure input preprocessing.

# In[42]:


model_def = caffe_root + 'models/4C/SSD_750x500/deploy.prototxt'
model_weights = caffe_root + 'models/4C/SSD_750x500/VGG_VOC0712_SSD_750x500_iter_125000.caffemodel'

net = caffe.Net(model_def,      # defines the structure of the model
                model_weights,  # contains the trained weights
                caffe.TEST)     # use test mode (e.g., don't perform dropout)

# input preprocessing: 'data' is the name of the input blob == net.inputs[0]
transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
transformer.set_transpose('data', (2, 0, 1))
transformer.set_mean('data', np.array([104,117,123])) # mean pixel
transformer.set_raw_scale('data', 255)  # the reference model operates on images in [0,255] range instead of [0,1]
transformer.set_channel_swap('data', (2,1,0))  # the reference model has channels in BGR order instead of RGB


# ### 2. SSD detection

# * Load an image.

# In[43]:


# set net to batch size of 1
image_resize1 = 500
image_resize2 = 750
net.blobs['data'].reshape(1,3,image_resize1,image_resize2)

test_dir = '/home/sxl/caffe-ssd/models/4C_dingweihuan/test/images3/' 
test_list = os.listdir(test_dir)
#print test_list
#savepath = '/home/sxl/caffe-ssd/models/4C_dingweihuan/test/images3_caijian/'
#if not os.path.exists(savepath):  
    #os.makedirs(savepath)
problempath = '/home/sxl/caffe-ssd/models/4C_dingweihuan/test/images3_problem/'
if not os.path.exists(problempath):  
    os.makedirs(problempath)

j = 1
for img in test_list:
    model_def = caffe_root + 'models/4C/SSD_750x500/deploy.prototxt'
    model_weights = caffe_root + 'models/4C/SSD_750x500/VGG_VOC0712_SSD_750x500_iter_125000.caffemodel'

    net = caffe.Net(model_def, model_weights, caffe.TEST)

# input preprocessing: 'data' is the name of the input blob == net.inputs[0]
    transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
    transformer.set_transpose('data', (2, 0, 1))
    transformer.set_mean('data', np.array([104,117,123])) # mean pixel
    transformer.set_raw_scale('data', 255)  # the reference model operates on images in [0,255] range instead of [0,1]
    transformer.set_channel_swap('data', (2,1,0))  # the reference model has channels in BGR order instead of RGB


# ### 2. SSD detection

# * Load an image.

# In[43]:


# set net to batch size of 1
    image_resize1 = 500
    image_resize2 = 750
    net.blobs['data'].reshape(1,3,image_resize1,image_resize2)
    #savepath = '/home/sxl/caffe-ssd/examples/4c/test/testcrop/'+img[:-4]+'/'
    #if not os.path.exists(savepath):  
    #    os.makedirs(savepath)
    savepath = '/home/sxl/caffe-ssd/models/4C_dingweihuan/test/images3_caijian/'
    if not os.path.exists(savepath):  
        os.makedirs(savepath) 
    image = caffe.io.load_image(test_dir + img)
    img_mid = Image.open(test_dir + img)
    width,height = img_mid.size
    #img_mid = cv2.imread(test_dir + img)
    #height = img_mid[0];
    #width = img_mid[1];
    print str(width)+' '+str(height)
    print type(image)
    image = cv2.resize(image, (750, 500))
#misc.toimage(image2, cmin=0.0, cmax=1.0).save('/home/sxl/caffe-ssd/examples/images/300.jpg')
    plt.subplot(1,2,1)
    plt.axis('OFF')
    plt.imshow(image)
#plt.show()


# * Run the net and examine the top_k results

# In[44]:


    transformed_image = transformer.preprocess('data', image)
    net.blobs['data'].data[...] = transformed_image

# Forward pass.
    detections = net.forward()['detection_out']

# Parse the outputs.
    det_label = detections[0,0,:,1]
    det_conf = detections[0,0,:,2]
    det_xmin = detections[0,0,:,3]
    det_ymin = detections[0,0,:,4]
    det_xmax = detections[0,0,:,5]
    det_ymax = detections[0,0,:,6]

# Get detections with confidence higher than 0.6.
    top_indices = [i for i, conf in enumerate(det_conf) if conf >= 0.2]

    top_conf = det_conf[top_indices]
    top_label_indices = det_label[top_indices].tolist()
    top_labels = get_labelname(labelmap, top_label_indices)
    top_xmin = det_xmin[top_indices]
    top_ymin = det_ymin[top_indices]
    top_xmax = det_xmax[top_indices]
    top_ymax = det_ymax[top_indices]


# * Plot the boxes

# In[45]:


    colors = plt.cm.hsv(np.linspace(0, 1, 21)).tolist()

    plt.subplot(1,2,2)
    plt.axis('OFF')
    plt.imshow(image)
    currentAxis = plt.gca()

    for i in xrange(top_conf.shape[0]):
        xmin = int(round(top_xmin[i] * image.shape[1]))
        ymin = int(round(top_ymin[i] * image.shape[0]))
        xmax = int(round(top_xmax[i] * image.shape[1]))
        ymax = int(round(top_ymax[i] * image.shape[0]))
        score = top_conf[i]
        label = int(top_label_indices[i])
        label_name = top_labels[i]
        display_txt = '%s: %.2f'%(label_name, score)
        coords = (xmin, ymin), xmax-xmin+1, ymax-ymin+1
        color = colors[label]
        #currentAxis.add_patch(plt.Rectangle(*coords, fill=False, edgecolor=color, linewidth=2))
        #currentAxis.text(xmin, ymin, display_txt, bbox={'facecolor':color, 'alpha':0.5})
        if label_name == 'dingweihuan':
            para1 = width/750
            para2 = height/500
            x1 = int(xmin*para1)
            x2 = int(xmax*para1)
            y1 = int(ymin*para2)
            y2 = int(ymax*para2)
            #cropedimg = img_mid[y1:y2, x1:x2]
            #cropedimg = cv2.equalizeHist(cropedimg)
            #cv2.imwrite(savepath + '/' + "%06d"%j + '.jpg', cropedimg)
            cropbox = (x1,y1,x2,y2)  
            cropedimg = img_mid.crop(cropbox)
            #cropedimg = cropedimg.resize((300, 300))
            cropedimg_ndarray = np.array(cropedimg)
            #print cropedimg_ndarray
            if cropedimg_ndarray.ndim == 3:
                cropedimg_ndarray = cv2.cvtColor(cropedimg_ndarray, cv2.COLOR_BGR2GRAY)
            cropedimg_ndarray = imadjust(cropedimg_ndarray)
            #cropedimg_ndarray = cv2.equalizeHist(cropedimg_ndarray)            
            #cropedimg_ndarray = exposure.equalize_hist(cropedimg_ndarray)
            cropedimg = Image.fromarray(cropedimg_ndarray) 
            cropedimg.save(savepath + '/' + img[0 : -4] + '.' + "%03d"%j + '.jpg')
            j += 1

    #plt.show()

################################################################################################
    labelmap_file_mini = 'data/VOC0712_dingweihuan/labelmap_voc.prototxt'
    file = open(labelmap_file_mini, 'r')
    labelmap_mini = caffe_pb2.LabelMap()
    text_format.Merge(str(file.read()), labelmap_mini)

# * Load the net in the test phase for inference, and configure input preprocessing.

# In[42]:


    model_def_mini = 'models/4C_dingweihuan/SSD_300x300/deploy.prototxt'
    model_weights_mini = 'models/4C_dingweihuan/SSD_300x300/VGG_VOC0712_SSD_300x300_iter_135000.caffemodel'

    net_mini = caffe.Net(model_def_mini, model_weights_mini, caffe.TEST)

        # input preprocessing: 'data' is the name of the input blob == net.inputs[0]
    transformer_mini = caffe.io.Transformer({'data': net_mini.blobs['data'].data.shape})
    transformer_mini.set_transpose('data', (2, 0, 1))
    transformer_mini.set_mean('data', np.array([104,117,123])) 
    transformer_mini.set_raw_scale('data', 255)  
    transformer_mini.set_channel_swap('data', (2,1,0))  

    image_resize1 = 300
    image_resize2 = 300
    net_mini.blobs['data'].reshape(1,3,image_resize1,image_resize2)

    test_list_mini = os.listdir(savepath)
    print test_list_mini
    for img_mini in test_list_mini:
        image_mini = caffe.io.load_image(savepath + img_mini)            
        transformed_image_mini = transformer_mini.preprocess('data', image_mini)
        net_mini.blobs['data'].data[...] = transformed_image_mini

# Forward pass.
        detections_mini = net_mini.forward()['detection_out']

# Parse the outputs.
        det_label_mini = detections_mini[0,0,:,1]
        det_conf_mini = detections_mini[0,0,:,2]

# Get detections with confidence higher than 0.6.
        top_indices_mini = [i for i, conf in enumerate(det_conf_mini) if conf >= 0.3]

        top_conf_mini = det_conf_mini[top_indices_mini]
        top_label_indices_mini = det_label_mini[top_indices_mini].tolist()            

        if np.mean(top_label_indices_mini) != 1.0:
            if not os.path.exists(problempath + img_mini):
                shutil.copy(savepath + img_mini, problempath)
            if os.path.exists(test_dir + img):
                shutil.move(test_dir + img, problempath)
        else:
            if np.sum(top_conf_mini)/len(top_label_indices_mini) <= 0.7:
                if not os.path.exists(problempath + img_mini):
                    shutil.copy(savepath + img_mini, problempath)
                if os.path.exists(test_dir + img):
                    shutil.move(test_dir + img, problempath)
                    

    shutil.rmtree(savepath)

