# coding=utf-8
'''
Created on 2013-4-26

@author: zxkletters
'''

import time
from Message import textTemplate

'''
   取消订阅事件的处理器
'''
class UnsubscribeEventHandler(object):
    def __init__(self, message):
        self.message = message
    
    def handle(self):
        message = self.message
        byebye = u'''谢谢您的使用，欢迎再次订阅'''
        return textTemplate % (message.fromUserName, message.toUserName, 
                                   time.time(), byebye, 0)
        
        

