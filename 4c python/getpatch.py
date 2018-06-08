from __future__ import division  
import os  
from PIL import Image  
import xml.dom.minidom  
import numpy as np  
  
ImgPath = '/home/sxl/caffe-ssd/data/dianwang/testimage/'   
AnnoPath = '/home/sxl/caffe-ssd/data/dianwang/testannotation/'  
ProcessedPath = '/home/sxl/caffe-ssd/data/dianwang/testcrop/'  
savepath = '/home/sxl/caffe-ssd/data/dianwang/testcrop'  
  
if not os.path.exists(ProcessedPath):  
    os.makedirs(ProcessedPath)  
  
imagelist = os.listdir(ImgPath)  
  
for image in imagelist:  
    print 'a new image:', image  
    image_pre, ext = os.path.splitext(image)  
    imgfile = ImgPath + image   
    xmlfile = AnnoPath + image_pre + '.xml'  
      
    DomTree = xml.dom.minidom.parse(xmlfile)  
    annotation = DomTree.documentElement  
  
    filenamelist = annotation.getElementsByTagName('filename') #[<DOM Element: filename at 0x381f788>]  
    filename = filenamelist[0].childNodes[0].data  
    objectlist = annotation.getElementsByTagName('object')  
      
    i = 1  
    for objects in objectlist:  
        # print objects  
          
        namelist = objects.getElementsByTagName('name')  
        # print 'namelist:',namelist  
        objectname = namelist[0].childNodes[0].data  
        print objectname  
  
  
        bndbox = objects.getElementsByTagName('bndbox')  
        #cropboxes = []  
        for box in bndbox:  
            try:  
                x1_list = box.getElementsByTagName('xmin')  
                x1 = int(x1_list[0].childNodes[0].data)
                print x1  
                y1_list = box.getElementsByTagName('ymin')  
                y1 = int(y1_list[0].childNodes[0].data)  
                x2_list = box.getElementsByTagName('xmax')  
                x2 = int(x2_list[0].childNodes[0].data)  
                y2_list = box.getElementsByTagName('ymax')  
                y2 = int(y2_list[0].childNodes[0].data)  
                w = x2 - x1  
                h = y2 - y1  
  
                img = Image.open(imgfile)  
                width,height = img.size  
                      
                #for cropbox in cropboxes:  
                    # print 'cropbox:',cropbox  
                    #minX = max(0,cropbox[0])  
                    #minY = max(0,cropbox[1])  
                    #maxX = min(cropbox[2],width)  
                    #maxY = min(cropbox[3],height)  
  
                cropbox = (x1,y1,x2,y2)  
                cropedimg = img.crop(cropbox)  
                cropedimg.save(savepath + '/' + image_pre + '_' + str(i) + '.jpg')  
                i += 1  
  
            except Exception, e:  
                print e  
