# coding=utf-8
'''
Created on 2013-4-22

@author: zxkletters
'''

# templates
textTemplate = '''
 <xml>
     <ToUserName><![CDATA[%s]]></ToUserName>
     <FromUserName><![CDATA[%s]]></FromUserName>
     <CreateTime>%d</CreateTime>
     <MsgType><![CDATA[text]]></MsgType>
     <Content><![CDATA[%s]]></Content>
     <FuncFlag>%d</FuncFlag>
 </xml>
 '''
 
musicTemplate = '''
 <xml>
   <ToUserName><![CDATA[%s]]></ToUserName>
   <FromUserName><![CDATA[%s]]></FromUserName>
   <CreateTime>%d</CreateTime>
   <MsgType><![CDATA[music]]></MsgType>
   <Music>
     <Title><![CDATA[%s]]></Title>
     <Description><![CDATA[%s]]></Description>
     <MusicUrl><![CDATA[%s]]></MusicUrl>
     <HQMusicUrl><![CDATA[%s]]></HQMusicUrl>
   </Music>
 </xml>
 '''
 
class BaseMessage(object):
    '''
    classdocs basic winxin's message object
    '''
    
    def __init__(self, toUserName, fromUserName, msgType, createTime):
        '''
        Constructor
        '''
        self.toUserName = toUserName
        self.fromUserName = fromUserName
        self.msgType = msgType
        self.createTime = createTime

class TextMessage(BaseMessage):
    def __init__(self, toUserName, fromUserName, content, msgId, createTime):
        super(TextMessage, self).__init__(toUserName, fromUserName, "text", createTime)  
        self.content = content.rstrip().lstrip()
        self.msgId = msgId


class ImageMessage(BaseMessage):
    def __init__(self, toUserName, fromUserName, picUrl, msgId, createTime):
        super(ImageMessage, self).__init__(toUserName, fromUserName, "image", createTime)  
        self.picUrl = picUrl
        self.msgId = msgId
        
class MusicMessage(BaseMessage):
    def __init__(self, **kwargs): 
#     def __init__(self, toUserName, fromUserName, picUrl, msgId, createTime):
        super(MusicMessage, self).__init__(kwargs["toUserName"], kwargs["fromUserName"], "music", kwargs["createTime"])  
        self.title = kwargs["title"]
        self.description = kwargs["description"]
        self.musicUrl = kwargs["musicUrl"]
        self.hqMusicUrl = kwargs["hqMusicUrl"]

class EventMessage(BaseMessage):
    def __init__(self,toUserName, fromUserName, createTime, event, eventKey):
        super(EventMessage, self).__init__(toUserName, fromUserName, "event", createTime)
        self.event = event
        self.eventKey = eventKey