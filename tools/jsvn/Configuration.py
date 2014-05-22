# -*- coding: cp936 -*-
import ConfigParser

"""
@staticmethod
SimClass.ShareStr()   #使用静态函数

@classmethod        #类方法修饰符


"""
class Configuration:

    DEFAULT_SECTION="config"

    def __init__(self, prefix=None, parser=None):
        self.prefix = prefix
        self.parser = parser
        self.configBlock = Configuration.DEFAULT_SECTION

    def setConfigBlock(self, configBlock):
        if configBlock == None:
            configBlock = Configuration.DEFAULT_SECTION
        self.configBlock = configBlock

    def load(self, confFile):
        self.confFile = confFile
        self.parser = ConfigParser.ConfigParser()
        self.parser.read(confFile)
        return self

    def getSub(self, prefix):
        prefix = self.__buildKey(prefix)
        conf = Configuration(prefix, self.parser)
        return conf

    def __buildKey(self, key):
        if self.prefix == None:
            return key
        else:
            return self.prefix+"."+key

    def hasKey(self, key):
        s = self.__buildKey(key)
        return self.parser.has_option(self.configBlock, s)
        
    def get(self, key, default=None):
        s = self.__buildKey(key)
        if self.parser.has_option(self.configBlock, s):
            return self.parser.get(self.configBlock, s)
        else:
            return default

    def getConfFile(self):
        return self.confFile

    def getList(self, key):
        v = self.get(key, None)
	if(v == None):
	    return None
        return v.split(",")

def testAppsConf():
    c = Configuration()
    c.load("apps.cfg")
    s = c.get("product.svn")
    print s


    aa = c.getSub("product")
    print aa.get("svn")
    print aa.getList("svn1")

def testAppConf():
    c = Configuration()
    c.setConfigBlock("svn.pre")
    c.load("work.config")
    print c.parser.options("svn.pre")
    print c.parser.items("svn.pre")


#testAppConf()

