# coding=utf-8
'''
Created on 2013-4-25

@author: zxkletters
'''
'''
股票查询处理器
'''

import httplib
import time

from Message import textTemplate
import Message
from utils import logInfo


HOST = "hq.sinajs.cn"
PORT = 80

class QueryStockHandler(object):
    
    def __init__(self, message):
        self.message = message
    
    def handle(self):
        message = self.message
        if message.msgType == "text":
            qryCategory, _ , codes = message.content.partition(":")
            helpInfos = "股票查询: gp:[股票代码], 如: gp:600030"              
            if not _ or not codes:
                # reply help infos
                return textTemplate % (message.fromUserName, message.toUserName,
                                   time.time(), helpInfos, 0)
            
            qryCategory = qryCategory.rstrip().lstrip()
            codes = codes.rstrip().lstrip()
            if qryCategory == "gp" or qryCategory == "gupiao" or qryCategory.lower() == "stock":
                qyrResult = self.getStockInfo(codes.split(","))
                return textTemplate % (message.fromUserName, message.toUserName,
                                   time.time(), qyrResult, 0)
            else:
                return textTemplate % (message.fromUserName, message.toUserName,
                                   time.time(), helpInfos, 0)
        else:
            return None
    
    def getStockInfo(self, stockList=[]):
        '''
            batch get stock's infos
            param stockList: your query stocks
        '''
        
        if len(stockList) == 0:
            logInfo("stock list is empty!") 
            exit(0) 

        params = []
        params.append("%s=%s" % ("_", str(time.time())))
        stockStrings = ""
        for x in ["sh" + x for x in stockList]:
            stockStrings += x + ","

        params.append("%s=%s" % ("list", stockStrings))
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
        if not infos or len(infos) < 3:
            return u"查询的股票不存在."
        else:
            return u"%s:\n日期:%s\n时间:%s\n最新价:%s\n今开:%s\n最高:%s\n最低:%s\n昨收:%s\n涨跌幅:%s%s" \
                % (infos[0].replace("\"", ""), infos[-3], infos[-2], infos[3], infos[1], infos[4], infos[5], infos[2], round(((float(infos[3]) - float(infos[2])) / float(infos[2])) * 100, 2), "%")
                
if __name__ == '__main__':
    a = QueryStockHandler(Message.TextMessage("test", "test2", "gp:notexist", 100, 329875))
    print a.handle()
    
    b = QueryStockHandler(Message.TextMessage("test", "test2", "gp:600030", 100, 329875))
    print b.handle()
