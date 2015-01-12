#!/usr/bin/python

import Log
import re

class SvnModule:
    def __init__(self,module, localPath, app, svn):
        self.module=module;
        self.localPath=localPath
        self.app=app
        self.svn=svn

        s = "http://svn.alibaba-inc.com/repos/ali_sourcing/system/business/(.*)"
#        s += "/[(business)|(technology)]/(.*)"
        s += "/[(branches)|(tags)|(trunk)]"
        rcompile = re.compile(s)
        rs = rcompile.search(svn)
 #r       print svn,"XXXXXXX",rs
        if rs != None:
            self.bizPath = rs.group(1)
#            print self.bizPath,"========"

    def getApp(self):
        return self.app
    def getBizPath(self):
        return self.bizPath
    def getModule(self):
        return self.module
    def getLocalPath(self):
        return self.localPath
    def getSvn(self):
        return self.svn
        
class RuleConf:
    def __init__(self,ruleReStr, moduleExpr, pathExpr, appExpr):
        self.ruleRe=None
        self.moduleExpr=moduleExpr
        self.pathExpr=pathExpr
        self.appExpr=appExpr
        self._buildRe(ruleReStr)

    def _buildRe(self, reStr):
        s = "http://svn.alibaba-inc.com/repos/"
        s += reStr
        s += "/[(branches)|(tags)|(trunk)]"
        self.ruleRe = re.compile(s)

    def parseSvnModule(self, svnUrl):
        rs = self.ruleRe.search(svnUrl)
        if rs != None:
		    module = eval(self.moduleExpr)
		    path = eval(self.pathExpr)
		    app = eval(self.appExpr)
		    svnModule = SvnModule(module, path, app, svnUrl)
		    return svnModule
        else:
		    return None

class SvnConfiguration:

    def __init__(self):
        self.svnPreList=[]
        self.svnPreModuleList=[]
        self.svnList=[]
        self.svnModuleList=[]
        self.rules=[]
        self._initParseRule()

    def _initParseRule(self):
##http://svn.alibaba-inc.com/repos/ali_sourcing/system/business/shipping/apps/web/intl-shippingbops/branches/20130815_281635_3
        self.rules.append(RuleConf("ali_sourcing/system/business/(.*)/apps(.*)/(.*)","rs.group(1)","rs.group(3)","rs.group(3)"))
        self.rules.append(RuleConf("ali_sourcing/system/business/(.*)/modules(.*)/(.*)","rs.group(1)","rs.group(1)+'/'+rs.group(3)","rs.group(3)"))
        self.rules.append(RuleConf("ali_sourcing/system/business/(.*)/open(.*)/(.*)","rs.group(1)","rs.group(1)+'/'+rs.group(3)","rs.group(3)"))
        
        self.rules.append(RuleConf("ali_sourcing/system/technology/(.*)/apps(.*)/(.*)","rs.group(1)","rs.group(3)","rs.group(3)"))
        self.rules.append(RuleConf("ali_sourcing/system/technology/(.*)/modules(.*)/(.*)","rs.group(1)","rs.group(1)+'/'+rs.group(3)","rs.group(3)"))
        self.rules.append(RuleConf("ali_sourcing/system/technology/(.*)/open(.*)/(.*)","rs.group(1)","rs.group(1)+'/'+rs.group(3)","rs.group(3)"))

        self.rules.append(RuleConf("ali_sourcing/open/(.*)","rs.group(1)","'open/'+rs.group(1)","rs.group(1)"))
        self.rules.append(RuleConf("ali_sourcing/share/biz/(.*)","rs.group(1)","'biz/'+rs.group(1)","rs.group(1)"))
        self.rules.append(RuleConf("ali_sourcing/share/(.*)","rs.group(1)","rs.group(1)","rs.group(1)"))

        self.rules.append(RuleConf("ali_sourcing/apps/web/(.*)","rs.group(1)","rs.group(1)","rs.group(1)"))
        self.rules.append(RuleConf("ali_sourcing/apps/service/(.*)","rs.group(1)","rs.group(1)","rs.group(1)"))
        self.rules.append(RuleConf("ali_sourcing/apps/modules/(.*)/(.*)","rs.group(1)","rs.group(1)+'/'+rs.group(2)","rs.group(2)"))

        self.rules.append(RuleConf("ali_platform/(.*)/(.*)/(.*)","rs.group(1)","rs.group(3)","rs.group(3)"))
        
        self.rules.append(RuleConf("ali_sourcing/sandbox/wangxingyong/(task-plan)","rs.group(1)","rs.group(1)","rs.group(1)"))
        self.rules.append(RuleConf("ali_sourcing/system/peconfig/(.*)","rs.group(1)","rs.group(1)","rs.group(1)"))
        
	
    def load(self, filename):
