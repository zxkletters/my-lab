# coding=utf-8
'''
Created on 2013-4-22

@author: zxkletters
'''
from handler.CalcDaysUntilNowHandler import CalcDaysUntilNowHandler
from handler.DoubanFMHandler import DoubanFMHandler
from handler.HelpHandler import HelpHandler
from handler.PingPongHandler import PingPongHandler
from handler.QueryFundHandler import QueryFundHandler
from handler.QueryStockHandler import QueryStockHandler
from handler.SubscribeEventHandler import SubscribeEventHandler
from handler.SubscribeStockHandler import SubscribeStockHandler
from handler.UnsubscribeEventHandler import UnsubscribeEventHandler
from utils import logInfo
from utils import toUnicode


class HandlerDispatcher(object):
    '''
     This class's duty is to select right handler 
     according to request message's content, then you can
     hander message with the handler
    '''
    
    def __init__(self, message):
        '''
        Constructor
        
        param: message - winxin's message model
        '''
        self.message = message
    
    def dispatcher(self):
        if not self.message:
            pass

        # you can define your rule here, and return right handler
 
        if self.message.msgType == "text":
            content = self.message.content
            
            if content.find("help") >= 0 or content.find("Help") >= 0 \
                or content.find("?") >= 0 or content.find(toUnicode("？")) >= 0:
                logInfo("select HelpHandler to service request")
                return HelpHandler(self.message)
            
            if content.startswith("jj") or content.startswith("jijin") \
                or content.startswith("fund"):
                logInfo("select QueryFundHandler to service request")
                return QueryFundHandler(self.message)
            
            if content.startswith("gp") or content.startswith("gupiao") \
                or content.startswith("stock"):
                logInfo("select QueryStockHandler to service request")
                return QueryStockHandler(self.message)
            
            if content.startswith("days"):
                logInfo("select CalcDaysBeforeHandler to service request")
                return CalcDaysUntilNowHandler(self.message)
            
            if content.startswith("fm") or content.startswith("FM"):
                logInfo("select DoubanFMHandler to service request")
                return DoubanFMHandler(self.message)
            
            if content.startswith("sbgp") or content.startswith("SBGP"):
                logInfo("select SubscribeStockHandler to service request")
                return SubscribeStockHandler(self.message)
            
            if content == "ping" or content == "Ping":
                logInfo("select PingPongHandler to service request")
                return PingPongHandler(self.message)
            
            return HelpHandler(self.message)
        elif self.message.msgType == "event":
            event = self.message.event
            
            if event == "subscribe":
                logInfo("select SubscribeEventHandler to service request")
                return SubscribeEventHandler(self.message)
            elif event == "unsubscribe":
                logInfo("select UnsubscribeEventHandler to service request")
                return UnsubscribeEventHandler(self.message)
            else:
                return HelpHandler(self.message)
        else:
            return PingPongHandler(self.message)
