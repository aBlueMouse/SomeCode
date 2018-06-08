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

    fileDir = "/media/sxl/68D6-4832/0824/label"

    regex = ur'FUNC_SYS_ADD_ACCDETAIL'

    fileList = listFiles(fileDir)

    for fileObj in fileList:

	f = open(fileObj,'r+')

	all_the_lines=f.readlines()

	f.seek(0)

	f.truncate()

	rep=re.escape(r"y")
        f=re.sub("<a>\n"+rep+"\n<b>","<a>\n<b>",f)
   
	f.close()  

if __name__=='__main__':

    main() 
