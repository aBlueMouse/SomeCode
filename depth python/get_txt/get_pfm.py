import os
import os.path
import re
import numpy as np
import sys
import matplotlib.pyplot as plt
from scipy import misc

def readPFM(file):
    file = open(file, 'rb')

    color = None
    width = None
    height = None
    scale = None
    endian = None

    header = file.readline().rstrip()
    if header == 'PF':
        color = True
    elif header == 'Pf':
        color = False
    else:
        raise Exception('Not a PFM file.')

    dim_match = re.match(r'^(\d+)\s(\d+)\s$', file.readline())
    if dim_match:
        width, height = map(int, dim_match.groups())
    else:
        raise Exception('Malformed PFM header.')

    scale = float(file.readline().rstrip())
    if scale < 0: # little-endian
        endian = '<'
        scale = -scale
    else:
        endian = '>' # big-endian

    data = np.fromfile(file, endian + 'f')
    shape = (height, width, 3) if color else (height, width)

    data = np.reshape(data, shape)
    data = np.flipud(data)
    return data, scale

path = "/media/sxl/LH/record/0328/Sampler/FlyingThings3D/disparity"

for parent, dirname ,filenames in os.walk(path):
	for filename in filenames:
		#print "parent is:" + parent
		#print "filename is:" + filename
		namelen = len(filename)
		[lh1, lh2] = readPFM(parent + '/' + filename)
		misc.imsave(parent + '/' + filename[ :namelen-4] + '.png' , lh1)
