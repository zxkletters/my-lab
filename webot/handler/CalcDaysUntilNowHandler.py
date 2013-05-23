# coding=utf-8
'''
Created on 2013-4-24

@author: zxkletters
'''
import time
from datetime import datetime
from Message import textTemplate

'''
    计算天数间隔的处理器
'''

class CalcDaysUntilNowHandler(object):
    
    def __init__(self, message):
        self.message = message
    
    def handle(self):
        message = self.message
        if message.msgType == "text":
            qryCategory, _ , date = message.content.partition(":")
            helpInfos = "计算天数间隔: days:yyyy/MM/dd, 例子:days:2013/05/01"
                           
            if not _ or not date:
                # reply help infos
                return textTemplate % (message.fromUserName, message.toUserName, 
                                   time.time(), helpInfos, 0)
                
            qryCategory = qryCategory.rstrip().lstrip()
            date = date.rstrip().lstrip()
            
            year, month, day = date.split("/")
            if not year or not month or not day:
                return textTemplate % (message.fromUserName, message.toUserName, 
                                   time.time(), helpInfos, 0)
            
            if qryCategory == "days":
                inputDate = datetime(int(year), int(month), int(day))
                now = datetime.now()
                nowDate = datetime(now.year, now.month, now.day)
                
                return textTemplate % (message.fromUserName, message.toUserName, 
                                   time.time(), (nowDate-inputDate).days, 0)
            else:
                return textTemplate % (message.fromUserName, message.toUserName, 
                                   time.time(), helpInfos, 0)
            
            pass
        else:
            return None
        return textTemplate % (message.fromUserName, message.toUserName, 
                                   time.time(), helpInfos, 0)