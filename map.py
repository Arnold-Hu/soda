#coding:utf-8


from mpl_toolkits.basemap import Basemap,cm
import matplotlib.pyplot as plt
import random
import json
path = '/home/arnold-hu/project/soda/number_data_accident.txt'
def basic_shanghai_map(ax=None, lllat = 31, urlat=32, lllon=121, urlon=122,width=None,height=None):
    m = Basemap(ax=ax, projection='cyl',
                lon_0=(urlon + lllon)/2,
                lat_0=(urlat + lllat)/2,
                llcrnrlat=lllat, urcrnrlat=urlat,
                llcrnrlon=lllon, urcrnrlon=urlon,
                resolution='f', width=None,
                height=None)
    m.drawcoastlines()
    m.drawstates()
    m.drawcountries()
    m.fillcontinents(color='0.95')
    return m
# data = []
lllat =30.6 
urlat=32 
lllon=120.9
urlon=122
width = (urlat - lllat) * 300
height = (urlon - lllon) * 300

index = 25
lons=[]
lats=[]


maptry =  basic_shanghai_map(ax=None, lllat=lllat, urlat=urlat, lllon=lllon, urlon=urlon,width=width,height=height)
with open(path) as d:
	for line in d.readlines()[1:]:
		line = line.strip('\n')
		line = line.split(',')
		lon = float(line[5])
		lat = float(line[6])
		lons.append(lon)
		lats.append(lat)
		

		# data.append(random.randint(1,10))
x,y = maptry(lons, lats)
#fix_size = [i * 200 / index for i in size]



maptry.scatter(x, y  , 5, zorder=10)

road_path = '/home/arnold-hu/map/CHN_roads'
# boundary_path = '/home/arnold-hu/map/bou2_4p'
maptry.readshapefile(road_path, 'roads')
# maptry.readshapefile(boundary_path, 'boundary')
plt.show(maptry)

