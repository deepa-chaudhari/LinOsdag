'''
Created on 08-Aug-2016

@author: deepa
'''
from cmd import Cmd
import os
class OsdagPrompt(Cmd):
    def __init__(self):
        pass
    
    def do_hello(self, args):
    
        if len(args) == 0:
            name = 'stranger'
        else:
            name = args
        print "Hello, %s" % name
        
    def do_getUserInputs(self,filename):
        if not os.path.exists(filename) and len(filename)== 0 :
            print"Please enter valid filename"
        else:
            fname = str(filename)
            
            print "You have enter, %s" % fname
     
if __name__ == '__main__':
    prompt = OsdagPrompt()
    prompt.prompt = 'Osdag >>>  '
    prompt.cmdloop('Starting prompt...')
    prompt.use_rawinput()

# from sys import *
# 
# 
# class MyPrompt():
# 
#     def do_hello(self, args):
# 
#         if len(args) == 0:
#             name = 'stranger'
#         else:
#             name = args
#         print "Hello, %s" % name
# 
#     def do_setInputs(self,args):
#         if len(args)== 0:
# 
#             print "inputs are not verified"
#         else:
#             inputs = args
#             print "inputs : %s" % inputs
#             inputlist = inputs
#             print inputlist[0]
#             print"valid inputs"
# 
#     def do_quit(self, args):
#         
#         print "Quitting."
#         return True
# 
# 
# if __name__ == '__main__':
#     prompt = MyPrompt()
#     
