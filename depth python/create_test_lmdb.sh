DATA=examples/lanhao/paper/moebius/8
rm -rf $DATA/test_rgb_1_lmdb
build/tools/convert_imageset --gray \
/home/sxl/caffe-master/examples/lanhao/paper/moebius/8/ $DATA/rgb1.txt  $DATA/test_rgb_1_lmdb

rm -rf $DATA/test_rgb_2_lmdb
build/tools/convert_imageset --gray \
/home/sxl/caffe-master/examples/lanhao/paper/moebius/8/ $DATA/rgb2.txt  $DATA/test_rgb_2_lmdb

rm -rf $DATA/test_rgb_3_lmdb
build/tools/convert_imageset --gray \
/home/sxl/caffe-master/examples/lanhao/paper/moebius/8/ $DATA/rgb3.txt  $DATA/test_rgb_3_lmdb

rm -rf $DATA/test_rgb_4_lmdb
build/tools/convert_imageset --gray \
/home/sxl/caffe-master/examples/lanhao/paper/moebius/8/ $DATA/rgb4.txt  $DATA/test_rgb_4_lmdb
