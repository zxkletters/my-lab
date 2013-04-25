# coding=utf-8
'''
Created on 2013-4-25

@author: zxkletters
'''
import time
from Message import textTemplate

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
        else:
            return textTemplate % (message.fromUserName, message.toUserName, 
                                   time.time(), "not support %s now, but it comming soon." \
                                   % (message.msgType), 0)