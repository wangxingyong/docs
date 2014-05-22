#!/usr/bin/python
# -*- coding: cp936 -*-

import time
import random
import codecs
from Configuration import Configuration
from AppConfig import AppConfig
from App import App
from EnvContext import EnvContext
from StringIO import StringIO
import sys
import os
from subprocess import Popen
import subprocess
import Log
import httplib

class SysResult:
    def __init__(self):
        self.isSucceed = False
        self.out = None
        self.error = None


def doSystem(cmd, envContext, commandKey):
    sr = doCommandSystem(cmd)
    execOutput(cmd, sr, envContext, commandKey)
    return sr

def doSubprocess(cmd, envContext, commandKey):
    sr = doCommandSubprocess(cmd)
    execOutput(cmd, sr, envContext, commandKey)
    return sr

def getLogFileName(envContext, op):
    op = op.replace("/","-")
    return envContext.getLogDir()+"/"+op+".log"

def saveLog(envContext, op, data):
    logFileName = getLogFileName(envContext, op)
    f = open(logFileName, 'w')
    f.write(data)
    f.close()
    return logFileName


def execOutput(cmd, sysResult, envContext, commandKey):
    if sysResult.out != None:
        logFileName = getLogFileName(envContext, commandKey+"_out")
        #f = codecs.open(logFileName, 'w',"utf-8")
        f = open(logFileName, 'w')
        f.write(cmd+"\n")
        f.write(sysResult.out)
        f.close()

    if sysResult.error != None:
        logFileName = getLogFileName(envContext, commandKey+"_error")
        #f = codecs.open(logFileName, 'w',"utf-8")
        f = open(logFileName, 'w')
        f.write(cmd+"\n")
        f.write(sysResult.error)
        f.close()

def doCommandSystem(cmd):
    sr = SysResult()
    sr.out=""
    try:
        returncode = os.system(cmd)
      
        if returncode == 0:
            sr.isSucceed = True
        else:
            sr.isSucceed = False
    except Exception, e:
        print "error info: ",e
        sr.isSucceed = False
    finally:
        pass
    return sr


def doCommandSubprocess(cmd):
    sr = SysResult()
    try:
        out = os.popen(cmd);
        sr.isSucceed = True
        sr.out = out.read()
    except Exception, e:
        Log.info(e)
        Log.info("error info: "+ e)
        sr.isSucceed = False
    finally:
        pass
    return sr

def httpGet(host, path):
    conn = httplib.HTTPConnection(host)
    conn.putrequest("GET", path)
    conn.endheaders()

    r1 = conn.getresponse()

    if r1.status==httplib.OK:
        return r1.read()
    else:
        print r1.status, r1.reason
        return None


def test():
    c = "E: & cd E:/SVN/work/a23_10 & jsvn merge --dry-run -r 7:HEAD file:///E:/SVN/sample/branches/a22_9 "
    c = "E: & cd E:/SVN/work/a23_10 & jsvn merge  -r 7:HEAD file:///E:/SVN/sample/branches/a22_9 "
    c1 = "dir&&dir&ping localhost"
    c = "jsvn help"
    c1 = "E: & cd E:/SVN/work/a23_10 &dir"
    c2 = "jsvn log --stop-on-copy file:///E:/SVN/sample/branches/a22_9"
    
    sr = doSubprocess()
    s = sr.out+"          doSubprocess"
    print sr.isSucceed
    print s
"""
    sr = doSystem(c)
    s = sr.out+"          doSystem"
    print sr.isSucceed
    print s
http://svn.alibaba-inc.com/repos/ali_intl/apps/intl-myalibaba/trunk
"""

#test()
