# -*- coding: utf-8 -*- 
# 增加当前路径到Path中
# add windows path variable
#path=%path%;D:/Python
#from subprocess import Popen, PIPE
import os
#import sys
'''import os
print os.getcwd()
import sys
print sys.argv[0]'''
"""
def add_path():
    proc = Popen(["set", 'path==\%path\%;d:/mypath'], stdout = PIPE, stderr = PIPE)
    return_code = proc.wait()
    voutput = proc.stdout.read()
    print return_code
    print voutput
    return 
    new_path = os.getcwd()
    proc = Popen(["path=\%path%" + ";" + "new_path",], stdout = PIPE, stderr = PIPE)
    return_code = proc.wait()
    voutput = proc.stdout.read()
    if return_code == 0:
        return True
    #elif return_code == -999:
    #    print 'not set:', voutput
    else:
        #print "Failure %s:\n%s" % (return_code, voutput)
        return False
"""
def add_path():
    cwd = os.getcwd()
    env = os.environ['PATH']
    os.environ['PATH'] = cwd + ";"+ env
    
if __name__ == '__main__':
    add_path()