#        print "load file:",filename
        if filename == None:
            return
        try:
            fp = open(filename)
            self. _read(fp)
        except IOError:
            Log.error("read SvnConfiguration error filename= "+filename)
            raise Exception, "read SvnConfiguration error filename= "+filename
        fp.close()
#        print "=======",self.svnList
##parse svn moule
        for svnUrl in self.svnList:
	        module = self._parseSvnModule(svnUrl)
#	        print "====",module
#	        localPaths.append(module.getLocalPath())
                if module != None:
         	        self.svnModuleList.append(module)

#		print "svn modules,",self.svnModuleList
##parse svn pre moule

        for svnUrl in self.svnPreList:
	        module = self._parseSvnModule(svnUrl)
#           print "====",module
#	        localPaths.append(module.getLocalPath())
	        self.svnPreModuleList.append(module)

        

    def getSvnPre(self, appName):
        return self._findMoule(self.svnPreModuleList, appName).getSvn()

    def getBizPath(self, appName):
        return self._findMoule(self.svnModuleList, appName).getBizPath()
    
    def getSvn(self, appName):
#        print "Module :",self._findMoule(self.svnModuleList, appName)
        return self._findMoule(self.svnModuleList, appName).getSvn()

    def getLocalPath(self, appName):
#        print "getLocalPath",appName,self
        svnUrl = self.getSvn(appName)
#        print "SvnConfiguration svnUrl",appName, svnUrl
        if svnUrl == None:
            svnUrl = self.getSvnPre(appName)
        if svnUrl == None:
            return None
#        return self._parseLocalPath(svnUrl)
#        print svnUrl
        module = self._parseSvnModule(svnUrl)
#        print "====",module
        return module.getLocalPath()

    def listAllPath(self):
	    localPaths=[]
	    for module in self.svnModuleList:
         	 localPaths.append(module.getLocalPath())
	    return localPaths

    def _parseSvnModule(self,svnUrl):
        for reConf in self.rules:
            module = reConf.parseSvnModule(svnUrl)
#            print module
            if module != None:
                return module

        return None
        
    def _parseLocalPath(self,svnUrl):
## old       pp = re.compile("(http://svn.alibaba-inc.com/repos/ali_intl/apps/)(.*)/[(branches)|(tags)|(trunk)]")
## wrong        pp = re.compile("(http://svn.alibaba-inc.com/repos/[(ali_intl_share/share/)|(ali_sourcing/share/)|(ali_intl_share/)|(ali_sourcing/apps/web/)])(.*)/[(branches)|(tags)|(trunk)]")
        reStr = "("
        reStr += "http://svn.alibaba-inc.com/repos/"
        reStr += "("

        reStr += "ali_sourcing/system/business/"
        reStr += "|ali_sourcing/system/technology/data_processing/apps/"
        reStr += "|ali_sourcing/system/technology/data_processing/modules/"
        reStr += "|ali_sourcing/system/technology/"
        reStr += "|ali_sourcing/system/peconfig/"
        reStr += "|ali_sourcing/open/"
        reStr += "|ali_intl_share/share/"
        reStr += "|ali_sourcing/share/"
        reStr += "|ali_sourcing/apps/(?!web/)"
        reStr += "|ali_intl_share/"
        reStr += "|ali_sourcing/apps/web/"
        reStr += "|ali_platform/doris/"
        reStr += "|ali_platform/mock/"
        reStr += ")"
        reStr += ")"
        reStr += "(.*)"
        reStr += "/[(branches)|(tags)|(trunk)]"
