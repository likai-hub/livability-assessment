# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 13:26:56 2019

@author: Administrator
"""

#import geopy
import os
import ogr
import numpy as np
from scipy.spatial.distance import cdist
from geopy import distance
#import urllib2
# when python version is 3.7
import urllib

import json
import time

#********************************************************************************************************************************            
def getDistance(origin,destination):
    # origin and destination should have a dimension of [2,],array([  34.98032273,  118.28843478])
    origin=','.join(map(lambda x:'%6f'%x,origin))
    destination=','.join(map(lambda x:'%6f'%x,destination))
    # url='http://api.map.baidu.com/direction/v2/riding?'
    url='http://api.map.baidu.com/routematrix/v2/walking?'
    output = 'json'
    # Likai
#    ak = 'v9ntzrdoClxSU4uMpLlk3DrLeDvhoPGH'
    # Hui's AK
    ak='mznuxpzGx7HUx6QLhHgq6P1HsBjdkPHO'
    coordType='wgs84'
    uri = url + 'origins=' + origin + '&destinations=' + destination + '&output=' + output + '&coord_type='+coordType+'&ak=' + ak
    print(uri)
#    req = urllib2.urlopen(uri)
    req=urllib.request.urlopen(uri)
    res = req.read()
    temp = json.loads(res)            

#    print(temp)
    distance = temp['result'][0]['distance']['value']/1000.0 # 那个0是因为它返回的routes是一个list，所以索引0就是第一条路线
    req.close()
#    duration = temp['result']['routes'][0]['duration']
    # print '距离%.2f千米，骑车耗时%d分钟' % (float(distance) / 1000, round(int(duration) / 60))
    return distance       
#********************************************************************************************************************************
    
    
outputFolder=r'H:\geography_presentation\indices_system'
if not os.path.exists(outputFolder):
    os.makedirs(outputFolder)


parkFile=r'H:\geography_presentation\parks\parks.shp'
squareFile=r'H:\geography_presentation\parks\squares.shp'
commFile=r'H:\geography_presentation\communities\digitalized\communities_digitalized.shp'

# Get driver by name
driver=ogr.GetDriverByName('ESRI Shapefile')

# open primary schoo; shapefile   (target file) 
dataSource1 = driver.Open(parkFile, 0)
if dataSource1 is None:
    print ('Could not open %s' % (parkFile))
else:
    print( 'Opened %s' % (parkFile))
    layer = dataSource1.GetLayer()
    
targetPts=np.empty((0,2))
parkSquareList=[]

#fid=open(r'G:\geography_presentation\test\test.txt','w')
for feature in layer:
    lat=feature.GetField('lat')
    lng=feature.GetField('lng')
#    print(lat)
    targetPts=np.vstack((targetPts,np.array([lat,lng])))
    name=feature.GetField('name')
#    print(name)
#    fid.write(name+'\n')
    parkSquareList.append(name)
#fid.close()

dataSource1=None

# squares

# open primary schoo; shapefile   (target file) 
dataSource1 = driver.Open(squareFile, 0)
if dataSource1 is None:
    print( 'Could not open %s' % (squareFile))
else:
    print ('Opened %s' % (squareFile))
    layer = dataSource1.GetLayer()
    
#targetPts2=np.empty((0,2))
#highList=[]
#fid=open(r'G:\geography_presentation\test\test.txt','w')
for feature in layer:
    lat=feature.GetField('lat')
    lng=feature.GetField('lng')
#    print(lat)
    targetPts=np.vstack((targetPts,np.array([lat,lng])))
    name=feature.GetField('name')
#    print(name)
#    fid.write(name+'\n')
    parkSquareList.append(name)
#fid.close()
dataSource1=None

# open community shapefile (source file)
dataSource2 = driver.Open(commFile, 0)
if dataSource2 is None:
    print ('Could not open %s' % (commFile))
else:
    print ('Opened %s' % (commFile))
    layer2 = dataSource2.GetLayer()
   
    
sourcePts= np.empty((0,2))

for feature in layer2:
    lat=feature.GetField('lat')
    lng=feature.GetField('lng')
#    print(lat)
    sourcePts=np.vstack((sourcePts,np.array([lat,lng])))

dataSource2=None     

distance_matrix=cdist(sourcePts,targetPts,lambda u,v:distance.distance(u, v).km)
neardist=np.empty((0,2),dtype=float)

index=0
for row in range(sourcePts.shape[0]):
#    print(row)
    time.sleep(4)
    rowValues=distance_matrix[row,:]
    indices=np.where(rowValues<5)[0]
    if len(indices)==0:
        neardist=np.vstack((neardist,np.array([np.min(rowValues),np.argmin(rowValues)])))
    else:
        distArr=np.empty((0))
        startP=sourcePts[row,:]
        for i in range(len(indices)):
            
            destP=targetPts[indices[i],:]
            dist=getDistance(startP,destP)
            distArr=np.hstack((distArr,dist))
            print (str(row)+','+str(index))
            index=index+1
        minDist=np.min(distArr)
        targetIndex=indices[np.argmin(distArr)]
        neardist=np.vstack((neardist,np.array([minDist,targetIndex])))
    
standardized=(np.max(neardist[:,0])-neardist[:,0])/(np.max(neardist[:,0])-np.min(neardist[:,0]))*100

fid=open(os.path.join(outputFolder,'distance_to_nearest_parks_square_revision1.txt'),'w')
fid.write('id,dist,std,park_name\n')
for i in range(neardist.shape[0]):
    lineContent=[str(i),'%.2f'%(neardist[i,0]),'%.2f'%(standardized[i]),parkSquareList[int(neardist[i,1])]]
    fid.write(','.join(lineContent)+'\n')
fid.close()



