#! /bin/bash

#org_path='/media/lib549/ECA6B990A6B95C30/WEI/caffe-ssd/models/VGGNet/VOC0712/20171206/detect_result/'
det_list_name='test.txt'
dst_file1='test_jpg.txt'
dst_file2='test_xml.txt'
#new_path1='\/home\/sxl\/caffe-ssd\/data\/VOCdevkit\/VOC2007\/JPEGImages\/'
#new_path2='\/home\/sxl\/caffe-ssd\/data\/VOCdevkit\/VOC2007\/Annotations\/'
new_path1='\/home\/sxl\/caffe-ssd\/data\/dianwang\/gailujing\/img\/'
new_path2='\/home\/sxl\/caffe-ssd\/data\/dianwang\/gailujing\/label\/'
jpg_houzui='.jpg'

if [ -f $dst_file1 ]
then
  rm -f $dst_file1
fi

if [ -f $dst_file2 ]
then
  rm -f $dst_file2
fi

cp $det_list_name $dst_file1
sed -i "s/^/${new_path1}/g" $dst_file1
sed -i "s/$/.jpg/g" $dst_file1

cp $det_list_name $dst_file2
sed -i "s/^/${new_path2}/g" $dst_file2
sed -i "s/$/.xml/g" $dst_file2
