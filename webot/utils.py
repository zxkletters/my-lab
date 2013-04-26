# coding=utf-8
'''
Created on 2013-4-20

@author: zxkletters
'''
import time
import logging
from hashlib import sha1
from Message import TextMessage, ImageMessage, EventMessage
import unittest

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


FORMAT = '%(asctime)-15s  %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)
logger = logging.getLogger(__name__)

def logInfo(msg):
    logger.info(msg)
    
def logError(msg):
    logger.error(msg)

def logWarn(msg):
    logger.warn(msg)

def checkSignature(token=None, timestamp=None, nonce=None, signature=None):
    if token is None or timestamp is None or nonce is None or signature is None:
        return False
    
    valueList = [token, timestamp, nonce]
    valueList.sort(cmp=None, key=None, reverse=False)
    return sha1("".join(valueList)).hexdigest() == signature

def toUnicode(value):
    if isinstance(value, unicode):
        return value
    if isinstance(value, basestring):
        return value.decode('utf-8')
    if isinstance(value, int):
        return str(value)
    if isinstance(value, bytes):
        return value.decode('utf-8')
    return value

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
        if msgType == "event":
            event = tree.find('Event').text
            eventKey = tree.find('EventKey').text
            return EventMessage(toUserName=toUser, fromUserName = fromUser,
                                event = event, eventKey = eventKey, createTime = createTime)
        
    except:
        logError("etree fromstring error, inputString:\n%s", receivedXml)
        return None


# test func
if __name__ == "__main__":
    class test(unittest.TestCase):
        def testCheckSignature_fail(self):
            self.assertFalse(checkSignature())
            self.assertFalse(checkSignature(token="test"))
            
        def testCheckSignature_success(self):
            # args have sorted
            token = "111"
            timestamp = "2222"
            nonce = "3333"
            
            signature = sha1("".join([token, timestamp, nonce])).hexdigest()
            self.assertTrue(checkSignature(token, timestamp, nonce, signature))
            
    unittest.main()
    