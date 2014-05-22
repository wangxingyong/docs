from Configuration import Configuration

class AppConfig:
    
    def __init__(self, appId):
		self.id=appId
		self.conf=None
		self.svn=""
		self.workDir=""
		self.releaseDir=""
		self.allDir=""
		self.deployDir=""
    
    def init(self, conf):
        self.conf = conf
        self.svn=conf.get("svn")
        self.workDir=conf.get("workDir")
        self.releaseDir=conf.get("releaseDir")
        self.allDir=conf.get("allDir")
        self.deployDir=conf.get("deployDir")

    def getId(self):
        return self.id

    def getSvn(self):
        return self.svn

    def getTrunk(self):
        return self.svn+"/trunk"

    def getWorkDir(self):
        return self.workDir

    def getReleaseDir(self):
        if self.isBiz():
            return self.releaseDir
        return ""

    def getAllDir(self):
        if self.allDir != None:
            return self.allDir
        return ""

    def getDeployDir(self):
        if self.deployDir != None:
            return self.deployDir
        return ""

    def isBiz(self):
        return self.releaseDir != None

    def isWeb(self):
        return self.deployDir != None and self.allDir != None

    def isWebBiz(self):
        return self.deployDir == None and self.allDir != None

    def getProperty(self, key, default):
        if self.conf.hasKey(key):
            return self.conf.get(key)
        else:
            return default

def test():
    c = Configuration()
    c.load("apps.cfg")

    ac = AppConfig()

    conf = c.getSub("myalibaba")
    ac.init(conf)
    print ac.isBiz() ," false"
    print ac.isWeb() ," true"
    print ac.isWebBiz() ," false"

    print "=========="
    
    conf = c.getSub("product")       
    ac.init(conf)
    print ac.isBiz() ," true"
    print ac.isWeb() ," false"
    print ac.isWebBiz() ," false"

    print "=========="

    conf = c.getSub("bops")       
    ac.init(conf)
    print ac.isBiz() ," false"
    print ac.isWeb() ," false"
    print ac.isWebBiz() ," true"
    

#test()

