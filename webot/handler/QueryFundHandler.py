# coding=utf-8
'''
Created on 2013-4-23

@author: zxkletters
'''
import time
import httplib
from Message import textTemplate

'''
    ��ѯ�������
'''

HOST = "hq.sinajs.cn"
PORT = 80

class QueryFundHandler(object):
    
    def __init__(self, message):
        self.message = message
    
    def handle(self):
        message = self.message
        if message.msgType == "text":
            qryCategory, _ , codes = message.content.partition(":")
            if not _ or not codes:
                # reply help infos
                helpInfos = "查询基金请输入: jj:[基金代码], 如: jj:040023 \n查询股票请输入:gp:[股票代码],如:gp:53333"              
                return textTemplate % (message.fromUserName, message.toUserName, 
                                   time.time(), helpInfos, 0)
            
            qryCategory = qryCategory.rstrip()
            codes = codes.rstrip()
            if qryCategory == "jj" or qryCategory == "jijin" or qryCategory.lower() == "fund":
                qyrResult = batchFetchFoundInfos(codes.split())
                return textTemplate % (message.fromUserName, message.toUserName, 
                                   time.time(), qyrResult, 0)
            elif qryCategory == "gp" or qryCategory == "gupiao" or qryCategory.lower() == "stock":
                return textTemplate % (message.fromUserName, message.toUserName, 
                                   time.time(), "not support, but comming soon!", 0)
            else:
                return textTemplate % (message.fromUserName, message.toUserName, 
                                   time.time(), "yes,have received your message!", 0)
        else:
            return None
            
    def batchFetchFoundInfos(fundList = []):
        '''
            batch get found's infos
            param fundList: your query funds
        '''
        
        if len(fundList) == 0:
            print "fund list is empty!" 
            exit(0) 
        
        params = []
        params.append("%s=%s" % ("_",str(time.time())))
        fundStrings = ""
        for x in ["fu_"+ x for x in fundList]:
            fundStrings += x + ","
        params.append("%s=%s" % ("list",fundStrings))
        
        conn = httplib.HTTPConnection(HOST, PORT)
        conn.request('GET', "/?"+"&".join(params), "", {"User-Agent":"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.22 (KHTML, like Gecko) Chrome/25.0.1364.172 Safari/537.22","Host":HOST,"Accept":"*/*"})
        response = conn.getresponse()
        
        result = []
        if response.status == 200:
            result = response.read()
            for line in result.splitlines():
                tmpList = line.partition("=")
                if(len(tmpList)) <= 2:
                    continue
                result.append(printFundInfos(tmpList[2]))
            
            return "\n\n".join(result)
        else:
            print "query error! status =",response.status,";",response.reason

    def printFundInfos(fundInfo):
        infos = fundInfo.split(",")
        
        return "%s:\nDate:%s\n最新净值:%d\n单位净值:%d\n累计净值:%d\n净值增长率:%d\n涨跌幅:%d" \
            % (infos[0].replace("\"",""), infos[7].replace("\";",""), infos[2], 
               infos[3], infos[4], infos[5], infos[6])
#         print "\t",infos[0].replace("\"",""),"\t\t|"
#         print "---------------------------------"
#         print "Date:",infos[7].replace("\";",""),infos[1]
#         print "最新净值:",infos[2]
#         print "单位净值:",infos[3]
#         print "累计净值:",infos[4]
#         print "净值增长率:",infos[5]
#         print "涨跌幅:",infos[6]
