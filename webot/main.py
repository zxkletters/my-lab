'''
Created on 2013-4-20

@author: zxkletters
'''
import time
import webapp2
import parseWinXinMsg as WX
from utils import checkSignature
from utils import toUnicode

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
        toUser, fromUser, content, msgType = WX.parseReceivedMsg(self.response.body)
        self.response.content_type = "application/xml"

        if msgType == "text":
            # TODO handle received content first , then reply
            self.response.write(toUnicode(WX.generateReplyMsg(toUser, fromUser, "yes,you are success")))
        else:
            replyContent = "not support %s now, but comming soon" % msgType
            self.response.write(toUnicode(WX.unSupportMsg % (fromUser, toUser, time.time(), replyContent)))
        
class welcome(webapp2.RequestHandler):
    def get(self):
        self.response.write("welcome! you may have interests to subscribe zxkletters")
    
    def post(self):
        self.response.write("welcome! you may have interests to subscribe zxkletters")
        
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
