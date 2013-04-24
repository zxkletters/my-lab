# coding=utf-8
'''
Created on 2013-4-22

@author: zxkletters
'''
import time
from Message import textTemplate
import handler.QueryFundHandler as QueryFundHandler

# __all__ = ["dispatcher"]

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
            
            if content.find("ping") > 0 or content.find("Ping"):
                return PingPongHandler(self.message)
            
            if content.startswith("jj") or content.startswith("jijin") or content.startswith("fund") \
                or content.startswith("gp") or content.startswith("gupiao") or content.startswith("stock"):
                return QueryFundHandler(self.message)
            
        return PingPongHandler(self.message)


class PingPongHandler(object):
    
    def __init__(self, message):
        self.message = message
    
    def handle(self):
        message = self.message
        if message.msgType == "text":
            if message.content == "Ping" or message.content == "ping":
                return textTemplate % (message.fromUserName, message.toUserName, 
                                   time.time(), "Pong!", 0)
            else:
                return textTemplate % (message.fromUserName, message.toUserName, 
                                   time.time(), "yes,have received your message!", 0)
            
