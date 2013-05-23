# coding=utf-8
'''
Created on 2013-4-24

@author: zxkletters
'''
import time
from Message import textTemplate

'''
    帮助使用说明
'''

class HelpHandler(object):
    
    def __init__(self, message):
        self.message = message
    
    def handle(self):
        message = self.message
        helpInfos = ("使用说明:\n"
                     "1.股票查询:\n"
                     "格式: gp:股票代码,股票代码\n"
                     "例子: gp:600030,600036\n"
                     "2.基金查询:\n"
                     "格式: jj:基金代码,基金代码\n"
                     "例子: jj:040023\n"
                     "3.间隔天数计算:\n"
                     "格式: days:yyyy/MM/dd\n"
                     "例子: days:2013/05/01\n\n"
                     "查看使用说明,请输入 'help' 或者 '?' "
                     )
        return textTemplate % (message.fromUserName, message.toUserName, 
                                   time.time(), helpInfos, 0)