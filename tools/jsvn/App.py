#!/usr/bin/python
from AppConfigStore import AppConfigStore
from AppConfig import AppConfig
from ProjectXml import ProjectXml
from Configuration import Configuration
from SvnConfiguration import SvnConfiguration
import os

class App:
    WORK_DIR_NAME="work"

    def __init__(self, appId="app"):
        self._localPath = None
        self._releasePath = None
        self.id = appId
    
    def init(self, envContext):
        self.envContext = envContext

        if AppConfigStore.hasAppConfig(self.id):
            self.appConfig = AppConfigStore.getAppConfig(self.id)
        else:
            self.appConfig = AppConfig(self.id)

        self.rootConf = envContext.getConf()
        self.svnConf = envContext.getSvnConf()

#        self.userHome = self.__getValue("user.home","/home/leo/work0")
#        workDirName = self.__getValue("work.dir",App.WORK_DIR_NAME)
#        self.workDir = self.userHome+"/"+workDirName+"/"+self.appConfig.getWorkDir()

        self.userHome = self.envContext.getHomeDir()

        message=self.__getValue("message")
        self.cpMessage=self.__getValue("message.cp",message)
        self.ciMessage=self.__getValue("message.ci",message)

###        print "sssssss"
        self.svn = self.__buildSvnPath("svn")
        self.svnPre = self.__buildSvnPath("svn.pre")
###        print "s222222",self.svn,self.svnPre
        localPath = self._getLocalPath(self.appConfig.getWorkDir())
#        print "local path: ",localPath
        self.workDir = self.userHome+"/work/"+localPath
        self.mergeDir = self.userHome+"/merge/"+localPath


    def __getValue(self, key, default=None):
#        print "sssssssssss333",self.id,key
        if self.rootConf.hasKey(self.id+"."+key):
            return self.rootConf.get(self.id+"."+key)
        elif self.rootConf.hasKey(key):
            return self.rootConf.get(key)
        else:
            return default
        
    def __buildSvnPath(self, svnKey):
#        print "buildSvnPath===",svnKey
        svn=self.__getValue(svnKey)
#        print "buildSvnPath===",svn
        if svn == None or svn == "":
            return self.appConfig.getTrunk()
        
        if svn.startswith("http://"):
            return svn;

        if svn.startswith("/"):
            svn = svn[1:1000]

        if svn.startswith("tags"):
            return self.appConfig.getSvn()+"/"+svn;

        if svn.startswith("branches"):
            return self.appConfig.getSvn()+"/"+svn;

        return self.appConfig.getSvn()+"/branches/"+svn

    def _getLocalPath(self, defaultPath = None):
#        print "ddddddddd",self.svnConf
        if self._localPath == None:
#            print "localPath from svn conf: ",self.id
            localPath = self.svnConf.getLocalPath(self.id)
#            print "localPath from svn conf: ",localPath
            if localPath == None:
                self._localPath = ""
            else:
                self._localPath = localPath

        if self._localPath == "":
            return defaultPath
        else:
            return self._localPath

    def getProperty(self, key, default):
        return self.__getValue(key, default)

    def getEnvContext(self):
        return self.envContext

    def getAppConfig(self):
        return self.appConfig

    def getId(self):
        return self.id

    def getWorkDir(self):
        return self.workDir

    def getMergeDir(self):
        return self.mergeDir

    def getAllDir(self):
        return self.workDir+"/all"

    def getDeployDir(self):
        return self.workDir+"/deploy"

    def getReleasePathMaven(self, defaultPath = None):
        if self._releasePath == None:
            releasePath = None
            mavnProject = ProjectXml("MAVEN")
            if self.isBiz():
                mavenXmlFile = os.path.join(self.workDir, "pom.xml")
            else:
                mavenXmlFile = os.path.join(self.workDir,"all", "pom.xml")

#            print mavenXmlFile

            if mavnProject.parse(mavenXmlFile):
                releasePath = mavnProject.getProjectPath()
            else:
                releasePath = defaultPath

#            print "getReleasePathMaven(): ",releasePath
            if releasePath == None:
                self._releasePath = ""
            else:
                self._releasePath = releasePath

        if self._releasePath == "":
            return defaultPath
        else:
            return self._releasePath

    def getReleasePath(self, defaultPath = None):
        if self._releasePath == None:
            releasePath = None
            mavnProject = ProjectXml("MAVEN")
            mavenXmlFile = os.path.join(self.workDir, "pom.xml")
            if mavnProject.parse(mavenXmlFile):
                releasePath = mavnProject.getProjectPath()
                releasePath = "/.m2/repository/"+releasePath
            else:
                antxProject = ProjectXml("ANTX")
                antxXmlFile = os.path.join(self.workDir, "project.xml")
                if antxProject.parse(antxXmlFile):
                    releasePath = antxXmlFile.getProjectPath()
                    releasePath = "/.antx/repository.project/"+releasePath

            if releasePath == None:
                self._releasePath = ""
            else:
                self._releasePath = releasePath

        if self._releasePath == "":
            return defaultPath
        else:
            return self._releasePath

    def getReleaseDir(self):
        releasePath = self.getReleasePath()
        if releasePath == None:
            return self.userHome + "/.antx/repository.project/" + self.appConfig.getReleaseDir()
        else:
            return self.userHome + releasePath

    def getHomeDir(self):
        return self.userHome

    def getSvn(self):
        svn = self.svnConf.getSvn(self.id)
        if svn == None:
            return self.svn
        else:
            return svn

    def getSvnPre(self):
        svnPre = self.svnConf.getSvnPre(self.id)
        if svnPre == None:
            return self.svnPre
        else:
            return svnPre

    def getCPMessage(self):
        return self.cpMessage

    def getCIMessage(self):
        return self.ciMessage

    def isBiz(self):
#        print self.getAllDir()
        if not os.path.exists(self.getAllDir()):
            return True
        else:
            return False

#test()

