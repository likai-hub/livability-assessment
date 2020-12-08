# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 11:07:25 2019

@author: Likai Zhu
This code is gapfill the missing observations within the MODIS daily land surface temperatures. 

Reference:40.	Li, X.; Zhou, Y.; Asrar, G.R.; Zhu, Z. Creating a seamless 1 km resolution daily land surface temperature dataset for urban and surrounding areas in the conterminous United States. 
Remote Sens. Environ. 2018, 206, 84–97.

"""

import gdal
from gdalconst import *
import numpy as np
import os
import glob
import math
from sklearn.linear_model import LinearRegression
import datetime
from scipy import interpolate

#*******************************************************************************
def Array2GTiff(inputArr,outFilePath,geoTrans,proj,nodataValue,dataType='float'):
    cols = inputArr.shape[1]
    rows = inputArr.shape[0]
    driver = gdal.GetDriverByName('GTiff')
    if dataType=='float':
        outRaster = driver.Create(outFilePath, cols, rows, 1, gdal.GDT_Float32)
#    elif dataType=='int8':
#        outRaster = driver.Create(outFilePath, cols, rows, 1, gdal.GDT_Byte)
    else:
        outRaster = driver.Create(outFilePath, cols, rows, 1, gdal.GDT_Int16)
    outRaster.SetGeoTransform(geoTrans)
    outRaster.SetProjection(proj)
    outband = outRaster.GetRasterBand(1)
    outband.WriteArray(inputArr)
    outband.SetNoDataValue(nodataValue)
    outRaster=None
#*******************************************************************************

# linyi boundary extent(xmin,xmax,ymin,ymax)
ext=[10731989.405,10807745.056,3875403.015,3930711.626]
inputFolder=r'G:\geography_presentation\modis_lst\raw'
outputFolder=r'G:\geography_presentation\modis_lst\step1'
if not os.path.exists(outputFolder):
    os.makedirs(outputFolder)
    

tempf=glob.glob(inputFolder+'\\mod\\*.hdf')[0]

ds=gdal.Open(gdal.Open(tempf).GetSubDatasets()[0][0])

rows=ds.RasterYSize
cols=ds.RasterXSize
proj=ds.GetProjection()

geoTrans=ds.GetGeoTransform()

offsetX=int((ext[0]-geoTrans[0])/geoTrans[1])
offsetY=int((ext[3]-geoTrans[3])/geoTrans[5])
newOrigX=geoTrans[0]+geoTrans[1]*offsetX
newOrigY=geoTrans[3]+geoTrans[5]*offsetY
geoTransList=list(geoTrans)
geoTransList[0]=newOrigX
geoTransList[3]=newOrigY
newGeoTrans=tuple(geoTransList)

rowNum=int(math.ceil(((ext[2]-ext[3])/geoTrans[5])))
colNum=int(math.ceil(((ext[1]-ext[0])/geoTrans[1])))

ds=None

lstArr1=np.empty((0,rowNum,colNum))
lstArr2=np.empty((0,rowNum,colNum))
lstArr3=np.empty((0,rowNum,colNum))
lstArr4=np.empty((0,rowNum,colNum))
for d in range(1,366):
    modf=glob.glob(inputFolder+'\\mod\\*A2018'+str(d).zfill(3)+'*.hdf')[0]
    mydf=glob.glob(inputFolder+'\\myd\\*A2018'+str(d).zfill(3)+'*.hdf')[0]
    # MOD LST
    lst1=gdal.Open(gdal.Open(modf).GetSubDatasets()[0][0]).ReadAsArray(offsetX,offsetY,colNum,rowNum)
    qa1=gdal.Open(gdal.Open(modf).GetSubDatasets()[1][0]).ReadAsArray(offsetX,offsetY,colNum,rowNum)
    angle1=gdal.Open(gdal.Open(modf).GetSubDatasets()[3][0]).ReadAsArray(offsetX,offsetY,colNum,rowNum)
    mask=(qa1&0)+(qa1&1)
    lst1[mask==0]=0
#    lst1[np.abs(angle1-65)>45]=0
    lst1[angle1==255]=0
    lstArr1=np.concatenate((lstArr1,lst1.reshape(1,rowNum,colNum)),axis=0)
        
    lst3=gdal.Open(gdal.Open(modf).GetSubDatasets()[4][0]).ReadAsArray(offsetX,offsetY,colNum,rowNum)
    qa3=gdal.Open(gdal.Open(modf).GetSubDatasets()[5][0]).ReadAsArray(offsetX,offsetY,colNum,rowNum)
    angle3=gdal.Open(gdal.Open(modf).GetSubDatasets()[7][0]).ReadAsArray(offsetX,offsetY,colNum,rowNum)
    mask=(qa3&0)+(qa3&1)
    lst3[mask==0]=0
#    lst3[np.abs(angle3-65)>45]=0
    lst3[angle3==255]=0
    lstArr3=np.concatenate((lstArr3,lst3.reshape(1,rowNum,colNum)),axis=0)
    
    #MYD LST
    lst2=gdal.Open(gdal.Open(mydf).GetSubDatasets()[0][0]).ReadAsArray(offsetX,offsetY,colNum,rowNum)
    qa2=gdal.Open(gdal.Open(mydf).GetSubDatasets()[1][0]).ReadAsArray(offsetX,offsetY,colNum,rowNum)
    angle2=gdal.Open(gdal.Open(mydf).GetSubDatasets()[3][0]).ReadAsArray(offsetX,offsetY,colNum,rowNum)
    mask=(qa2&0)+(qa2&1)
    lst2[mask==0]=0
#    lst2[np.abs(angle2-65)>45]=0
    lst2[angle2==255]=0
    lstArr2=np.concatenate((lstArr2,lst2.reshape(1,rowNum,colNum)),axis=0)
    
    lst4=gdal.Open(gdal.Open(mydf).GetSubDatasets()[4][0]).ReadAsArray(offsetX,offsetY,colNum,rowNum)
    qa4=gdal.Open(gdal.Open(mydf).GetSubDatasets()[5][0]).ReadAsArray(offsetX,offsetY,colNum,rowNum)
    angle4=gdal.Open(gdal.Open(mydf).GetSubDatasets()[7][0]).ReadAsArray(offsetX,offsetY,colNum,rowNum)    
    
    mask=(qa4&0)+(qa4&1)
    lst4[mask==0]=0
#    lst4[np.abs(angle4-65)>45]=0 
    lst4[angle4==255]=0
    lstArr4=np.concatenate((lstArr4,lst4.reshape(1,rowNum,colNum)),axis=0)
    

lstArr1=lstArr1*0.02
lstArr2=lstArr2*0.02  
lstArr3=lstArr3*0.02
lstArr4=lstArr4*0.02

# Linear regression of T2 against T1
processArr2=np.zeros((365,rowNum,colNum))

for r in range(lstArr1.shape[1]):
    for c in range(lstArr1.shape[2]):
        y=lstArr2[:,r,c]
        x=lstArr1[:,r,c]
        newy=y[(y>0) & (x>0)]
        newx=x[(y>0) & (x>0)]
        y_to_pred=x[(y<=0) & (x>0)]
        if len(newy)<10 or len(y_to_pred)==0:
            print (r,c)
            processArr2[:,r,c]=lstArr2[:,r,c]
        else:
            reg=LinearRegression().fit(newx.reshape(-1,1),newy)
            preds=reg.predict(y_to_pred.reshape(-1,1))
            y[(y<=0) & (x>0)]=preds
            processArr2[:,r,c]=y
            
# Shift method T3>T2

startT=datetime.datetime(2018,1,1)
endT=datetime.datetime(2018,12,31)
monArr=np.empty((0))
dayArr=np.empty((0))
for df in range((endT-startT).days+1):
    curD=startT+datetime.timedelta(days=df)
    monArr=np.hstack((monArr,curD.month))
    dayArr=np.hstack((dayArr,int(curD.strftime('%j'))))
    
    
monthx=np.array([int(datetime.datetime(2018,1,1).strftime('%j'))])    

#monthx=np.empty((0))
for m in range(1,13):
    monthx=np.hstack((monthx,int(datetime.datetime(2018,m,15).strftime('%j'))))

monthx=np.hstack((monthx,int(datetime.datetime(2018,12,31).strftime('%j'))))

                
for r in range(lstArr2.shape[1]):
    for c in range(lstArr2.shape[2]): 
        
        y=lstArr2[:,r,c]
        x=lstArr3[:,r,c]
        monDiff=np.ones(12)*(-999)
        for m in range(1,13):
            subsety=y[monArr==m]
            subsetx=x[monArr==m]
            if np.sum((subsety>0) & (subsetx>0))==0:
                continue
            else:     
                monDiff[m-1]=np.mean(subsety[(subsety>0) & (subsetx>0)]-subsetx[(subsety>0) & (subsetx>0)])
        monDiff=np.hstack((monDiff[0],monDiff,monDiff[-1]))
        subset=monDiff[monDiff!=-999]
        print(subset)
        submonthx=monthx[monDiff!=-999]
        if len(subset)<6:
            continue
        else:
            f=interpolate.interp1d(submonthx,subset,fill_value="extrapolate")
            ypred=f(dayArr)
        ypred[ypred<0]=0
        processedVals=processArr2[:,r,c]
        processedVals[(processedVals<=0) & (x>0)]=x[(processedVals<=0) & (x>0)]+ypred[(processedVals<=0) & (x>0)]
        processArr2[:,r,c]=processedVals


# shift T4>>T2

for r in range(lstArr2.shape[1]):
    for c in range(lstArr2.shape[2]): 
        
        y=lstArr2[:,r,c]
        x=lstArr4[:,r,c]
        monDiff=np.ones(12)*(-999)
        for m in range(1,13):
            subsety=y[monArr==m]
            subsetx=x[monArr==m]
            if np.sum((subsety>0) & (subsetx>0))==0:
                continue
            else:     
                monDiff[m-1]=np.mean(subsety[(subsety>0) & (subsetx>0)]-subsetx[(subsety>0) & (subsetx>0)])
        monDiff=np.hstack((monDiff[0],monDiff,monDiff[-1]))
        subset=monDiff[monDiff!=-999]
        print subset
        submonthx=monthx[monDiff!=-999]
        if len(subset)<6:
            continue
        else:
            f=interpolate.interp1d(submonthx,subset,fill_value="extrapolate")
            ypred=f(dayArr)
        ypred[ypred<0]=0
        processedVals=processArr2[:,r,c]
        processedVals[(processedVals<=0) & (x>0)]=x[(processedVals<=0) & (x>0)]+ypred[(processedVals<=0) & (x>0)]
        processArr2[:,r,c]=processedVals        
         

for d in range(1,366):
    Array2GTiff(processArr2[d-1],os.path.join(outputFolder,'lst'+str(d).zfill(3)+'.tif'),newGeoTrans,proj,0)
    print('lst'+str(d).zfill(3)+'.tif')

    
    
    
        
        
     
        
        
        
        

    
    
    
    
    
    
    
    
    
    
    