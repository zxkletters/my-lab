'''
Created on 2013-4-19

@author: zxkletters
'''

import time
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

# change to False, if on your product environment 
DEV = True

unSupportMsg = ('''<xml>
    <ToUserName><![CDATA[%s]]></ToUserName>
    <FromUserName><![CDATA[%s]]></FromUserName>
    <CreateTime>%d</CreateTime>
    <MsgType><![CDATA[text]]></MsgType>
    <Content><![CDATA[%s]]></Content>
    <FuncFlag>0</FuncFlag>
</xml>''')

def parseReceivedMsg(msg):
    if DEV:
        tree = ET.ElementTree(file='wxMsg.xml')
    else:
        tree = ET.fromstring(msg)

    for elem in tree.iter():
        if elem.tag == "ToUserName":
            toUser = elem.text
        if elem.tag == "FromUserName":
            fromUser = elem.text
        if elem.tag == "Content":
            content = elem.text
        if elem.tag == "MsgType":
            msgType = elem.text
            
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
    to, fro, cont = parseReceivedMsg(sendMsg)
    replyMsg = generateReplyMsg(to, fro, cont)
    print to, fro, cont
    print replyMsg


        