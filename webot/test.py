# coding=utf-8
'''
Created on 2013-4-20

@author: zxkletters
'''
import httplib
from hashlib import sha1
import time

xml = """<xml><ToUserName><![CDATA[xiaoke]]></ToUserName>
 <FromUserName><![CDATA[zxkletters]]></FromUserName> 
 <CreateTime>%d</CreateTime>
 <MsgType><![CDATA[text]]></MsgType>
 <Content><![CDATA[ping]]></Content>
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

conn = httplib.HTTPConnection(host="42.120.21.19", port=80)
conn.request(method='POST', url=url, body=xml % time.time(), headers={"Content-Type": "application/xml"})
response = conn.getresponse()

print response.getheaders()
print response.read()
conn.close()