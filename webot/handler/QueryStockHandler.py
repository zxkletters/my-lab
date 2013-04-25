# coding=utf-8
'''
Created on 2013-4-25

@author: zxkletters
'''
import time
from utils import logInfo
from utils import toUnicode
import httplib
from Message import textTemplate

'''
股票查询处理器
'''

class QueryStockHandler(object):
    
    def __init__(self, message):
        self.message = message
    
    def handle(self):
        message = self.message
        if message.msgType == "text":
            qryCategory, _ , codes = message.content.partition(":")
            if not _ or not codes:
                # reply help infos
                helpInfos = "基金查询: jj:[基金代码], 如: jj:040023 \n股票查询: gp:[股票代码],如: gp:600030"              
                return textTemplate % (message.fromUserName, message.toUserName, 
                                   time.time(), helpInfos, 0)
            
            return textTemplate % (message.fromUserName, message.toUserName, 
                                   time.time(), "not support now, but comming soon.", 0)
        else:
            return None