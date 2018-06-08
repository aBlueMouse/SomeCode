import csv
import os
import argparse

def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('--cloth', required=True, type=str,
                        help='name of the cloth')
	parser.add_argument('--ann', required=True, type=str,
                        help='path of the csv')
	args = parser.parse_args()
	return args
	
def write_csv(name, results):
	import csv
	with open(name, 'w') as f:
		writer = csv.writer(f)
		writer.writerows(results)
		
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
	
def generate_csv(ann, cloth):
	non = '-1_-1_-1'
	if cloth == 'blouse':
		num_imgs = len(ann)
		results = []
		for i in range(num_imgs):
			print('{}:{}/{}'.format(cloth, i+1, num_imgs))
			row = ann[i]
			submit_bluse = []
			for j in range(0, 9):
				submit_bluse.append(row[j])
			for j in range(2):
				submit_bluse.append(non)
			for j in range(9, 15):
				submit_bluse.append(row[j])
			for j in range(9):
				submit_bluse.append(non)
			'''submit_bluse = row[0]+row[1]+row[2]+row[3]+row[4]+row[5]+row[6]+\
			row[7]+row[8]+(non*2)+row[9]+row[10]+row[11]+row[12]+row[13]+\
			row[14]+(non*9)'''
			results.append(submit_bluse)
		write_csv('submit_bluse.csv', results)
	elif cloth == 'skirt':
		num_imgs = len(ann)
		results = []
		for i in range(num_imgs):
			print('{}:{}/{}'.format(cloth, i+1, num_imgs))
			row = ann[i]
			submit_skirt = []
			for j in range(0, 2):
				submit_skirt.append(row[j])
			for j in range(15):
				submit_skirt.append(non)
			for j in range(2, 6):
				submit_skirt.append(row[j])
			for j in range(5):
				submit_skirt.append(non)
			'''submit_skirt = row[0]+row[1]+(non*15)+row[2]+row[3]+row[4]+row[5]+\
			(non*5)'''
			results.append(submit_skirt)
		write_csv('submit_skirt.csv', results)
	elif cloth == 'outwear':
		num_imgs = len(ann)
		results = []
		for i in range(num_imgs):
			print('{}:{}/{}'.format(cloth, i+1, num_imgs))
			row = ann[i]
			submit_outwear = []
			for j in range(0, 4):
				submit_outwear.append(row[j])
			for j in range(1):
				submit_outwear.append(non)
			for j in range(4, 16):
				submit_outwear.append(row[j])
			for j in range(9):
				submit_outwear.append(non)
			'''submit_outwear = row[0]+row[1]+row[2]+row[3]+non+row[4]+row[5]+\
			row[6]+row[7]+row[8]+row[9]+row[10]+row[11]+row[12]+row[13]+\
			row[14]+row[15]+(non*9)'''
			results.append(submit_outwear)
		write_csv('submit_outwear.csv', results)
	elif cloth == 'dress':
		num_imgs = len(ann)
		results = []
		for i in range(num_imgs):
			print('{}:{}/{}'.format(cloth, i+1, num_imgs))
			row = ann[i]
			submit_dress = []
			for j in range(0, 15):
				submit_dress.append(row[j])
			for j in range(4):
				submit_dress.append(non)
			for j in range(15, 17):
				submit_dress.append(row[j])
			for j in range(5):
				submit_dress.append(non)
			'''submit_dress = row[0]+row[1]+row[2]+row[3]+row[4]+row[5]+\
			row[6]+row[7]+row[8]+row[9]+row[10]+row[11]+row[12]+row[13]+\
			row[14]+(non*4)+row[15]+row[16]+(non*5)'''
			results.append(submit_dress)
		write_csv('submit_dress.csv', results)
	elif cloth == 'trousers':
		num_imgs = len(ann)
		results = []
		for i in range(num_imgs):
			print('{}:{}/{}'.format(cloth, i+1, num_imgs))
			row = ann[i]
			submit_trousers = []
			for j in range(0, 2):
				submit_trousers.append(row[j])
			for j in range(15):
				submit_trousers.append(non)
			for j in range(2, 4):
				submit_trousers.append(row[j])
			for j in range(2):
				submit_trousers.append(non)
			for j in range(4, 9):
				submit_trousers.append(row[j])
			'''submit_trousers = row[0]+row[1]+(non*15)+row[2]+row[3]+(non*2)+row[4]+row[5]+\
			row[6]+row[7]+row[8]'''
			results.append(submit_trousers)
		write_csv('submit_trousers.csv', results)
	
def main():	
	args = parse_args()
	
	ann_file = args.ann
	info, anns = read_csv(ann_file)
	
	cloth = args.cloth
	generate_csv(anns, cloth)
	
if __name__ == '__main__':
    main()
