# -*- coding: utf-8 -*-
# @Author: chenym
# @Email:   254906610@qq.com
# @Date:   2019-10-15 16:34:23
# @Last Modified by:   chenym
# @Last Modified time: 2020-06-04 16:19:06
import logging
import json
from WebTool import Webtools
import urllib3
import random
class Maptools():
    def __init__(self,key='4d7e070d9ca8a48f2894c852eed08f74',r=150):
        urllib3.disable_warnings()
        logging.basicConfig(format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                    level=logging.WARNING)
        self.webtools = Webtools()
        self.key = key
        self.r = r
    #根据地址获取经纬度
    def getLocation(self,addr):
        url = 'https://restapi.amap.com/v3/geocode/geo?key='+self.key+'&address='+addr
        respon = self.webtools.web_Get(url).text
        return respon
    # 根据经纬度获取详细单一地址
    def getAddr(self,locat):
        url = 'https://restapi.amap.com/v3/geocode/regeo?key='+self.key+'&location='+locat
        respon = self.webtools.web_Get(url).text
        return respon
    # 根据经纬度获取半径100内的所有建筑信息
    def getAddrList(self,locat,r=100):
        url = 'https://restapi.amap.com/v3/geocode/regeo?key='+self.key+'&location='+locat+'&radius='+str(r)+'&extensions=all'
        respon = self.webtools.web_Get(url).text
        return respon
    def toJson(self,str1):
        jsonStr = json.loads(str1)
        return jsonStr
    def getDestLocatInfo(self,addr):
        locat_info = Maptools().getLocation(addr)
        # 转JSON格式
        locat_json = Maptools().toJson(locat_info)
        # 获取经纬度
        location = locat_json['geocodes'][0]['location']
        #print("1.获取经纬度-"+addr+':'+location)
        # 获取半径是50米以内所有建筑物信息
        addr_info = Maptools().getAddrList(location,self.r)
        # 转JSON格式
        addr_json = Maptools().toJson(addr_info)
        address = addr_json['regeocode']['pois']
        logging.info("    1.获取经纬度-"+addr+':'+location)
        # 附近建筑物个数
        total = len(address)
        logging.info("    2.获取-"+str(self.r)+"米以内建筑物总数："+str(total))
        # 取出经纬度与建筑物信息
        logging.info("    3.获取-"+str(self.r)+"米以内所有建筑物信息")
        for v_addr in address:
            logging.info("    "+v_addr['location'] +':'+v_addr['name'])
        # 随机取一条信息
        locat_index = random.randint(0,total-1)
        tar_locat = address[locat_index]['location']
        tar_addr = address[locat_index]['name']
        logging.info("    4.随机获取第"+str(locat_index+1)+"条信息-"+tar_locat +':'+tar_addr)
        # 取详细的信息
        tar_addr_info = Maptools().getAddr(tar_locat)
        # 转JSON格式
        tar_addr_json = Maptools().toJson(tar_addr_info)
        tar_addr_locat = tar_addr_json['regeocode']['addressComponent']['streetNumber']['location']
        tar_addr_name = tar_addr_json['regeocode']['formatted_address']
        tar_address = [tar_addr_locat,tar_addr_name]
        logging.info("    5.获取-"+str(self.r)+"米以内随机建筑物信息")
        logging.info("    "+str(tar_address))
        return tar_address
# if __name__ == '__main__':
#     key = '4d7e070d9ca8a48f2894c852eed08f74'
#     addr = '观日路38号'
#     maptools = Maptools(key,400)
#     maptools.getDestLocatInfo(addr)

    #logging.info(maptools.getAddr('118.185881,24.485719'))

    # locat_info = maptools.getLocation(addr)
    # # 转JSON格式
    # locat_json = maptools.toJson(locat_info)
    # # 获取经纬度
    # location = locat_json['geocodes'][0]['location']
    # #print("1.获取经纬度-"+addr+':'+location)
    # # 获取半径是50米以内所有建筑物信息
    # r =150
    # addr_info = maptools.getAddrList(location,r)
    # # 转JSON格式
    # addr_json = maptools.toJson(addr_info)
    # address = addr_json['regeocode']['pois']
    # logging.info("1.获取经纬度-"+addr+':'+location)
    # # 附近建筑物个数
    # total = len(address)
    # logging.info("2.获取-"+str(r)+"米以内建筑物总数："+str(total))
    # # 取出经纬度与建筑物信息
    # logging.info("3.获取-"+str(r)+"米以内所有建筑物信息")
    # for v_addr in address:
    #     logging.info("    "+v_addr['location'] +':'+v_addr['name'])
    # # 随机取一条信息
    # locat_index = random.randint(0,total-1)
    # tar_locat = address[locat_index]['location']
    # tar_addr = address[locat_index]['name']
    # logging.info("4.随机获取第"+str(locat_index+1)+"条信息-"+tar_locat +':'+tar_addr)
    # # 取详细的信息
    # tar_addr_info = maptools.getAddr(tar_locat)
    # # 转JSON格式
    # tar_addr_json = maptools.toJson(tar_addr_info)
    # tar_addr_locat = tar_addr_json['regeocode']['addressComponent']['streetNumber']['location']
    # tar_addr_name = tar_addr_json['regeocode']['formatted_address']
    # tar_address = [tar_addr_locat,tar_addr_name]
    # logging.info("5.获取-"+str(r)+"米以内随机建筑物信息")
    # logging.info(str(tar_address))

# logging.debug('debug 信息')
# logging.info('info 信息')
# logging.warning('warning 信息')
# logging.error('error 信息')
# logging.critical('critial 信息')