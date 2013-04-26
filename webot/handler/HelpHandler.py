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
                     "目前只支持股票、基金查询功能.\n"
                     "股票查询: gp:股票代码\n"
                     "批量查询: gp:股票代码,股票代码\n"
                     "基金查询: jj:基金代码\n"
                     "批量查询: jj:基金代码,基金代码\n"
                     "查看使用说明,请输入 'help' 或者 '?' "
                     )
        return textTemplate % (message.fromUserName, message.toUserName, 
                                   time.time(), helpInfos, 0)