# coding=utf-8
'''
Created on 2013-4-24

@author: zxkletters
'''
import time
import httplib
from Message import textTemplate

'''
    帮助说明处理器
'''

HOST = "hq.sinajs.cn"
PORT = 80

class HelpHandler(object):
    
    def __init__(self, message):
        self.message = message
    
    def handle(self):
        message = self.message
        helpInfos = ("使用说明:\n"
                     "目前只支持股票、基金查询功能.\n"
                     "股票查询: gp:[股票代码]\n"
                     "批量查询: gp:[股票代码,股票代码]\n"
                     "基金查询: jj:[基金代码]\n"
                     "批量查询: jj:[基金代码,基金代码]\n"
                     "查看使用说明请输入'help'或者'?'"
                     )
        return textTemplate % (message.fromUserName, message.toUserName, 
                                   time.time(), helpInfos, 0)
            
            
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
