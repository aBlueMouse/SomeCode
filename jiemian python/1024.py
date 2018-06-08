
# coding: utf-8
from __future__ import unicode_literals, print_function
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
#from scipy import misc
import  xml.dom.minidom
#get_ipython().magic(u'matplotlib inline')

received = raw_input()
file_temp = open("result1.xml", "w+")
file_temp.write(received)
file_temp.close()

dom = xml.dom.minidom.parse('result1.xml')
root = dom.documentElement

test_dir_1 = dom.getElementsByTagName('Test_Dir')
test_dir_2 = test_dir_1[0]
test_dir = test_dir_2.firstChild.data

labelmap_file_1 = dom.getElementsByTagName('LabelMap_File')
labelmap_file_2 = labelmap_file_1[0]
labelmap_file = labelmap_file_2.firstChild.data

model_def_1 = dom.getElementsByTagName('Model_Def')
model_def_2 = model_def_1[0]
model_def = model_def_2.firstChild.data

model_weights_1 = dom.getElementsByTagName('Model_Weights')
model_weights_2 = model_weights_1[0]
model_weights = model_weights_2.firstChild.data

test_dir = test_dir.encode('unicode-escape').decode('string_escape')
labelmap_file = labelmap_file.encode('unicode-escape').decode('string_escape')
model_def = model_def.encode('unicode-escape').decode('string_escape')
model_weights = model_weights.encode('unicode-escape').decode('string_escape')

'''print type(test_dir)
test_dir = 'E:\\4C\\4c_windows\images3\\'
print type(test_dir)
print(labelmap_file)
print(model_def)
print(model_weights)'''

plt.rcParams['figure.figsize'] = (50, 50)
plt.rcParams['image.interpolation'] = 'nearest'
plt.rcParams['image.cmap'] = 'gray'

import sys
sys.path.insert(0, 'python')

import caffe
# caffe.set_mode_cpu()

from google.protobuf import text_format
from caffe.proto import caffe_pb2

file = open(labelmap_file, 'r')
labelmap = caffe_pb2.LabelMap()
text_format.Merge(str(file.read()), labelmap)

# def get_labelname(labelmap, labels):
#     num_labels = len(labelmap.item)
#     labelnames = []
#     if type(labels) is not list:
#         labels = [labels]
#     for label in labels:
#         found = False
#         for i in xrange(0, num_labels):
#             if label == labelmap.item[i].label:
#                 found = True
#                 labelnames.append(labelmap.item[i].display_name)
#                 break
#         assert found == True
#     return labelnames

net = caffe.Net(model_def,      # defines the structure of the model
                model_weights,  # contains the trained weights
                caffe.TEST)     # use test mode (e.g., don't perform dropout)

# input preprocessing: 'data' is the name of the input blob == net.inputs[0]
transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
transformer.set_transpose('data', (2, 0, 1))
transformer.set_mean('data', np.array([104,117,123])) # mean pixel
transformer.set_raw_scale('data', 255)  # the reference model operates on images in [0,255] range instead of [0,1]
transformer.set_channel_swap('data', (2,1,0))  # the reference model has channels in BGR order instead of RGB

image_resize1 = 500
image_resize2 = 750
net.blobs['data'].reshape(1,3,image_resize1,image_resize2)

image = caffe.io.load_image(test_dir)

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
# top_labels = get_labelname(labelmap, top_label_indices)
top_xmin = det_xmin[top_indices]
top_ymin = det_ymin[top_indices]
top_xmax = det_xmax[top_indices]
top_ymax = det_ymax[top_indices]

out = ''
for i in xrange(top_conf.shape[0]):
    xmin = int(round(top_xmin[i] * image.shape[1]))
    ymin = int(round(top_ymin[i] * image.shape[0]))
    xmax = int(round(top_xmax[i] * image.shape[1]))
    ymax = int(round(top_ymax[i] * image.shape[0]))
    score = top_conf[i]
    label = int(top_label_indices[i])
    #label_name = top_labels[i]
#    display_txt = '%s: %.2f'%(label_name, score)
    coords = xmax-xmin+1, ymax-ymin+1, ymin, xmin
    out += coords.__str__() + '\n'

result = out[: -1]
file_temp = open("temp.data", "w+")
file_temp.write(result)
file_temp.close()