'''
Created on 2013-4-8

@author: xiaoke.zhangxk
'''

def blueBox(func):
    def wrapped():
        print "~~ blue ~~~"
        func()
        print "~~ blue ~~"
    return wrapped

def redBox(func):
    def wrapped():
        print "** red **"
        func()
        print "** red **"
    return wrapped

def box():
    print " i am a box."
    
box()

print "-----------------"
decorated = redBox(blueBox(box))
decorated()

print "-----------------"
@blueBox
@redBox
def newBox():
    print "i am another box."
newBox()