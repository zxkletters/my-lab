# coding=GBK
'''
Created on 2013-4-20

@author: zxkletters
'''

import httplib
from hashlib import sha1
import time

xml = """<xml><ToUserName><![CDATA[toUser]]></ToUserName>
 <FromUserName><![CDATA[fromUser]]></FromUserName> 
 <CreateTime>%d</CreateTime>
 <MsgType><![CDATA[text]]></MsgType>
 <Content><![CDATA[this is a test]]></Content>
 <MsgId>1111111</MsgId>
</xml>"""

timestamp = str(time.time())
nonce = str(time.time())
token = "test"
echostr = "test"
valueList = [timestamp, nonce, token]
valueList.sort()
signature = sha1("".join(valueList)).hexdigest()
url = "/gate?timestamp=" + timestamp + "&nonce=" + nonce + "&echostr=" + echostr + "&signature=" + signature

conn = httplib.HTTPConnection(host="127.0.0.1", port=8080)
conn.request(method='POST', url=url, body=xml % time.time(), headers={"Content-Type": "application/xml"})
response = conn.getresponse()

print response.getheaders()
print response.read()
conn.close()
