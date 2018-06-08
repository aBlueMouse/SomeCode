import numpy as np
import csv
	
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
	
def _get_keypoints(ann):
	kpt = np.zeros((24, 3))
	for i in range(2, len(ann)):
		str = ann[i]
		[x_str, y_str, vis_str] = str.split('_')
		kpt[i - 2, 0], kpt[i - 2, 1], kpt[i - 2, 2] = int(x_str), int(y_str), int(vis_str)
	return kpt	

def prepare_row(ann, keypoints):
	# cls
	image_name = ann[0]
	category = ann[1]
	keypoints_str = []
	for i in range(24):
		cell_str = str(int(keypoints[i][0])) + '_' + str(int(keypoints[i][1])) + '_' + str(int(keypoints[i][2]))
		keypoints_str.append(cell_str)
	row = [image_name, category] + keypoints_str
	return row
	
def write_csv(name, results):
	import csv
	with open(name, 'w') as f:
		writer = csv.writer(f)
		writer.writerows(results)
		
def main():
	result1 = '/home/sxl/code/combine/result_CPM_FPN_0405.csv'
	result2 = '/home/sxl/code/combine/result_0405_21.1%.csv'
	k1 = 0.6
	k2 = 0.4
	name = 'result.csv'
	
	info1, anns1 = read_csv(result1)
	info2, anns2 = read_csv(result2)
	
	num_imgs = len(anns1)
	results = []
	results.append(info1)
	for i in range(num_imgs):
		kpt1 = _get_keypoints(anns1[i])
		kpt2 = _get_keypoints(anns2[i])
		
		kpt = k1 * kpt1 + k2 * kpt2
		
		row = prepare_row(anns1[i], kpt)
		results.append(row)
	write_csv(name, results)
	
if __name__ == '__main__':
    main()
