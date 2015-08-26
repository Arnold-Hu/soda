# coding=utf-8
import time
import re
import urllib2
import os

key = 'ak=XoGwGhTaucOT9P95tnFXVOXm'
city = 'city=上海'
path = '/home/arnold-hu/\xe6\xa1\x8c\xe9\x9d\xa2/SODA_distSample/accident.txt'
result_path = '/home/arnold-hu/project/soda/location_accident.txt'
count = 0
os.remove(result_path)
with open(path, 'r') as f:
	for line in f.readlines()[1:]:
		line = line.strip('\n')
		addr = line.split(',')[3]
		address = addr.split('约')[0]
		add =  'address=' + address
		reqlist = [key, add, city]
		req = 'http://api.map.baidu.com/geocoder/v2/?' + '&'.join(reqlist) 
		web = urllib2.urlopen(req)
		webdata = web.readlines()
		try:
			lat = re.search('\d+\.\d+', webdata[6]).group()
			lng = re.search('\d+\.\d+', webdata[7]).group()
			count = count + 1
			with open(result_path, 'a+') as result:
				r = line + ',' + lat + ',' + lng 
				print r
				result.write(str(count) + ',' +r + '\n')
		except AttributeError:
			pass
		# 	with open(result_path, 'a+') as result:
		# 		r = line + ',' + 'null' + ',' + 'null'
		# 		print r
		# 		result.write(r + '\n')







