# coding=utf-8
'''
Created on 2013-08-26 20:37

@author: zxkletters
'''
import time
import urllib2
import json
from Message import musicTemplate
from Message import textTemplate

'''
    豆瓣FM
'''
DOUBAN_FM_LAYLIST = "http://douban.fm/j/mine/playlist?type=n&sid=1052632&pt=14.0&channel=%s&pb=64&from=mainsite&r=4d46e8067b"

class DoubanFMHandler(object):
    
    def __init__(self, message):
        self.message = message
        
    def getDoubanFmInfo(self, channel=9):
        try:
            url = DOUBAN_FM_LAYLIST % (9)
            resp = urllib2.urlopen(url=url, timeout=5)
            return resp.read()
        except:
            return None
        
    def handle(self):
        message = self.message
        if message.msgType == "text":
            _, _ , channel = message.content.partition(":")
            helpInfos = "收听豆瓣FM: fm:channel, 例子:fm:9"
                           
            if not _ or not channel:
                # reply help infos
                return textTemplate % (message.fromUserName, message.toUserName, 
                                   time.time(), helpInfos, 0)
                
            channel = channel.rstrip().lstrip()
            
            doubanFMResp = self.getDoubanFmInfo(channel)
            if doubanFMResp:
                jsonObj = json.loads(doubanFMResp)
                loop = 0
                for song in jsonObj["song"]:
                    if loop >= 1:
                        break
                    loop +=1
                    return musicTemplate % (message.fromUserName, message.toUserName, 
                                    time.time(), song["title"], song["artist"], song["url"], song["url"])
        else:
            return None
        
        return textTemplate % (message.fromUserName, message.toUserName, 
                                   time.time(), helpInfos, 0)