# coding=utf-8
'''
Created on 2013-4-20

@author: zxkletters
'''
# import logging
import webapp2
import parseWinXinMsg as WX
from utils import checkSignature
from utils import logInfo
from HandlerDispatcher import HandlerDispatcher

# your token put here
token = ""

class home(webapp2.RequestHandler):
    def get(self):
        signature = self.request.get("signature", None)
        timestamp = self.request.get("timestamp", None)
        nonce = self.request.get("nonce", None)
        echostr = self.request.get("echostr", None)
        
        if checkSignature(signature = signature, timestamp = timestamp, nonce = nonce, token = token):
            self.response.write(echostr)
        else:
            webapp2.abort(403)
        
    def post(self):
#         signature = self.request.get("signature", None)
#         timestamp = self.request.get("timestamp", None)
#         nonce = self.request.get("nonce", None)
#         if not checkSignature(signature = signature, timestamp = timestamp, nonce = nonce, token = token):
#             webapp2.abort(403)
        
        logInfo("request.body:\n%s" % self.request.body)
        message = WX.generateMessage(self.request.body)
        
        # you can handle message here, example: substring content,then reply
        handler = HandlerDispatcher(message).dispatcher()
        replyString = handler.handle()
        
        self.response.content_type = "application/xml"
        self.response.write((replyString))
        
class welcome(webapp2.RequestHandler):
    def get(self):
        self.response.write("welcome! you may have interests to subscribe Mee at WinXin mp")
    
    def post(self):
        self.response.write("welcome! you may have interests to subscribe Mee at WinXin mp")

# your wsgi's app , url mapping shoud put here
app = webapp2.WSGIApplication([
                               ('/', welcome),
                               ('/gate', home)
                               ], debug=True)

def startServer():
    from paste import httpserver
    httpserver.serve(app, host='0.0.0.0', port='80')

if __name__ == '__main__':
    startServer()
