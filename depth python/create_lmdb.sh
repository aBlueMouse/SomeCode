DATA=examples/lanhao/train
rm -rf $DATA/data2_lmdb
build/tools/convert_imageset --gray \
/home/sxl/caffe-master/examples/lanhao/train/ $DATA/data2.txt  $DATA/data2_lmdb
