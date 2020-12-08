# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 08:31:39 2019

@author: Likai Zhu

The code is to calcualte the travel distance between origin and destination based on BAIDU API, and then to store the outputs to a text file

Here we take the calcualtion of community-school travel distance as an example.

"""
# Likai's AK
# ak='v9ntzrdoClxSU4uMpLlk3DrLeDvhoPGH'
# Lei's AK
# ak='ohoiaw1tSqOIHziQUXWB9rp752GCqHVn'
# Wenxue's AK
# ak='cxSpeloGXq3mHcT3yyGVcHG5QSelBUc8'

#import geopy
import os
import ogr
import numpy as np
from scipy.spatial.distance import cdist
from geopy import distance
import urllib2
import json
import time

#********************************************************************************************************************************            
def getDistance(origin,destination):
    # origin and destination should have a dimension of [2,],array([  34.98032273,  118.28843478])
    origin=','.join(map(lambda x:'%6f'%x,origin))
    destination=','.join(map(lambda x:'%6f'%x,destination))
    # url='http://api.map.baidu.com/direction/v2/riding?'
    url='http://api.map.baidu.com/routematrix/v2/driving?'
    output = 'json'
    # Likai
#    ak = 'v9ntzrdoClxSU4uMpLlk3DrLeDvhoPGH'
    # Wenxue Tang
#    ak = 'cxSpeloGXq3mHcT3yyGVcHG5QSelBUc8'
    # Hui
    ak='mznuxpzGx7HUx6QLhHgq6P1HsBjdkPHO'
    coordType='wgs84'
    uri = url + 'origins=' + origin + '&destinations=' + destination + '&output=' + output + '&coord_type='+coordType+'&ak=' + ak
    print(uri)
    req = urllib2.urlopen(uri)
    res = req.read()
    temp = json.loads(res)            

#    print(temp)
    distance = temp['result'][0]['distance']['value']/1000.0 # 那个0是因为它返回的routes是一个list，所以索引0就是第一条路线
    req.close()
#    duration = temp['result']['routes'][0]['duration']
    # print '距离%.2f千米，骑车耗时%d分钟' % (float(distance) / 1000, round(int(duration) / 60))
    return distance       

#********************************************************************************************************************************
    
outputFolder=r'G:\geography_presentation\indices_system'
if not os.path.exists(outputFolder):
    os.makedirs(outputFolder)


primSchFile=r'G:\geography_presentation\schools\primary_schools.shp'
highSchFile=r'G:\geography_presentation\schools\high_schools.shp'
commFile=r'G:\geography_presentation\communities\digitalized\communities_digitalized.shp'

# Primary school
# Get driver by name
driver=ogr.GetDriverByName('ESRI Shapefile')

# open primary school shapefile   (target file) 
dataSource1 = driver.Open(primSchFile, 0)
if dataSource1 is None:
    print 'Could not open %s' % (primSchFile)
else:
    print 'Opened %s' % (primSchFile)
    layer = dataSource1.GetLayer()
    
targetPts1=np.empty((0,2))
primList=[]
#fid=open(r'G:\geography_presentation\test\test.txt','w')
for feature in layer:
    lat=feature.GetField('lat')
    lng=feature.GetField('lng')
#    print(lat)
    targetPts1=np.vstack((targetPts1,np.array([lat,lng])))
    name=feature.GetField('name')
#    print(name)
#    fid.write(name+'\n')
    primList.append(name)
#fid.close()

dataSource1=None

# High school

# open high school shapefile   (target file) 
dataSource1 = driver.Open(highSchFile, 0)
if dataSource1 is None:
    print 'Could not open %s' % (highSchFile)
else:
    print 'Opened %s' % (highSchFile)
    layer = dataSource1.GetLayer()
    
targetPts2=np.empty((0,2))
highList=[]
#fid=open(r'G:\geography_presentation\test\test.txt','w')
for feature in layer:
    lat=feature.GetField('lat')
    lng=feature.GetField('lng')
#    print(lat)
    targetPts2=np.vstack((targetPts2,np.array([lat,lng])))
    name=feature.GetField('name')
#    print(name)
#    fid.write(name+'\n')
    highList.append(name)
#fid.close()

# open community shapefile (source file)
dataSource2 = driver.Open(commFile, 0)
if dataSource2 is None:
    print 'Could not open %s' % (commFile)
else:
    print 'Opened %s' % (commFile)
    layer2 = dataSource2.GetLayer()
   
    
sourcePts= np.empty((0,2))

for feature in layer2:
    lat=feature.GetField('lat')
    lng=feature.GetField('lng')
#    print(lat)
    sourcePts=np.vstack((sourcePts,np.array([lat,lng])))

dataSource2=None     

    
# Select the pairs of school and community whose distance is within 5 km to further calculate their travel distance
# This will save the times of computation which BAIDU API has put limits on.

distance_matrix=cdist(sourcePts,targetPts1,lambda u,v:distance.distance(u, v).km)


neardist1=np.empty((0,2),dtype=float)

index=0
for row in range(distance_matrix.shape[0]):
    time.sleep(3)
#    print(row)
    rowValues=distance_matrix[row,:]
    indices=np.where(rowValues<3)[0]
    if len(indices)==0:
        neardist1=np.vstack((neardist1,np.array([np.min(rowValues),np.argmin(rowValues)])))
    else:
        distArr=np.empty((0))
        startP=sourcePts[row,:]
        for i in range(len(indices)):
            
            destP=targetPts1[indices[i],:]
            dist=getDistance(startP,destP)
            distArr=np.hstack((distArr,dist))
            print str(row)+','+str(index)
            index=index+1
        minDist=np.min(distArr)
        targetIndex=indices[np.argmin(distArr)]
        neardist1=np.vstack((neardist1,np.array([minDist,targetIndex])))

# standardize the calculated distances (excluding the value equal to 999)
#standardized1=neardist1[:,0]
#subset=standardized1[standardized1!=999]
#standardized1[standardized1!=999]=(np.max(subset)-subset)/(np.max(subset)-np.min(subset))*100 
#standardized1[standardized1==999]=0
standardized1=(np.max(neardist1[:,0])-neardist1[:,0])/(np.max(neardist1[:,0])-np.min(neardist1[:,0]))*100   
# Select the points that fall within 5km of the source point

distance_matrix=cdist(sourcePts,targetPts2,lambda u,v:distance.distance(u, v).km)


neardist2=np.empty((0,2),dtype=float)


for row in range(distance_matrix.shape[0]):
    time.sleep(4)
#    print(row)
    rowValues=distance_matrix[row,:]
    indices=np.where(rowValues<5)[0]
    if len(indices)==0:
        neardist2=np.vstack((neardist2,np.array([np.min(rowValues),np.argmin(rowValues)])))
    else:
        distArr=np.empty((0))
        startP=sourcePts[row,:]
        for i in range(len(indices)):
            
            destP=targetPts2[indices[i],:]
            dist=getDistance(startP,destP)
            distArr=np.hstack((distArr,dist))
            print str(row)+','+str(index)
            index=index+1
        minDist=np.min(distArr)
        targetIndex=indices[np.argmin(distArr)]
        neardist2=np.vstack((neardist2,np.array([minDist,targetIndex])))

# standardize the calculated distances (excluding the value equal to 999)
#standardized2=neardist2[:,0]
#subset=standardized2[standardized2!=999]
#standardized2[standardized2!=999]=(np.max(subset)-subset)/(np.max(subset)-np.min(subset))*100 
#standardized2[standardized2==999]=0
standardized2=(np.max(neardist2[:,0])-neardist2[:,0])/(np.max(neardist2[:,0])-np.min(neardist2[:,0]))*100   
      
# average standardized values
meanStd=np.mean(np.vstack((standardized1,standardized2)),axis=0)
# average distance
meanDist=np.mean(np.vstack((neardist1[:,0],neardist2[:,0])),axis=0)
# 
meanstd2=(np.max(meanDist)-meanDist)/(np.max(meanDist)-np.min(meanDist))*100

fid=open(os.path.join(outputFolder,'distance_to_nearest_schools.txt'),'w')
fid.write('id,prim_dist,prim_std,prim_name,high_dist,high_std,high_name,mean_std,mean_dist,mean_std2\n')
for i in range(neardist1.shape[0]):
    lineContent=[str(i),'%.2f'%(neardist1[i,0]),'%.2f'%(standardized1[i]),primList[int(neardist1[i,1])],'%.2f'%(neardist2[i,0]),'%.2f'%(standardized2[i]),highList[int(neardist2[i,1])],'%.2f'%(meanStd[i]),'%.2f'%(meanDist[i]),'%.2f'%(meanstd2[i])]
    fid.write(','.join(lineContent)+'\n')
fid.close()


