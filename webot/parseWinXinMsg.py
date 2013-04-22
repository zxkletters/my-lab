'''
Created on 2013-4-19

@author: zxkletters
'''
import time
import logging
from utils import toUnicode
from Message import TextMessage, ImageMessage
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
    
FORMAT = '%(asctime)-15s  %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)
logger = logging.getLogger(__name__)
# change to False, if on your product environment 
DEV = False

unSupportMsg = ('''<xml>
    <ToUserName><![CDATA[%s]]></ToUserName>
    <FromUserName><![CDATA[%s]]></FromUserName>
    <CreateTime>%d</CreateTime>
    <MsgType><![CDATA[text]]></MsgType>
    <Content><![CDATA[%s]]></Content>
    <FuncFlag>0</FuncFlag>
</xml>''')

def generateMessage(receivedXml): 
    try:
        tree = ET.fromstring(receivedXml)
        msgType = tree.find('MsgType').text
        toUser = tree.find('ToUserName').text
        fromUser = tree.find('FromUserName').text
        createTime =  tree.find('CreateTime').text
        
        if msgType == "text":
            content = toUnicode(tree.find('Content').text)
            msgId = tree.find('MsgId').text
            return TextMessage(toUserName=toUser, fromUserName = fromUser, 
                               content = content, msgId = msgId, createTime = createTime)
        if msgType == "image":
            picUrl = tree.find('PicUrl').text
            msgId = tree.find('MsgId').text
            return ImageMessage(toUserName=toUser, fromUserName = fromUser,
                                picUrl = picUrl, msgId = msgId, createTime = createTime)
        
    except:
        logger.error("etree fromstring error, inputString:\n%s", receivedXml)
        return None

def parseReceivedMsg(msg):
    if DEV:
        tree = ET.ElementTree(file='wxMsg.xml')
    else:
        tree = ET.fromstring(msg)
    
    msgType = tree.find('MsgType').text
    toUser = tree.find('ToUserName').text
    fromUser = tree.find('FromUserName').text
    
    content = None
    if msgType == "text":
        content = tree.find('Content').text
        
    return toUser, fromUser, content, msgType

def generateReplyMsg(toUser=None, fromUser=None, content=None):
    replyMsg = ('''<xml>
    <ToUserName><![CDATA[%s]]></ToUserName>
    <FromUserName><![CDATA[%s]]></FromUserName>
    <CreateTime>%d</CreateTime>
    <MsgType><![CDATA[text]]></MsgType>
    <Content><![CDATA[%s]]></Content>
    <FuncFlag>0</FuncFlag>
</xml>''')

    return replyMsg % (fromUser, toUser , time.time(), content)


if __name__ == "__main__":
    sendMsg = (''' <xml>
 <ToUserName><![CDATA[aaaa]]></ToUserName>
 <FromUserName><![CDATA[bbbb]]></FromUserName> 
 <CreateTime>1348831860</CreateTime>
 <MsgType><![CDATA[text]]></MsgType>
 <Content><![CDATA[thisxxxxxxxxxxxxxxxxx is a test]]></Content>
 <MsgId>1234567890123456</MsgId>
 </xml>''')
    to, fro, cont, msgType = parseReceivedMsg(sendMsg)
    replyMsg = generateReplyMsg(to, fro, cont)
    print to,';', fro,';', cont, ';', msgType
    print replyMsg
    
    print "aaaaaaaaaaaaaaaaaaaaaaaa \n", "bbbbbbbbbbbbbbbbbbbb"


        