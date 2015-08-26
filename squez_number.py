# coding=utf-8
import os

path =  '/home/arnold-hu/project/soda/location_accident.txt'
new_path = '/home/arnold-hu/project/soda/number_data_accident.txt'
try:
	os.remove(new_path)
finally:
	with open(new_path, 'a+') as number:
		head = ','.join(['id', 'accident_id', 'flag', 'time', 'lat', 'lng'])
		h=number.write(head + '\n')
	with open(path, 'r') as f:
		for line in f.readlines():
			line = line.strip('\n')
			with open(new_path, 'a+') as number:
				line = line.split(',')
				if line[3] == '死亡事故': 
					flag =1
				elif line[3] == '伤人事故': 
					flag =2
				else:
					flag = 3
				record = ','.join([line[0], line[2], str(flag), line[5], line[6], line[7]])
				number.write(record + '\n')