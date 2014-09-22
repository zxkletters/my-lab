# coding=utf-8
'''
Created on 2014-9-22

@author: zxkletters
'''
'''
订阅股票处理器,股票到指定价格后会自动推通知消息
'''

import httplib
import time

from Message import textTemplate
from utils import logInfo


HOST = "hq.sinajs.cn"
PORT = 80

class SubscribeStockHandler(object):
    
    def __init__(self, message):
        self.message = message
    
    def handle(self):
        message = self.message
        if message.msgType == "text":
            qryCategory, _ , values = message.content.partition(":")
            helpInfos = "订阅股票: sbgp:[美股|A股] [股票代码] 100,如: sbgp:m baba 100"
            
            if qryCategory != "sbgp" or qryCategory != "SBGP":
                return textTemplate % (message.fromUserName, message.toUserName,
                                   time.time(), helpInfos, 0)
            if not _ or not values:
                # reply help infos
                return textTemplate % (message.fromUserName, message.toUserName,
                                   time.time(), helpInfos, 0)
                
            sbValues = values.split(" ")
            if len(sbValues) != 3:
                # reply help infos
                return textTemplate % (message.fromUserName, message.toUserName,
                                   time.time(), helpInfos, 0)
            
            qyrResult = self.batchFetchStockInfos([ x.rstrip().lstrip() for x in sbValues ])
            return textTemplate % (message.fromUserName, message.toUserName,
                                   time.time(), qyrResult, 0)
        else:
            return None
    
    def batchFetchStockInfos(self, sbValues=[]):
        stockType, stock, stockPriceWithNotify = sbValues
        if not stockType and not stock and not stockPriceWithNotify:
            logInfo("sbValues is invalid!") 
            exit(0) 

        params = []
        params.append("%s=%s" % ("_", str(time.time())))
        if stockType == "m":            
            params.append("%s=%s" % ("list", "gb_" + stock))
        else:
            params.append("%s=%s" % ("list", "sh" + stock))
        
        conn = httplib.HTTPConnection(HOST, PORT)
        conn.request('GET', "/?" + "&".join(params), "", {"User-Agent":"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.22 (KHTML, like Gecko) Chrome/25.0.1364.172 Safari/537.22", \
                                                    "Host":HOST, \
                                                    "Accept-Charset":"GBK,utf-8;q=0.7,*;q=0.3", \
                                                    "Accept-Language":"zh-CN,zh;q=0.8"})
        response = conn.getresponse()
        if response.status == 200:
            res = response.read().decode("GBK")
            
            result = []
            for line in res.splitlines():
                __, __, v = line.partition("=")
                if not v:
                    continue
                
                if v and len(v) > 0:
                    finfo = self.printStockInfos(v)
                    if finfo:
                        result.append(finfo)
            return "\n\n".join(result)
        else:
            print "query error! status =", response.status, ";", response.reason

    def printStockInfos(self, stockInfo):
        infos = stockInfo.split(",")
        if not infos:
            return ""
        else:
            return u"%s:\n日期:%s\n时间:%s\n最新价:%s\n今开:%s\n最高:%s\n最低:%s\n昨收:%s\n涨跌幅:%s%s" \
                % (infos[0].replace("\"", ""), infos[-3], infos[-2], infos[3], infos[1], infos[4], infos[5], infos[2], round(((float(infos[3]) - float(infos[2])) / float(infos[2])) * 100, 2), "%")
