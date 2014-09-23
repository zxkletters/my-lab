# coding=utf-8
'''
Created on 2013-4-23

@author: zxkletters
'''
'''
基金查询处理器
'''

import httplib
import time

from Message import textTemplate
import Message
from utils import logInfo


HOST = "hq.sinajs.cn"
PORT = 80

class QueryFundHandler(object):
    
    def __init__(self, message):
        self.message = message
    
    def handle(self):
        message = self.message
        if message.msgType == "text":
            qryCategory, _ , codes = message.content.partition(":")
            helpInfos = "基金查询: jj:基金代码, 如: jj:040023"               
            if not _ or not codes:
                # reply help infos
                return textTemplate % (message.fromUserName, message.toUserName,
                                   time.time(), helpInfos, 0)
            
            qryCategory = qryCategory.rstrip().lstrip()
            codes = codes.rstrip().lstrip()
            if qryCategory == "jj" or qryCategory == "jijin" or qryCategory.lower() == "fund":
                qyrResult = self.batchFetchFoundInfos(codes.split(","))
                return textTemplate % (message.fromUserName, message.toUserName,
                                   time.time(), qyrResult, 0)
            else:
                return textTemplate % (message.fromUserName, message.toUserName,
                                   time.time(), helpInfos, 0)
        else:
            return None
            
    def batchFetchFoundInfos(self, fundList=[]):
        '''
            batch get found's infos
            param fundList: your query funds
        '''
        
        if len(fundList) == 0:
            logInfo("fund list is empty!") 
            exit(0) 

        params = []
        params.append("%s=%s" % ("_", str(time.time())))
        fundStrings = ""
        for x in ["fu_" + x for x in fundList]:
            fundStrings += x + ","

        params.append("%s=%s" % ("list", fundStrings))
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
                    finfo = self.printFundInfos(v)
                    if finfo:
                        result.append(finfo)
            return "\n\n".join(result)
        else:
            print "query error! status =", response.status, ";", response.reason

    def printFundInfos(self, fundInfo):
        infos = fundInfo.split(",")
        if not infos or len(infos) < 6:
            return u"查询的基金不存在."
        else:
            return u"%s:\n日期:%s\n时间:%s\n最新估值:%s\n最新净值:%s\n涨跌幅:%s%s" \
                % (infos[0].replace("\"", ""), infos[7].replace("\";", ""), infos[1], infos[2], infos[3], infos[6], "%")
                
if __name__ == '__main__':
    a = QueryFundHandler(Message.TextMessage("test", "test2", "jj:notexist", 100, 329875))
    print a.handle()
    
    b = QueryFundHandler(Message.TextMessage("test", "test2", "jj:040023", 100, 329875))
    print b.handle()
