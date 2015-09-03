# coding=utf-8
import time
import re
import urllib2
import os
import json


key = 'ak=XoGwGhTaucOT9P95tnFXVOXm'
city = 'city=上海'
path = '/home/arnold-hu/project/soda/accident.txt'
result_path = '/home/arnold-hu/project/soda/location_accident.txt'  # 用于存放增加经纬度信息并且剔除经纬度无效的数据，保存的信息最完整
number_data_path = '/home/arnold-hu/project/soda/number_data_accident.txt' # 用于存放全数字化信息
map_data_path = '/home/arnold-hu/project/soda/map_data.txt'  #用于存放将要提交给百度地图api的json信息
count = 0
points = [] 

#输入精度系数，地图将会按index的数量把地图均等分割，然后把每一块的事故集中到中点
index = raw_input('请输入地图分割精度（数字越大地图分割越细）: ')
index = int(index)
#确定上海市经纬度范围并求出各个grid中点坐标
lllat =30.6 
urlat=32 
lllon=120.9
urlon=122
lats = [lllat + (urlat - lllat)*(x+0.5)/index for x in range(index)]
lons = [lllon + (urlon - lllon)*(x+0.5)/index for x in range(index)]
centers = [(x,y) for x in lons for y in lats]
lon_all = [x[0] for x in centers]
lat_all = [x[1] for x in centers]
size = [0] * (index * index)

#创建或覆盖原有的number_data_accdent.txt用来储存全数字化数据，并给其增加头部索引以便后来分析
with open(number_data_path, 'w+') as number:
	head = ','.join(['id', 'accident_id', 'flag', 'date', 'time', 'lng', 'lat'])
	h=number.write(head + '\n')

#主要操作
try:
	os.remove(result_path)  # 删除原文件
finally:
	with open(path, 'r') as f:
		for line in f.readlines()[1:]:
			line = line.strip('\n')
			addr = line.split(',')[3]
			address = addr.split('约')[0]
			add =  'address=' + address
			req = 'http://api.map.baidu.com/geocoder/v2/?' + '&'.join([key, add, city]) 
			web = urllib2.urlopen(req)
			webdata = web.readlines()
			try:
				lat = re.search('\d+\.\d+', webdata[6]).group()
				lng = re.search('\d+\.\d+', webdata[7]).group()
				lines = line.split(',')
				date = lines[4].split(' ')[0]
				time = lines[4].split(' ')[1]
				count = count + 1
				#向location_accident.txt填充数据
				with open(result_path, 'a+') as result:
					r = line + ',' + lng + ',' + lat 
					result.write(str(count) + ',' +r + '\n')
				#向number_data_accident.txt填充数据
				with open(number_data_path, 'a+') as number:
					#用flg表示事故类型，1为死亡，2为伤人，3为财产损失或其他
					if lines[2] == '死亡事故': 
						flag =1
					elif lines[2] == '伤人事故': 
						flag =2
					else:
						flag = 3
					number_line = ','.join([str(count), lines[1], str(flag), date, time, str(lng), str(lat)])
					number.write(number_line + '\n')
				# 如果事故点在上海市范围，则所属grid的计数加1
				if (float(lng) <= urlon and float(lng) >= lllon and float(lat) <= urlat and float(lat) >= lllat):
					lat_shift = int( (float(lng) - lllon) / ((urlon - lllon) / index)) 
					lon_shift = int( (float(lat) - lllat) / ((urlat - lllat) / index )) 
					size[index * lat_shift + lon_shift] += 1

			except AttributeError:   # 若生成经纬度的api出现错误，或者时间信息不全，则pass此记录
				pass
			except IndexError:
				pass


#生成points变量，转化为json格式，并写入文件
for i in range(len(lon_all)):
	points.append({"lng":lon_all[i], "lat":lat_all[i], "count":size[i]*5})
points = json.dumps(points, indent=4)
with open(map_data_path, 'w+') as md:
	md.write(points)




