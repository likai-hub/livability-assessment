# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 10:17:10 2019

@author: Administrator

The code is to retrieve the traffic status of each grid in fishnet for every specific period, and then to store the ouputs into text file.

"""

import json
import urllib2
import ogr
import os
import numpy as np
import datetime
import time

# Likai's ak
#Lei's AK
# Wenxue's AK
# Hui's AK
# Chunyan's AK
akPool=['WcZhfkW5X2qL6yQ4lCZGEdTaotZ8jfqR','ohoiaw1tSqOIHziQUXWB9rp752GCqHVn','mznuxpzGx7HUx6QLhHgq6P1HsBjdkPHO','v9ntzrdoClxSU4uMpLlk3DrLeDvhoPGH','cxSpeloGXq3mHcT3yyGVcHG5QSelBUc8']
#********************************************************************************************************************************            
def getTrafficStatus(rectInfo,ak):
    # rectInfo is latitude and longitude values of the lowleft and upright corners of search rectangle
    # format: LL lat,LL lng;UR lat,UR lng
    

    url='http://api.map.baidu.com/traffic/v1/bound?'
#    ak = 'v9ntzrdoClxSU4uMpLlk3DrLeDvhoPGH'
    # Hui
#    ak='mznuxpzGx7HUx6QLhHgq6P1HsBjdkPHO'    
    coordType='wgs84'
    uri = url + 'bounds='+ rectInfo+'&coord_type_input='+coordType+'&coord_type_output=gcj02'+'&ak=' + ak
    print(uri)
    req = urllib2.urlopen(uri)
    res = req.read()
    temp = json.loads(res)      
    req.close()
    dkeys=temp.keys()
    if 'evaluation' in dkeys and ('road_traffic' in dkeys):      
        overallStatus=temp['evaluation']['status']
        roadNum=len(temp['road_traffic'])
        
        if roadNum==0:
            output=dict(overall=overallStatus,specific=[0],roadnames=['none'])
        else:
            statusArr=np.empty((0),dtype=int)
            roads=[]
            for i in range(roadNum):
                roads.append(temp['road_traffic'][i]['road_name'])
                if len(temp['road_traffic'][i])==1:
                    statusArr=np.hstack((statusArr,1))
                      
                else:
                    statusArr=np.hstack((statusArr,temp['road_traffic'][i]['congestion_sections'][0]['status']))
            output=dict(overall=overallStatus,specific=statusArr,roadnames=roads)
    else:
        output=dict(overall=0,specific=[0],roadnames=['none'])
    return output

#    print(temp)
      
#********************************************************************************************************************************

tod=datetime.datetime.today()
if tod.hour<12:
    subsetName=tod.strftime('%Y%m%d')+'AM'
else:
    subsetName=tod.strftime('%Y%m%d')+'PM'
outputFolder=r'G:\geography_presentation\traffic\rawdata\\'+subsetName
if not os.path.exists(outputFolder):
    os.makedirs(outputFolder)

gridFile=r'G:\geography_presentation\communities\fishnet_1km_central_urban.shp'

# Get driver by name
driver=ogr.GetDriverByName('ESRI Shapefile')

# open hospital shapefile   (target file) 
dataSource = driver.Open(gridFile, 0)
if dataSource is None:
    print 'Could not open %s' % (gridFile)
else:
    print 'Opened %s' % (gridFile)
    layer = dataSource.GetLayer()
    
rectBounds=[]
#targetPts=np.empty((0,2))
#mallList=[]
#hospList=[]
#fid=open(r'G:\geography_presentation\test\test.txt','w')
for feature in layer:
    xmin=feature.GetField('xmin')
    xmax=feature.GetField('xmax')
    ymin=feature.GetField('ymin')
    ymax=feature.GetField('ymax')
    rectBounds.append('%.6f'%(ymin)+','+'%.6f'%(xmin)+';'+'%.6f'%(ymax)+','+'%.6f'%(xmax))    
dataSource=None

# create a dictionary to save traffic description for the whole grid
# create a dictionary to save traffic status of each raads within each grid
gridStatus={}
roadStatus={}
roadName={}
extractedPeriod=[]
#endTime=datetime.datetime.now()+datetime.timedelta(hours=2.5)
#endTime=datetime.datetime.now()+datetime.timedelta(minutes=20)
endTime=datetime.datetime(2019,7,30,7,0)
startTime=datetime.datetime(2019,7,30,9,30)
# monitoring how many times are used to extract
runtimes=0
index=0
while True:
    if datetime.datetime.now()<startTime:
        continue
    if index==0:
        index=index+1
        startt=datetime.datetime.now()
        extractedPeriod.append(str(startt.month).zfill(2)+str(startt.day).zfill(2)+str(startt.hour).zfill(2)+str(startt.minute).zfill(2))
        print(str(startt.month).zfill(2)+str(startt.day).zfill(2)+str(startt.hour).zfill(2)+str(startt.minute).zfill(2))
        for i in range(len(rectBounds)):
            runtimes=runtimes+1
            rectInfo=rectBounds[i]
            res_traffic=getTrafficStatus(rectInfo,akPool[0])
            gridStatus['grid'+str(i).zfill(3)]=res_traffic['overall']
            roadStatus['grid'+str(i).zfill(3)]=res_traffic['specific']
            roadName['grid'+str(i).zfill(3)]=res_traffic['roadnames']
        endt=datetime.datetime.now()
        tdelta=(endt-startt).seconds
        
    else:
        time.sleep(15*60-tdelta)
        
        startt=datetime.datetime.now()
        extractedPeriod.append(str(startt.month).zfill(2)+str(startt.day).zfill(2)+str(startt.hour).zfill(2)+str(startt.minute).zfill(2))
        print(str(startt.month).zfill(2)+str(startt.day).zfill(2)+str(startt.hour).zfill(2)+str(startt.minute).zfill(2))
        for i in range(len(rectBounds)):
            runtimes=runtimes+1
#            if runtimes>3000:
#                break
            rectInfo=rectBounds[i]
            res_traffic=getTrafficStatus(rectInfo,akPool[int(runtimes/1990)])
            gridStatus['grid'+str(i).zfill(3)]=np.hstack((gridStatus['grid'+str(i).zfill(3)],res_traffic['overall']))
            if len(res_traffic['specific'])!=len(roadName['grid'+str(i).zfill(3)]):
                roadStatus['grid'+str(i).zfill(3)]=np.vstack((roadStatus['grid'+str(i).zfill(3)],np.zeros((len(roadName['grid'+str(i).zfill(3)]),))))
            else:
                roadStatus['grid'+str(i).zfill(3)]=np.vstack((roadStatus['grid'+str(i).zfill(3)],res_traffic['specific']))
#            roadName['grid'+str(i).zfill(3)]=res_traffic['roadnames']
        endt=datetime.datetime.now()
        tdelta=(endt-startt).seconds 
        if datetime.datetime.now()>endTime:
            break

fid=open(os.path.join(outputFolder,'overall_status_grids.txt'),'w')
headline=['id']+extractedPeriod+['prob\n']
fid.write(','.join(headline))

for i in range(len(rectBounds)):
    statusArr=gridStatus['grid'+str(i).zfill(3)]
    probVal=len(statusArr[statusArr>=3])*1.0/len(statusArr)*100
    linec=[str(i)]+map(lambda x:str(x),statusArr)+['%.2f'%(probVal)]
    fid.write(','.join(linec)+'\n')
fid.close()

newHeadline=','.join(extractedPeriod)
for i in range(len(rectBounds)):
    fid=open(os.path.join(outputFolder,'traffic_status_grids'+str(i).zfill(3)+'.txt'),'w')
    fid.write(newHeadline+'\n')
    statusArr=np.transpose(roadStatus['grid'+str(i).zfill(3)])
    for j in range(statusArr.shape[0]):
        fid.write(','.join(map(lambda x:str(x),statusArr[j,:]))+'\n')
    fid.close()
    print('grid'+str(i).zfill(3))
    
fid=open(os.path.join(outputFolder,'roadnames_grids.txt'),'w')

for i in range(len(rectBounds)):
    roads=roadName['grid'+str(i).zfill(3)]
    linec=str(i)+','+(','.join(roads))
    linec=linec.encode('utf-8')
    fid.write(linec+'\n')
fid.close()

print runtimes


    
    
