# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 14:09:13 2019
@author: Likai Zhu
The code is to retrieve specific type of Points of Interest (POIs) from BAIDU API by grid defined by fishnet, and to store the retrievals in the text file.
 

"""

import sys
import requests  
ty=sys.getfilesystemencoding()
import time
#import xlwt
import os
import math






#BAIDU API, search for POIs through inputing the extent of latitude and longitude
#http://lbsyun.baidu.com/index.php?title=lbscloud/poitags 该网址为POI类型，即API链接中的query的类型
base_url='http://api.map.baidu.com/place/v2/search?query={}&bounds={}&page_size=20&page_num={}&output=json&ak=v9ntzrdoClxSU4uMpLlk3DrLeDvhoPGH'

#*******************************************************************************************************
# tranform baidu coordinates to WGS84
x_pi = 3.14159265358979324 * 3000.0 / 180.0
pi = 3.1415926535897932384626  # π
a = 6378245.0  # 长半轴
ee = 0.00669342162296594323  # 偏心率平方

def bd09_to_gcj02(bd_lon, bd_lat):
    """
    百度坐标系(BD-09)转火星坐标系(GCJ-02)
    百度——>谷歌、高德
    :param bd_lat:百度坐标纬度
    :param bd_lon:百度坐标经度
    :return:转换后的坐标列表形式
    """
    x = bd_lon - 0.0065
    y = bd_lat - 0.006
    z = math.sqrt(x * x + y * y) - 0.00002 * math.sin(y * x_pi)
    theta = math.atan2(y, x) - 0.000003 * math.cos(x * x_pi)
    gg_lng = z * math.cos(theta)
    gg_lat = z * math.sin(theta)
    return [gg_lng, gg_lat]

def gcj02_to_wgs84(lng, lat):
    """
    GCJ02(火星坐标系)转GPS84
    :param lng:火星坐标系的经度
    :param lat:火星坐标系纬度
    :return:
    """
    if out_of_china(lng, lat):
        return [lng, lat]
    dlat = _transformlat(lng - 105.0, lat - 35.0)
    dlng = _transformlng(lng - 105.0, lat - 35.0)
    radlat = lat / 180.0 * pi
    magic = math.sin(radlat)
    magic = 1 - ee * magic * magic
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * pi)
    dlng = (dlng * 180.0) / (a / sqrtmagic * math.cos(radlat) * pi)
    mglat = lat + dlat
    mglng = lng + dlng
    return [lng * 2 - mglng, lat * 2 - mglat]

def bd09_to_wgs84(bd_lon, bd_lat):
    lon, lat = bd09_to_gcj02(bd_lon, bd_lat)
    return gcj02_to_wgs84(lon, lat)

def _transformlat(lng, lat):
    ret = -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * lat * lat + \
          0.1 * lng * lat + 0.2 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 *
            math.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lat * pi) + 40.0 *
            math.sin(lat / 3.0 * pi)) * 2.0 / 3.0
    ret += (160.0 * math.sin(lat / 12.0 * pi) + 320 *
            math.sin(lat * pi / 30.0)) * 2.0 / 3.0
    return ret


def _transformlng(lng, lat):
    ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + \
          0.1 * lng * lat + 0.1 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 *
            math.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lng * pi) + 40.0 *
            math.sin(lng / 3.0 * pi)) * 2.0 / 3.0
    ret += (150.0 * math.sin(lng / 12.0 * pi) + 300.0 *
            math.sin(lng / 30.0 * pi)) * 2.0 / 3.0
    return ret


def out_of_china(lng, lat):
    """
    判断是否在国内，不在国内不做偏移
    :param lng:
    :param lat:
    :return:
    """
    return not (lng > 73.66 and lng < 135.05 and lat > 3.86 and lat < 53.55)
#*******************************************************************************************************

#1.获取每个格网起始URL
def get_begin_url(keyword,page=0):
    with open(outputGridBound, 'r') as f:
        #网格矩形范围内每一行是一个小方格的经纬度范围，保存顺序为mini longitude, maxi longitude, mini latitude, maxi latitude
        f.readline()
        lines=f.readlines()
#        index=1
        for line in lines:
#            index=index+1
#            if index>20:
#                break
            line=line.rstrip()
            w1 = float(line.split(',')[2])
            j1 = float(line.split(',')[0])
            w2 = float(line.split(',')[3])
            j2 = float(line.split(',')[1])
            url2 = base_url.format(keyword, str(w1) + ',' + str(j1) + ',' + str(w2) + ',' + str(j2), str(page))
            yield url2

#2.解析起始URL，请求成功返回json数据
def parse_begin_url(url,keyword):
    print(url)
    html=requests.get(url)
    time.sleep(3)
    if html.status_code==200:
        data = html.json()
        # 每个经纬度的POI数据会只显示前400个，以后不再显示，如果当总数为400时，需要将范围缩小在进行一次搜索
        if 400>data['total']>0:
            print(data['total'])
            page_numbers = int(data['total'] / 20) + 1
            if page_numbers>=1:
                write_to_file(data,keyword)
                time.sleep(3)
                if page_numbers>1:
                    for page in range(1,page_numbers):
                        url2=url.replace('page_num=0','page_num='+str(page))
                        res=requests.get(url2).json()
                        write_to_file(res,keyword)
                        time.sleep(3)
        elif data['total']==400:
            print('The grid has POIs more than 400 which exceeds the limit. THe grid should be sublimited')
            urls=get_four_areas(url,keyword)
            for url in urls:
                parse_begin_url(url,keyword)

def get_four_areas(url,keyword):
    #分割的原则是将输入的经纬度范围平均分成四份
    areas=[]
    boundary = url.split('=')[2].split('&')[0].split(',')
    w1=float(boundary[0])
    j1=float(boundary[1])
    w2=float(boundary[2])
    j2=float(boundary[3])
    wei=(float(w2)-float(w1))/2
    jing=(float(j2)-float(j1))/2
    area1=[w1,j1,w1+wei,j1+jing]
    area1=','.join([str(x) for x in area1])
    area2=[w1,j1+jing,w1+wei,j2]
    area2 = ','.join([str(x) for x in area2])
    area3=[w1+wei,j1,w2,j1+jing]
    area3 = ','.join([str(x) for x in area3])
    area4=[w1+wei,j1+jing,w2,j2]
    area4 = ','.join([str(x) for x in area4])
    areas=[area1,area2,area3,area4]
    urls=[]
    for index,area in enumerate(areas):
        url=base_url.format(keyword,area,str(0))
        print('第'+str(index+1)+'个分割图形url：'+url)
        urls.append(url)
    return urls

def write_to_file(data,keyword):
    outputTextFn=os.path.join(outputPOIFd,'{}.txt'.format(keyword))
    if (not os.path.exists(unicode(outputTextFn,'utf-8'))) :
        fid=open(unicode(outputTextFn,'utf-8'),'a')
        fid.write('uid;name;address;lat;lng;district;city;province\n')
    else:
        if (os.stat(unicode(outputTextFn,'utf-8'))).st_size==0:
            fid=open(unicode(outputTextFn,'utf-8'),'a')
            fid.write('uid;name;address;lat;lng;district;city;province\n')
        else:
            fid=open(unicode(outputTextFn,'utf-8'),'a')
    
    for result in data['results']:
        name = result['name']
        bdlat = result['location']['lat']
        bdlng = result['location']['lng']
        coordTrans=bd09_to_wgs84(bdlng,bdlat)
        lat=coordTrans[1]
        lng=coordTrans[0]
        
        address = result['address']
        area=result['area']
        city=result['city']
        province=result["province"]
#        detail = result['detail']
        uid = result['uid']
        print(result)
        a = ';'.join([uid, name, address, str(lat), str(lng),area,city,province])
        a=a.encode('utf-8')
        print(a)
        fid.write(a + '\n')
    fid.close()

#        a = ';'.join([uid, name, address, str(lat), str(lng), str(detail),area,city,province])
#        with open('E:/贾学斌/{}.txt'.format(keyword), 'a') as f:
#            f.write(a + '\n')
#            print('写入成功')

#----------------------------------------------------------------------------------------------------------------------------------
#outputGrid=r'C:\likai_drive\project\test\fishnet4.shp'
outputGridBound=r'C:\likai_drive\project\test\fishnet_grid_bound2.txt'
#keywords=['住宅小区']
#keywords=['美食','中学','小学','幼儿园','综合医院','诊所','公交车站','政府机构']
#keywords=['飞机场','火车站','长途汽车站']
keywords=['休闲广场']
outputPOIFd=r'C:\likai_drive\project\test'
#keyword=keywords[0]
for keyword in keywords:
    urls=get_begin_url(keyword)
    for url in urls:
        parse_begin_url(url,keyword)
#
#def main():
#    keywords = ['百货商场', '超市', '便利店', '商铺', '集市', '通讯营业厅', '邮局', '物流公司', '公用事业', '公园', '风景区', '动物园', '植物园', '游乐园', '文物古迹', '度假村', '农家院', '休闲广场', '高等院校', '中学', '小学', '幼儿园', '特殊教育学校', '综合医院', '专科医院', '诊所', '药店', '飞机场', '火车站', '长途汽车站', '公交车站', '公交线路', '港口', '服务区', '收费站', '银行', '', '信用社', '投资理财', '中央机构', '各级政府', '行政单位', '政治教育机构', '福利机构', '高速公路出口', '高速公路入口', '机场出口', '机场入口', '车站出口', '车站入口', '岛屿', '山峰', '水系']
#    for keyword in keywords:
#        urls=get_begin_url(keyword)
#        for url in urls:
#            parse_begin_url(url,keyword)


