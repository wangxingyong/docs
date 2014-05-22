#!/usr/bin/python

# -*- coding: cp936 -*-
import re
import os
import Util
import httplib

def workDirSvnInfo(workDir):
    cmd = "svn info "+workDir
    sr = Util.doCommandSubprocess(cmd)
    if (sr == None) or (not sr.isSucceed):
        return None

    return info_url(sr.out)

def info_url(svnInfo):
    p = re.compile('^URL: (.*)$',re.M)  
    m = p.search(svnInfo)
    if m:
        return m.group(1)
    else:
        return None

def svnIsTrunk(svnUrl):
    if svnUrl.endswith("/trunk") or svnUrl.endswith("/trunk/"):
        return True
    return False

def logInfo_firstVersion(svnUrl):
    sr = Util.doCommandSubprocess("svn log --stop-on-copy "+svnUrl)
    if (sr == None) or (not sr.isSucceed):
        return None

    svnLogInfo = sr.out
    p = re.compile('^r(\d{3,20})\s{1,5}',re.M)  
    #m = p.findall(svnLogInfo)
    version = None
    for m in p.finditer(svnLogInfo):
        version = m.group(1)

    return version



def svnUrlExist(svnUrl):
    path=svnUrl[26:1000]+"/"
    conn = httplib.HTTPConnection("svn.alibaba-inc.com")
    conn.putrequest("GET", path)
    conn.putheader("Authorization","Basic eGluZ3lvbmcud2FuZ3h5Ondhbmd4aW4=")
    conn.endheaders()
    r1 = conn.getresponse()

    if r1.status==httplib.OK:
        return True
    else:
        #print r1.status, r1.reason
        return False


def svnMergeConflicts(dryMergeResult):
    p = re.compile('^\s{0,10}C\s{1,10}.*$',re.M)
    cs = ""
    for m in p.finditer(dryMergeResult):
        cs += m.group()+"\n"

    if len(cs) == 0:
        return None

    return cs


"""
class SysResult:
    def __init__(self):
        self.isSucceed = False
        self.out = None
        self.error = None

def doSubprocess(cmd):
    print "exec command : ",cmd
    
    sr = SysResult()
    try:
        out = os.popen(cmd);
        sr.isSucceed = True
        sr.out = out.read()
    except Exception, e:
        print "error info: ", e
        sr.isSucceed = False
    finally:
        pass


    print "exec command end , isSucceed=",sr.isSucceed
    return sr

"""
def test():
    s = workDirSvnInfo("~/work4/work/intl-myalibaba")
    print s
    print s=="http://svn.alibaba-inc.com/repos/ali_intl/apps/intl-myalibaba/tags/20100312_R_RELEASE"

#    sr = doSubprocess("cd /usr/ali/alibaba/work/intl-myalibaba/deploy; svn info")
#    s = sr.out+"          doSubprocess"
#    s = info_url(s)    

#    sr = Util.doCommand("svn log --stop-on-copy ~/work4/work/intl-myalibaba")
#    s = sr.out+"          doSubprocess"
#    s = logInfo_firstVersion(s)
    s = logInfo_firstVersion("~/work4/work/intl-myalibaba")
    print s
    dryMergeResult = """
cd /home/leo/work0/work/intl-base; svn merge --dry-run -r 214677:HEAD http://svn.alibaba-inc.com/repos/ali_intl/apps/intl-base/branches/200100107_afterPay_Dev3/
C1    project.xml
  G    project.xml
  C1    project.xml
    C1    project.xml
 G   .
Summary of conflicts:
  Text conflicts: 1
"""
    cs = svnMergeConflicts(dryMergeResult)
    print cs

#test()



#r = svnUrlExist("http://svn.alibaba-inc.com/repos/ali_intl/apps/intl-myalibaba/trunk")
#print r
