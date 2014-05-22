from SvnConfiguration import SvnConfiguration
from Configuration import Configuration
from AppConfigStore import AppConfigStore
from AppConfig import AppConfig
from App import App
from Args import Args
import os
import Log

class EnvContext:
    WORK_DIR_NAME="work"

    def __init__(self, conf):
        self.init(conf)
    
    def init(self, args):
        self.args = args
        self.configName = args.getOption(Args.OPTION_CONFIG)
        if not os.path.isfile(self.configName):
            Log.error(self.configName + " not exist.")
            raise Exception, "not found ["+self.configName+"] config"

        self.conf = Configuration()
        self.conf.load(self.configName)

        self.svnConf = SvnConfiguration()
        self.svnConf.load(self.configName)

        apps = self.args.getOption(Args.OPTION_APPS)
        if apps == None:
            self.appIds = self.conf.getList("apps")
        else:
            self.appIds = apps.split(",")

    	if(self.appIds == None or len(self.appIds) == 0):
	        self.appIds = self.svnConf.listAllPath()


        print "svn appIds=", ",".join(self.appIds)

        self.initHomeDir();
        workDirName = self.conf.get("work.dir", EnvContext.WORK_DIR_NAME)
        self.workDir = self.homeDir+"/"+workDirName
        self.logDir = self.conf.get("log.dir",self.homeDir+"/logs")

    def initHomeDir(self):
        home = self.args.getOption(Args.OPTION_USERHOME)
        if home == None:
            home = self.conf.get("user.home",os.environ['HOME'])

        self.homeDir = home

    def getArgs(self):
        return self.args

    def getWorkDir(self):
        return self.workDir

    def getLogDir(self):
        if not os.path.exists(self.logDir):
           os.makedirs(self.logDir)
        return self.logDir

    def getHomeDir(self):
        return self.homeDir

    def setAppIds(self, apps):
        self.appIds = apps

    def getAppIds(self):
        return self.appIds
    
    def getConf(self):
        return self.conf

    def getSvnConf(self):
        return self.svnConf

    def getAppLocalPath(self, appName):
#        print "aaaaaaaaa",self.svnConf
        return self.svnConf.getLocalPath(appName)
    
    def buildApp(self, appId):
        app = App(appId)
        app.init(self)
        return app

    def getAppConfig(self, appId):
        return AppConfigStore.getAppConfig(appId)

    def getConfFile(self):
        return self.configName
   

#test()

