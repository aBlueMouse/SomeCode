import time
import os
import cv2
import csv
import numpy as np
import tensorflow as tf
os.environ['CUDA_VISIBLE_DEVICES'] = '2'
#--------------Model preparation----------------
# Path to frozen detection graph. This is the actual model that is used for 
# the object detection.
PATH_TO_CKPT = 'train_skirt/output_inference_graph/frozen_inference_graph.pb'

# Load a (frozen) Tensorflow model into memory
detection_graph = tf.Graph()
with detection_graph.as_default():
  od_graph_def = tf.GraphDef()
  with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
    serialized_graph = fid.read()
    od_graph_def.ParseFromString(serialized_graph)
    tf.import_graph_def(od_graph_def, name='')

image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
# Each box represents a part of the image where a particular 
# object was detected.
gboxes = detection_graph.get_tensor_by_name('detection_boxes:0')
# Each score represent how level of confidence for each of the objects.
# Score is shown on the result image, together with the class label.
gscores = detection_graph.get_tensor_by_name('detection_scores:0')
gclasses = detection_graph.get_tensor_by_name('detection_classes:0')
gnum_detections = detection_graph.get_tensor_by_name('num_detections:0')

def read_csv(ann_file):
    info = []
    anns = []
    with open(ann_file, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            anns.append(row)
    info = anns[0]
    anns = anns[1:]
    return info, anns

# TODO: Add class names showing in the image
def detect_image_objects(image, sess, detection_graph):
    # Expand dimensions since the model expects images to have 
    # shape: [1, None, None, 3]
    image_np_expanded = np.expand_dims(image, axis=0)

    # Actual detection.
    (boxes, scores, classes, num_detections) = sess.run(
        [gboxes, gscores, gclasses, gnum_detections],
        feed_dict={image_tensor: image_np_expanded})

    # Visualization of the results of a detection.
    boxes = np.squeeze(boxes)
    scores = np.squeeze(scores)
    height, width = image.shape[:2]
    key = 0
    for i in range(boxes.shape[0]):
        #if (scores is None or scores[i] > 0.5):
        if(scores[i]>scores[key]):
            key = i            
    ymin, xmin, ymax, xmax = boxes[key]
    ymin = int(ymin * height)
    ymax = int(ymax * height)
    xmin = int(xmin * width)
    xmax = int(xmax * width)
    return xmin, ymin, xmax, ymax
'''         score = None if scores is None else scores[i]
            font = cv2.FONT_HERSHEY_SIMPLEX
            text_x = np.max((0, xmin - 10))
            text_y = np.max((0, ymin - 10))
            cv2.putText(image, 'Detection score: ' + str(score), (text_x, text_y), font, 0.4, (0, 255, 0))
            cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2) '''

test_csv = 'test3/test_skirt.csv'
info, anns = read_csv(test_csv)
test_result_csv = 'skirt_with_bbox.csv'
with detection_graph.as_default():
    with tf.Session(graph=detection_graph) as sess:
        for i in range(len(anns)):
            print i
            print anns[i][0]
            image = cv2.imread('test3/'+anns[i][0])
            #t_start = time.clock()
            xmin, ymin, xmax, ymax = detect_image_objects(image, sess, detection_graph)
            anns[i] += [xmin, ymin, xmax, ymax]
            #t_end = time.clock()
            #print('detect time per frame: ', t_end - t_start)   
    with open(test_result_csv, 'wb') as f:
        writer = csv.writer(f)
        writer.writerows([info])
        writer.writerows(anns)
'''         
        cv2.imshow('detected', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows() '''
