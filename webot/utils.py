'''
Created on 2013-4-20

@author: zxkletters
'''
from hashlib import sha1
import unittest
import logging

FORMAT = '%(asctime)-15s  %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)
logger = logging.getLogger(__name__)

def logInfo(msg):
    logger.info(msg)
    
def logError(msg):
    logger.error(msg)

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
    