#	print reStr;
        ##pp = re.compile("(http://svn.alibaba-inc.com/repos/(ali_sourcing/system/business/|ali_sourcing/system/technology/|ali_sourcing/open/|ali_intl_share/share/|ali_sourcing/share/|ali_sourcing/apps/(?!web/)|ali_intl_share/|ali_sourcing/apps/web/))(.*)/[(branches)|(tags)|(trunk)]")
        pp = re.compile(reStr)
#http://svn.alibaba-inc.com/repos/ali_sourcing/system/business/authentication/modules/assessment/trunk/
        rs = pp.search(svnUrl)
        if rs:
#            print rs.group(3)
            return rs.group(3)
#            return None
        else:
            return None

    def _findMoule(self, svnModuleList, appName):
#        print "findModule",appName
        if appName == None:
            return None    
        for module in svnModuleList:
            lp = module.getLocalPath()
#            print "find module", lp,appName,lp.find(appName)
            if lp==appName or lp.find(appName) != -1:
#                print "zhao dao module",module
                return module
        return None

    def _findAppSvn(self, svnList, appName):
        if appName == None:
            return None

        # http://svn.alibaba-inc.com/repos/ali_intl/apps/intl-biz/consign/branches/20101123_26249_1
        # consign+/
        #key = appName.replace('-','/') + "/";
        key = appName
        for svn in svnList:
            index = svn.find(key)
            if index != -1:
                return svn

        return None

    def _read(self, fp):
        currentList=None

        while True:
            line = fp.readline()
            if not line:
                break
            # comment or blank line?
            if line.strip() == '' or line[0] in '#;':
                continue

            line = line.strip()

            if line == "[svn.pre]":
                currentList = self.svnPreList
            elif line == "[svn]":
                currentList = self.svnList
            elif line[0] == '[' and line != "[svn]" and line != "[svn.pre]":
                currentList = None
            elif currentList == None:
                continue            
            else:
#		print line
                currentList.append(line)


def test():
    c = SvnConfiguration()
    c.load("work.config")
    s = c.getSvn("myalibaba")
    print s
    s = c.getSvn("commons-udas")
    print s

    s = c.getSvnPre("myalibaba")
    print s
    s = c.getSvnPre("commons-udas")
    print s

def testLocalPath():
    c = SvnConfiguration()
    c.load("work.config")
    path = c.getLocalPath("udas");
    print path
    path = c._parseLocalPath("http://svn.alibaba-inc.com/repos/ali_intl/apps/intl-biz/consign/branches/20101123_26249_1");
    print path
    path = c._parseLocalPath("http://svn.alibaba-inc.com/repos/ali_intl/apps/intl-biz/consign/tags/20101123_26249_1");
    print path
    path = c._parseLocalPath("http://svn.alibaba-inc.com/repos/ali_intl/apps/intl-commons/udas/branches/20101216_26249_4");
    print path
    path = c._parseLocalPath("http://svn.alibaba-inc.com/repos/ali_intl/apps/intl-standalone/databrusher/branches/20101216_26249_4");
    print path
    path = c._parseLocalPath("http://svn.alibaba-inc.com/repos/ali_intl/apps/intl-standalone/databrusher/av/av/tags/20101216_26249_4");
    print path


def testLocalPathNew():
    c = SvnConfiguration()
