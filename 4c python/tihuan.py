#coding:utf-8

import os

import re

#list files

def listFiles(dirPath):

    fileList=[]

    for root,dirs,files in os.walk(dirPath):

	for fileObj in files:

	    fileList.append(os.path.join(root,fileObj))

    return fileList

 

def main():

    fileDir = "/home/sxl/caffe-ssd/data/VOCdevkit/VOC2007/Annotations"

    regex = ur'FUNC_SYS_ADD_ACCDETAIL'

    fileList = listFiles(fileDir)

    for fileObj in fileList:

	f = open(fileObj,'r+')

	all_the_lines=f.readlines()

	f.seek(0)

	f.truncate()

	for line in all_the_lines:
            #str1 = r'C:\Users\Administrator\Desktop\windows_v1.3.3\image' + '\\'
            #str1 = '<path>'
            #str2 = '<!--<path>'
            str1 = '6</name>'
            str2 = '5</name>'
	    if f.write(line.replace(str1 , str2)):
                print fileObj    

	f.close()  

if __name__=='__main__':

    main() 
