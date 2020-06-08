# -*- coding: utf-8 -*-
# @Author: chenym
# @Email:	254906610@qq.com
# @Date:   2019-10-10 10:04:26
# @Last Modified by:   chenym
# @Last Modified time: 2020-05-29 11:06:56
'''
日志打印工具
'''
import logging
from logging import handlers

class Logger():
    level_relations = {
        'debug':logging.DEBUG,
        'info':logging.INFO,
        'warning':logging.WARNING,
        'error':logging.ERROR,
        'crit':logging.CRITICAL
    }#日志级别关系映射

    def __init__(self,filename ='all.log',level='debug',when='D',backCount=6,fmt='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'):
        self.logger = logging.getLogger(filename)
        format_str = logging.Formatter(fmt)#设置日志格式
        self.logger.setLevel(self.level_relations.get(level))#设置日志级别
        sh = logging.StreamHandler()#往屏幕上输出
        sh.setFormatter(format_str) #设置屏幕上显示的格式
        th = handlers.TimedRotatingFileHandler(filename=filename,when=when,backupCount=backCount,encoding='utf-8')#往文件里写入#指定间隔时间自动生成文件的处理器
        #实例化TimedRotatingFileHandler
        #interval是时间间隔，backupCount是备份文件的个数，如果超过这个个数，就会自动删除，when是间隔的时间单位，单位有以下几种：
        # S 秒
        # M 分
        # H 小时、
        # D 天、
        # W 每星期（interval==0时代表星期一）
        # midnight 每天凌晨
        th.setFormatter(format_str)#设置文件里写入的格式
        self.logger.addHandler(sh) #把对象加到logger里
        self.logger.addHandler(th)
    def LogFile(self,str,type=20):
        if type == 10 :
            self.logger.debug(str)
        elif type == 20 :
            self.logger.info(str)
        elif type == 30 :
            self.logger.warning(str)
        elif type == 40 :
            self.logger.error(str)
        elif type == 50 :
            self.logger.critical(str)
    def LogDebug(self,str):
        self.logger.debug(str)
    def LogInfo(self,str):
        self.logger.info(str)
    def LogWarn(self,str):
        self.logger.warning(str)
    def LogError(self,str):
        self.logger.error(str)
    def LogCritical(self,str):
        self.logger.critical(str)
if __name__ == '__main__':
    log = Logger('all.log',level='debug')
    log.LogError('日志打印')