#!/usr/bin/python
# -*- coding: utf-8 -*-
#########################################################################
# File Name: recordLanIp.py
# Author: zxkletters
# mail: zxkletters@gmail.com
# Created Time: 2013-09-11 16:35:49
#########################################################################

import os
import urllib2
import json

def replaceWithSpecificIp(ip=None):
    newHostArray = []
    f = open("C:\Windows\System32\drivers\etc\hosts","r")
    #lines = f.readlines()
    for line in f:
        if line.__contains__("ubuntu"):
            newHostArray.append("%s  zxkletters ubuntu\n" % ip)
        else:
            newHostArray.append(line)
            
    f.close()
    
    return newHostArray

def getPcInnerIp():
    req = urllib2.Request('http://api.xively.com/v2/feeds/$feed_id/datastreams/inner_ip.json')
    req.add_header('X-ApiKey', '$your-app-key')
    f = urllib2.urlopen(req)
    
    ret = f.read()
    jsonObj = json.loads(ret,encoding="utf-8")
    return jsonObj["current_value"].strip()

def flushToHost(lines=None):
    if not lines:
        return 
    
    f = open("C:\Windows\System32\drivers\etc\hosts","w")
    for line in lines:    
        f.write(line)
        
    f.close()

innerIp = getPcInnerIp()
print "inner ip: %s" % innerIp
hostLines = replaceWithSpecificIp(innerIp)
flushToHost(hostLines)
