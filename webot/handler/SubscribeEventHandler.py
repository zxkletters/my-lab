# coding=utf-8
'''
Created on 2013-4-26

@author: zxkletters
'''

import time
from Message import textTemplate

'''
   订阅事件处理器
'''
class SubscribeEventHandler(object):
    '''
       when user subscribe 'Mee', it will print welcome infos
    '''
    
    def __init__(self, message):
        self.message = message
    
    def handle(self):
        message = self.message
        welcome = (u"谢谢订阅，该公共帐号主要提供了一些常用工具，在您使用的过程中有任何问题和建议，"
        u"随时都可以进行回复、反馈。\n输入'help'或'?'可以查看使用说明。")
        return textTemplate % (message.fromUserName, message.toUserName, 
                                   time.time(), welcome, 0)
        
        

