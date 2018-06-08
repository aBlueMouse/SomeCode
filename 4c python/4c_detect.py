
# coding: utf-8

# # Detection with SSD
# 
# In this example, we will load a SSD model and use it to detect objects.

# ### 1. Setup
# 
# * First, Load necessary libs and set up caffe and caffe_root

# In[40]:

import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy import misc
#get_ipython().magic(u'matplotlib inline')

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
labelmap_file = 'data/VOC0712_old/labelmap_voc.prototxt'
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


model_def = 'models/4C/SSD_750x500/deploy.prototxt'
model_weights = 'models/4C/SSD_750x500/VGG_VOC0712_SSD_750x500_iter_300000.caffemodel'

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

#test_dir = '/home/sxl/caffe-ssd/examples/4c/images3/' 
test_dir = '/home/sxl/caffe-ssd/examples/4c/images3/'
test_list = os.listdir(test_dir)
print test_list
for img in test_list:
    image = caffe.io.load_image(test_dir + img)
    image2 = cv2.resize(image, (500, 750))
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
    top_indices = [i for i, conf in enumerate(det_conf) if conf >= 0.3]

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
        currentAxis.add_patch(plt.Rectangle(*coords, fill=False, edgecolor=color, linewidth=2))
        currentAxis.text(xmin, ymin, display_txt, bbox={'facecolor':color, 'alpha':0.5})

    plt.show()
# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




