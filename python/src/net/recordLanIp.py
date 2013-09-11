#!/usr/bin/python
# -*- coding: utf-8 -*-
#########################################################################
# File Name: recordLanIp.py
# Author: zxkletters
# mail: zxkletters@gmail.com
# Created Time: 2013-09-11 16:35:49
#########################################################################

import httplib
import json
import subprocess as subp
import time

# 2 minites
SLEEP_TIME_IN_SECONDS = 60 * 2

def getLanIp():
  p = subp.Popen("ifconfig|awk -v RS='' '{if(NR==1) print $0}'|grep 'inet '|awk '{print $2}'|awk -F':' '{print $2}'",stderr=subp.PIPE,stdout=subp.PIPE,shell=True)
  lanIp = p.communicate()[0].decode("utf-8")

  return lanIp

def postData(host,port=80):
  if host and port:
      conn = httplib.HTTPConnection(host, port)
      body = json.dumps({"version":"1.0.0","datastreams":[{"id":"inner_ip","current_value":lanIp}]})
      conn.request("PUT","/v2/feeds/$your_feed_id",body,{"X-ApiKey":"$your-api-key"})
  else:
      return None

  response = conn.getresponse()
  return response.status



# sleep for /etc/rc.local
time.sleep(SLEEP_TIME_IN_SECONDS)
lanIp = getLanIp().strip()

print "------> date: %s" % time.ctime()
print "lan ip: %s" % (lanIp)
print "response status: %s" % postData("api.xively.com", 80)
