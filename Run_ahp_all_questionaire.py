# -*- coding: utf-8 -*-
"""
Created on Thu Aug 15 11:02:37 2019

@author: Administrator
"""

# AHP in python

import sys
sys.path.insert(0, r"G:\geography_presentation\code\ahp")

from ahpy import Compare
from ahpy import Compose
import numpy as np
import os

inputFolder=r'G:\geography_presentation\ahp\questionaire'
outputFolder=r'G:\geography_presentation\ahp\process_results'
if not os.path.exists(outputFolder):
    os.makedirs(outputFolder)

fileList=[f for f in os.listdir(inputFolder) if f.endswith('.csv')]

health=['thermal','pm25']
comfort=['green','built','pop','dpark','droad']
facility=['dhosp','dschool','dshopping','dmarket','drestaurant']
convenience=['dbus','dstation','dcenter','traffic']

livability=['health','comfort','facility','convenience']



# 
fid1=open(os.path.join(outputFolder,'separate_weights.txt'),'w')
fid2=open(os.path.join(outputFolder,'weights.txt'),'w')
fid3=open(os.path.join(outputFolder,'consistence_ratio.txt'),'w')
ind=1
for f in fileList:
    print ('Start to run AHP for file: '+f)
    fid=open(os.path.join(inputFolder,f),'r')
    index=0
    mat1=np.empty((0,2))
    mat2=np.empty((0,5))
    mat3=np.empty((0,5))
    mat4=np.empty((0,4))
    mat5=np.empty((0,4))
    for line in fid.readlines():
        if "Mat" in line or 'mat' in line or line.startswith(','):
            index=index+1
            continue
        else:
            linec=map(lambda x:float(x),line.rstrip(',\n').split(','))
            if index==1:
                mat1=np.vstack((mat1,np.array(linec)))
            if index==2:
                mat2=np.vstack((mat2,np.array(linec)))
            if index==3:
                mat3=np.vstack((mat3,np.array(linec)))
            if index==4:
                mat4=np.vstack((mat4,np.array(linec)))            
            if index==5:
                mat5=np.vstack((mat5,np.array(linec)))   
    fid.close()
    
    mat1[mat1==0.333]=1/3.0
    mat1[mat1==0.143]=1/7.0
    mat1=np.transpose(np.matrix(mat1))
    healthRes=Compare('health',mat1,health,3,random_index='Saaty')
    
    mat2[mat2==0.333]=1/3.0
    mat2[mat2==0.143]=1/7.0 
    mat2=np.transpose(np.matrix(mat2))
    comfortRes=Compare('comfort',mat2,comfort,3,random_index='Saaty')
    
    mat3[mat3==0.333]=1/3.0
    mat3[mat3==0.143]=1/7.0 
    mat3=np.transpose(np.matrix(mat3))
    facilityRes=Compare('facility',mat3,facility,3,random_index='Saaty')
    
    mat4[mat4==0.333]=1/3.0
    mat4[mat4==0.143]=1/7.0 
    mat4=np.transpose(np.matrix(mat4))
    convenienceRes=Compare('convenience',mat4,convenience,3,random_index='Saaty')

    mat5[mat5==0.333]=1/3.0
    mat5[mat5==0.143]=1/7.0 
    mat5=np.transpose(np.matrix(mat5))
    livabilityRes=Compare('comLivability',mat5,livability,3,random_index='Saaty')
    
    comp_matrices = [healthRes,comfortRes,facilityRes,convenienceRes]
    composed=Compose('Goal', livabilityRes, comp_matrices)
    if ind==1:
        headLine1=['qcode']+healthRes.weights['health'].keys()+comfortRes.weights['comfort'].keys()+facilityRes.weights['facility'].keys()+convenienceRes.weights['convenience'].keys()+livabilityRes.weights['comLivability'].keys()
        headLine1=','.join(headLine1)+'\n'
        fid1.write(headLine1)
        linec1=healthRes.weights['health'].values()+comfortRes.weights['comfort'].values()+facilityRes.weights['facility'].values()+convenienceRes.weights['convenience'].values()+livabilityRes.weights['comLivability'].values()
        linec1=f+','+','.join(map(lambda x: str(x),linec1))+'\n'
        fid1.write(linec1)
        headLine2=['qcode']+composed.weights['Goal'].keys()
        headLine2=','.join(headLine2)+'\n'
        fid2.write(headLine2)
        
        linec2=composed.weights['Goal'].values()
        linec2=f+','+','.join(map(lambda x: str(x),linec2))+'\n'
        fid2.write(linec2)
        
        
        headLine3=['qcode','health','comfort','facility','convenience']
        headLine3=','.join(headLine3)+'\n'
        fid3.write(headLine3)
        linec3=[healthRes.consistency_ratio,comfortRes.consistency_ratio,facilityRes.consistency_ratio,convenienceRes.consistency_ratio]
        linec3=f+','+','.join(map(lambda x: str(x),linec3))+'\n'
        
        fid3.write(linec3)
        
        ind=ind+1
    else:
#        headLine1=['qcode']+healthRes.weights['health'].keys()+comfortRes.weights['comfort'].keys()+facilityRes.weights['facility'].keys()+convenienceRes.weights['convenience'].keys()+livabilityRes.weights['comLivability'].keys()
#        headLine1=','.join(headLine1)+'\n'
#        fid1.write(headLine1)
        linec1=healthRes.weights['health'].values()+comfortRes.weights['comfort'].values()+facilityRes.weights['facility'].values()+convenienceRes.weights['convenience'].values()+livabilityRes.weights['comLivability'].values()
        linec1=f+','+','.join(map(lambda x: str(x),linec1))+'\n'
        fid1.write(linec1)
#        headLine2=['qcode']+composed.weights['Goal'].keys()
#        headLine2=','.join(headLine2)+'\n'
#        fid2.write(headLine2)
        
        linec2=composed.weights['Goal'].values()
        linec2=f+','+','.join(map(lambda x: str(x),linec2))+'\n'
        fid2.write(linec2)
        
        
#        headLine3=['qcode','health','comfort','facility','convenience']
#        headLine3=','.join(headLine3)+'\n'
#        fid3.write(headLine3)
        linec3=[healthRes.consistency_ratio,comfortRes.consistency_ratio,facilityRes.consistency_ratio,convenienceRes.consistency_ratio]
        linec3=f+','+','.join(map(lambda x: str(x),linec3))+'\n'
        
        fid3.write(linec3)
        
        ind=ind+1

fid1.close()
fid2.close()
fid3.close()
    
    
    
    
            
    
    
    