#    c.load("work.config")
#    path = c.getLocalPath("udas");
#    print path
    path = c._parseLocalPath("http://svn.alibaba-inc.com/repos/ali_sourcing/apps/web/intl-login/branches/20110518_55841_5");
    print path
    path = c._parseLocalPath("http://svn.alibaba-inc.com/repos/ali_intl_share/intl-resources/branches/20110518_55841");
    print path
    path = c._parseLocalPath("http://svn.alibaba-inc.com/repos/ali_sourcing/share/biz/account/impl/branches/20110518_55841_4");
    print path
    path = c._parseLocalPath("http://svn.alibaba-inc.com/repos/ali_intl_share/share/web/biz/branches/20110518_55841_4");
    print path
    path = c._parseLocalPath("http://svn.alibaba-inc.com/repos/ali_sourcing/apps/standalone/ganges/branches/20110518_55841_4");
    print path
    path = c._parseLocalPath("http://svn.alibaba-inc.com/repos/ali_sourcing/system/business/authentication/modules/assessment/trunk/");
    print path
    path = c._parseLocalPath("http://svn.alibaba-inc.com/repos/ali_sourcing/system/technology/data_processing/apps/intl-dp-admin/trunk/");
    print path
    path = c._parseLocalPath("http://svn.alibaba-inc.com/repos/ali_sourcing/system/business/shipping/apps/web/intl-shippingbops/branches/20120917_178565_1");
    print path
    path = c._parseLocalPath("http://svn.alibaba-inc.com/repos/ali_sourcing/system/business/shipping/modules/biz/tracking/branches/20120917_178565_1");
    print path

def parseSvn(svn):
	rules = []
	rules.append("ali_sourcing/system/business/(.*)/modules(.*)/(.*)")
	rules.append("ali_sourcing/system/business/(.*)/apps(.*)/(.*)")
	for r in rules:
		reStr = "http://svn.alibaba-inc.com/repos/"
		reStr += r
		reStr += "/[(branches)|(tags)|(trunk)]"
		pp = re.compile(reStr)
		rs = pp.search(svn)
		if rs != None:
			return rs.groups()
	
	return None


def testParseSvn():
    sc = SvnConfiguration()
    svn="http://svn.alibaba-inc.com/repos/ali_sourcing/system/business/shipping/modules/biz/tracking/branches/20120917_178565_1"
    print parseSvn(svn)
    m = sc._parseSvnModule(svn)
    print m,m.getApp(),m.getModule(),m.getLocalPath()
    svn="http://svn.alibaba-inc.com/repos/ali_sourcing/system/business/shipping/modules/tracking/branches/20120917_178565_1"
    print parseSvn(svn)
    m = sc._parseSvnModule(svn)
    print m,m.getApp(),m.getModule(),m.getLocalPath()
    svn="http://svn.alibaba-inc.com/repos/ali_sourcing/system/business/shipping/modules/biz/abc/tracking/branches/20120917_178565_1"
    print parseSvn(svn)
    m = sc._parseSvnModule(svn)
    print m,m.getApp(),m.getModule(),m.getLocalPath()
    svn="http://svn.alibaba-inc.com/repos/ali_sourcing/system/business/shipping/apps/web/intl-shippingma/branches/20120917_178565_1"
    print parseSvn(svn)
    m = sc._parseSvnModule(svn)
    print m,m.getApp(),m.getModule(),m.getLocalPath()
    svn="http://svn.alibaba-inc.com/repos/ali_sourcing/open/assessment-crm/trunk"
    m = sc._parseSvnModule(svn)
    print m,m.getApp(),m.getModule(),m.getLocalPath()
    svn="http://svn.alibaba-inc.com/repos/ali_sourcing/share/biz/column/trunk"
    m = sc._parseSvnModule(svn)
    print m,m.getApp(),m.getModule(),m.getLocalPath()
    svn="http://svn.alibaba-inc.com/repos/ali_sourcing/apps/web/intl-aisn/trunk"
    m = sc._parseSvnModule(svn)
    print m,m.getApp(),m.getModule(),m.getLocalPath()
    svn="http://svn.alibaba-inc.com/repos/ali_sourcing/apps/modules/globalseo/admin/trunk"
    m = sc._parseSvnModule(svn)
    print m,m.getApp(),m.getModule(),m.getLocalPath()

def testString():
    bp ="shipping/modules/tracking"
    print bp.rindex("/"),bp[0:16]
#test()
#testLocalPath()

#testLocalPathNew()

#testString()

#testParseSvn()

