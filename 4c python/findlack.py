import os

imgpath = '/media/sxl/9A46-C9B4/0926/0919'
annopath = '/media/sxl/9A46-C9B4/0926/label'

img_list = os.listdir(imgpath)
anno_list = os.listdir(annopath)

img_list.sort(key= lambda x:int(x[:-4]))
anno_list.sort(key= lambda x:int(x[:-4]))

#print img_list[1][0:6]

for i in range(4057):
    if img_list[i][0:6] != anno_list[i][0:6]:
        print img_list[i]
        break
