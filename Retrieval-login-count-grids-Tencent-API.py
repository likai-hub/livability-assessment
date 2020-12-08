# -*- coding: utf-8 -*-
"""
Created on Fri Jul 26 10:17:49 2019

@author: Likai Zhu

The code is used to retrieve the login count of Tencent-related applications at a grid size of about 1 by 1 km.

"""

import requests
import json
import pandas as pd
import time
import datetime
import os


#********************************************************************************************************************************

def get_TecentData(count=4,rank=0):   #先默认为从rank从0开始
    url='https://xingyun.map.qq.com/api/getXingyunPoints'
    locs=''
    paload={'count':count,'rank':rank}
    response=requests.post(url,data=json.dumps(paload))
    datas=response.text
    dictdatas=json.loads(datas)#dumps是将dict转化成str格式，loads是将str转化成dict格式
    time=dictdatas["time"]   #有了dict格式就可以根据关键字提取数据了，先提取时间
    print(time)
    locs=dictdatas["locs"]    #再提取locs（这个需要进一步分析提取出经纬度和定位次数）
    locss=locs.split(",")
    #newloc=[locss[i:i+3] for i in range(0,len(locss),3)]
    temp=[]          
    for i in range(int(len(locss)/3)):
        lat = locss[0+3*i]      #得到纬度
        lon = locss[1+3*i]      #得到经度
        count = locss[2+3*i]
#        temp.append([time,int(lat)/100.0,int(lon)/100.0,count])
        if(3495<int(lat)<3516 and  11822<int(lon)<11847):
            temp.append([time,int(lat)/100.0,int(lon)/100.0,count])   
    
    result=pd.DataFrame(temp)      
    result.dropna()                
    return result
    
        
#********************************************************************************************************************************
outputFolder=r'G:\geography_presentation\population\tencent_position'
if not os.path.exists(outputFolder):
    os.makedirs(outputFolder)

#endTime=datetime.datetime.now()+datetime.timedelta(hours=1)
endTime=datetime.datetime(2019,7,26,23,30)
startTime=datetime.datetime(2019,7,26,21,30)

index=1
while True:
    if datetime.datetime.now()<startTime:
        continue
    startt=datetime.datetime.now()
    for i in range(4):
        res=get_TecentData(4,i)
        if res.empty:
            print('Returns from rank'+str(i)+' is empty')
            continue
        else:
            if index==1:
                res.columns = ['time', 'lat', 'lon','count']
                res.to_csv(os.path.join(outputFolder,'TecentData.txt'),mode='a',index = False)
                index=index+1
            else:
                # Don't save the header to csv file for more than one run.
                res.to_csv(os.path.join(outputFolder,'TecentData.txt'),mode='a',index = False,header=False)
        
    endt=datetime.datetime.now()
    tdelta=(endt-startt).seconds
    time.sleep(5*60-tdelta)
    if endt>endTime:
        break
    

    
    