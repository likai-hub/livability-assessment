# -*- coding: utf-8 -*-
"""
Created on Fri Aug 02 16:23:02 2019

@author: Likai Zhu

The code is retrieve the housing prices of communities from Lianjia website (https://linyi.lianjia.com), and the coordinates of communities then retrieve from BAIDU API.

"""
import requests
from bs4 import BeautifulSoup
import random
import urllib2
import json
import os
import time
import math



hds=[{'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},\
    {'User-Agent':'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},\
    {'User-Agent':'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'},\
    {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0'},\
    {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/44.0.2403.89 Chrome/44.0.2403.89 Safari/537.36'},\
    {'User-Agent':'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'},\
    {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'},\
    {'User-Agent':'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0'},\
    {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'},\
    {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'},\
    {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11'},\
    {'User-Agent':'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11'},\
    {'User-Agent':'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11'}]

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

#*************************************************************************************
def xiaoqu_spider_detail(url_detail):
    try:
        res=requests.get(url_detail,headers=hds[random.randint(0,len(hds)-1)])
        plain_text=res.text
        soup = BeautifulSoup(plain_text,"html.parser")
    except (urllib2.HTTPError, urllib2.URLError) as e:
        print(e)
        exit(-1)
    except Exception as e:
        print(e)
        exit(-1)    

    xq_info=soup.findAll('span',{'class':'xiaoquInfoContent'})
    if len(xq_info)!=7:
        return ['NULL']*7
    else:
        detailed_info=[]
        for i in range(len(xq_info)):
            detailed_info.append(xq_info[i].get_text())
            
        
        return detailed_info
#*************************************************************************************

##基于百度地图获取小区地理坐标
def getlocation(name):#调用百度API查询位置
    bdurl='http://api.map.baidu.com/place/v2/search?query='
    output='json'
    ak='v9ntzrdoClxSU4uMpLlk3DrLeDvhoPGH'#输入你刚才申请的密匙
    region=u'临沂'
    tag=u'房地产'
    uri=bdurl+name+'&tag='+tag+'&region='+region+'&output='+output+'&ak='+ak
#    print(uri)
    res=requests.get(uri)
    s=json.loads(res.text)['results']
    if s==[]:
        loc={'lng':'NULL','lat':'NULL'}
    else:
        s=json.loads(res.text)['results'][0]
        loc=s.get('location', 'not exist')
        if loc=="not exist":
            loc={'lng':'NULL','lat':'NULL'}
        else:
            trans=bd09_to_wgs84(loc['lng'],loc['lat'])
            loc={'lng':trans[0],'lat':trans[1]}            
    return(loc)

#*************************************************************************************
    
##构建爬虫爬取数据
def xiaoqu_spider(url_page,outputFilePath):
    """
    爬取页面链接中的小区信息
    """
    try:
        res=requests.get(url_page,headers=hds[random.randint(0,len(hds)-1)])
        plain_text=res.text
        soup = BeautifulSoup(plain_text,"html.parser")
    except (urllib2.HTTPError, urllib2.URLError) as e:
        print(e)
        exit(-1)
    except Exception as e:
        print(e)
        exit(-1)
        
    xiaoqu_list=soup.findAll('li',{'class':'clear xiaoquListItem'})
    for xq in xiaoqu_list:
        time.sleep(1)
        info_dict={}
        info_dict.update({u'小区ID':xq.get('data-id')})
        info_dict.update({u'小区名称':xq.find('div',{'class':'title'}).get_text().strip()})
        print(xq.find('div',{'class':'title'}).get_text())
        info_dict.update({u'参考均价':xq.find('div',{'class':'totalPrice'}).get_text()})
        info_dict.update({u'大区域':xq.find('a',{'class':'district'}).get_text()})
        info_dict.update({u'小区域':xq.find('a',{'class':'bizcircle'}).get_text()})
        url_detail="https://linyi.lianjia.com/xiaoqu/"+xq.get('data-id')+"/"
        info=xiaoqu_spider_detail(url_detail)
        try:
#            info_dict.update({u'建筑年代':info[0]})
            info_dict.update({u'建筑类型':info[0]})
            info_dict.update({u'物业费用':info[1]})
            info_dict.update({u'物业公司':info[2]})
            info_dict.update({u'开发商':info[3]})
            info_dict.update({u'楼栋总数':info[4]})
            info_dict.update({u'房屋总数':info[5]})
            info_dict.update({u'附近门店':info[6]})
        except Exception as e:
            print(url_detail)
            print(e)
        esLocation=getlocation(xq.find('div',{'class':'title'}).get_text().strip())
        
        info_dict.update({u'经度':esLocation['lng']})
        info_dict.update({u'纬度':esLocation['lat']})
        info_list=[u'经度',u'纬度',u'小区ID',u'小区名称',u'参考均价',u'大区域',u'小区域',u'建筑类型',u'物业费用',u'物业公司',u'开发商',u'楼栋总数',u'房屋总数',u'附近门店']
        
        if not os.path.exists(outputFilePath):
            fid=open(outputFilePath,'w')
            headline=','.join(info_list)
            headline=headline.encode('utf-8')
            fid.write(headline+'\n')
        else:
            fid=open(outputFilePath,'a')
        linec=[]
        for il in info_list:
            if il in info_dict:
                if isinstance(info_dict[il],(float,int)):
                    linec.append('%.6f'%(info_dict[il]))
                else:
                    
                    linec.append(info_dict[il])
            else:
                linec.append('')
        linec=(','.join(linec)).encode('utf-8')
        fid.write(linec+'\n')
        fid.close()
        
#*************************************************************************************
        
def do_xiaoqu_spider(region_pinyin,outputPath):
    """
    爬取大区域中的所有小区信息
    """
    url=u"https://linyi.lianjia.com/xiaoqu/"+urllib2.quote(region_pinyin)+"/"
    try:
        res=requests.get(url,headers=hds[random.randint(0,len(hds)-1)])
        plain_text=res.text
        soup = BeautifulSoup(plain_text,"html.parser")
    except (urllib2.HTTPError, urllib2.URLError) as e:
        print(e)
        return
    except Exception as e:
        print(e)
        return
    d=json.loads(soup.find('div',{'class':'page-box house-lst-page-box'}).get('page-data'))
    total_pages=d['totalPage']
#    threads=[]
    for i in range(total_pages):
        url_page=u"https://linyi.lianjia.com/xiaoqu/"+urllib2.quote(region_pinyin)+"/"+"pg%s/" % (i+1)
        xiaoqu_spider(url_page,outputPath)
        
#*************************************************************************************

outputFolder=r'G:\geography_presentation\prices_realestate'
if not os.path.exists(outputFolder):
    os.makedirs(outputFolder)
    
#regions=['lanshanqu']
regions=['lanshanqu','hedongqu','luozhuangqu']
for reg in regions:
    outputPath=os.path.join(outputFolder,reg+'.txt')
    do_xiaoqu_spider(reg,outputPath)
    

