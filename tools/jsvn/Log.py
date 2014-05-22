#!/usr/bin/python
import os
logFile = None

def init(envContext):
    logDir=envContext.getLogDir()
    if not os.path.exists(logDir):
        os.makedirs(logDir)

    log = logDir+"/log.txt"
    info("log file: " + log)
    global logFile
    logFile = open(log, "aw")

def _file(msg):
    if logFile != None:
        logFile.write(msg+"\n")


def info(msg):
    s = "[info]: " + msg
    _file(s)
    print s

def debug(msg):
    s = "[debug]: " + msg
    _file(s)
    print s

def error(msg):
    s = "[error]: " + msg
    _file(s)
    print s
