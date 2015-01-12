#!/usr/bin/python
# -*- coding: gbk -*-
from Configuration import Configuration
from Command import CommandBase
from AppConfig import AppConfig
from App import App
from EnvContext import EnvContext
import Util
import Svn
import os
import Log

## work,merge
def processDefaultWorkDir(envContext, app, paramValue, default):
    toDir = envContext.getArgs().getParameter(0, None)
    dirName = None
    if toDir == paramValue:
        dirName = paramValue
    else:
        dirName = default

    if dirName == "work":
        return app.getWorkDir()
    elif dirName == "merge":
        return app.getMergeDir()
    else:
        return None

class CP(CommandBase):
    def init(self):
        self._commandName = "cp"
        self._help = "svn cp" 

    def runApp(self, envContext, app):
        appConfig = app.getAppConfig()
        if Svn.svnUrlExist(app.getSvn()):
            print app.getSvn(),", is exist"
            sr = Util.SysResult()
            sr.isSucceed = True
            return sr

        cpLog = envContext.getLogDir()+"/cp.txt"
        f = open(cpLog, "aw")
        f.write(app.getId()+"\n"+app.getSvn()+"\n")

        cmd = "svn cp "+appConfig.getTrunk()+" "+app.getSvn()+" -m "+app.getCPMessage()
        return self.execCommandFile(envContext, cmd, app.getId())

class CO(CommandBase):
    def init(self):
        self._commandName = "co"
        self._help = "svn check out [param0=merge, default=work]" 

    def runApp(self, envContext, app):
#        print "app111===="
        appConfig = app.getAppConfig()
        workDir = processDefaultWorkDir(envContext, app, "merge", "work")

        if os.path.islink(workDir) or os.path.isfile(workDir):
            os.remove(workDir)

        if os.path.isdir(workDir):
            print workDir,", dir is exist, check out error."
            sr = Util.SysResult()
            sr.isSucceed = True
            return sr


        cmd = "svn co "+app.getSvn()+" "+workDir

#        Log.info("jsvn co: "+cmd)

        toDir = envContext.getArgs().getParameter(0, None)
        if "work" == toDir or toDir == None:
            bizDir = self.bizDir(app)
            if bizDir != None:
                cmd += "; cd "+envContext.getHomeDir()+"/work; mkdir -p biz_folder/"+bizDir+"; cd biz_folder/"+bizDir+"; ln -s "+workDir

        Log.info("jsvn co: "+cmd)
        return self.execCommandFile(envContext, cmd, app.getId())
    
    def bizDir(self, app):
        bizPath = app.getBizPath()
        if bizPath == None:
            return None
        i = bizPath.rindex("/")
        return bizPath[0:i]


class ST(CommandBase):
    def init(self):
        self._commandName = "st"
        self._newThread = False
        self._help = "svn st [param0=work, default=merge]" 

    def runApp(self, envContext, app):
        appConfig = app.getAppConfig()
        workDir = processDefaultWorkDir(envContext, app, "work", "merge")
        cmd = "svn st "+workDir
        Log.info("-------------svn st--------------" + workDir)
        sr = self.execCommandFile(envContext, cmd, app.getId())
        print sr.out
        return sr

class CI(CommandBase):
    def init(self):
        self._commandName = "ci"
        self._help = "svn ci [param0=work, default=merge]" 

    def runApp(self, envContext, app):
        appConfig = app.getAppConfig()
        workDir = processDefaultWorkDir(envContext, app, "work", "merge")
        if not os.path.exists(workDir):
            print workDir,", dir not exist"
            sr = Util.SysResult()
            sr.isSucceed = True
            return sr

        cmd = "cd "+workDir+"; svn ci -m '"+app.getCIMessage()+"'"
        return self.execCommandFile(envContext, cmd, app.getId())

class MergeCI(CommandBase):
    def init(self):
        self._commandName = "mergeci"
        self._help = "svn ci -m last_svn_address [param0=work, default=merge]" 

    def runApp(self, envContext, app):
        appConfig = app.getAppConfig()
        workDir = processDefaultWorkDir(envContext, app, "work", "merge")
        if not os.path.exists(workDir):
            print workDir,", dir not exist"
            sr = Util.SysResult()
            sr.isSucceed = True
            return sr

        cmd = "cd "+workDir+"; svn ci -m 'merge from:"+app.getSvnPre()+"'"
        return self.execCommandFile(envContext, cmd, app.getId())


class UP(CommandBase):
    def init(self):
        self._commandName = "up"
        self._newThread = False
        self._help = "svn up [param0=merge, default=work]" 

    def runApp(self, envContext, app):
        appConfig = app.getAppConfig()
        workDir = processDefaultWorkDir(envContext, app, "merge", "work")
        if not os.path.exists(workDir):
            print workDir,", dir not exist"
            sr = Util.SysResult()
            sr.isSucceed = True
            return sr

        cmd = "svn up "+workDir
        return self.execCommandFile(envContext, cmd, app.getId())

class SW(CommandBase):
    def init(self):
        self._commandName = "sw"
        self._newThread = False
        self._help = "svn sw [param0=merge, default=work]" 

    def runApp(self, envContext, app):
        appConfig = app.getAppConfig()
        workDir = processDefaultWorkDir(envContext, app, "merge", "work")
        if not os.path.exists(workDir):
            print workDir,", dir not exist"
            sr = Util.SysResult()
            sr.isSucceed = True
            return sr

        u = Svn.workDirSvnInfo(workDir)
        if u==None:
            print workDir,", is not svn dir"
            return
        elif u== app.getSvn():
            cmd = "cd "+workDir+"; svn up"
        else:
            cmd = "cd "+workDir+"; svn sw "+app.getSvn()

        return self.execCommandFile(envContext, cmd, app.getId())

class DryMerge(CommandBase):
    op = "MergeConflicts_"

    def init(self):
        self._commandName = "drymerge"
        self._newThread = False
        self._help = "svn dry merge [param0=work, default=merge]" 


    def runApp(self, envContext, app):
        appConfig = app.getAppConfig()
        workDir = processDefaultWorkDir(envContext, app, "work", "merge")
        if not os.path.exists(workDir):
            print workDir,", dir not exist"
            sr = Util.SysResult()
            sr.isSucceed = True
            return sr

        if Svn.svnIsTrunk(app.getSvnPre()):
            firstVersion = Svn.logInfo_firstVersion(app.getSvn())
        else:
            firstVersion = Svn.logInfo_firstVersion(app.getSvnPre())

        if firstVersion==None:
            print app.getSvnPre(),", url is wrong"
            sr = Util.SysResult()
            sr.isSucceed = False
            return sr

        cmd = "cd "+workDir+"; svn merge --dry-run -r "+firstVersion+":HEAD "+app.getSvnPre()
        Log.info("-------------dryMerge--------------" + workDir)
        sr = self.execCommandFile(envContext, cmd, app.getId())
        if (sr == None) or (not sr.isSucceed):
            return sr

        cs = Svn.svnMergeConflicts(sr.out)
        if cs == None:
            print app.getId()," no conflicts"
            if hasConflicts(envContext, app):
                os.remove(conflictsFileName)
        else:
            drymergeOp = DryMerge.op + app.getId()
            logFileName = Util.saveLog(envContext, drymergeOp, cs)
            print app.getId()," has conflicts, please check, conflicts: ",logFileName

        return sr

def hasConflicts(envContext, app):
    conflictsFileName = Util.getLogFileName(envContext, DryMerge.op + app.getId())
    if os.path.exists(conflictsFileName):
        return True
    else:
        return False

class Merge(CommandBase):
    def init(self):
        self._commandName = "merge"
        self._newThread = False
        self._help = "svn merge [param0=work, default=merge]" 

    def runApp(self, envContext, app):
        appConfig = app.getAppConfig()
        workDir = processDefaultWorkDir(envContext, app, "work", "merge")
        if not os.path.exists(workDir):
            print workDir,", dir not exist"
            sr = Util.SysResult()
            sr.isSucceed = True
            return sr

        if hasConflicts(envContext, app):
            print app.getId()," has conflicts, please check, dir: ",app.getWorkDir()
            return None

        if Svn.svnIsTrunk(app.getSvnPre()):
            firstVersion = Svn.logInfo_firstVersion(app.getSvn())
        else:
            firstVersion = Svn.logInfo_firstVersion(app.getSvnPre())

        if firstVersion==None:
            print app.getSvnPre(),", url is wrong"
            sr = Util.SysResult()
            sr.isSucceed = False
            return sr

        cmd = "cd "+workDir+"; svn merge -r "+firstVersion+":HEAD "+app.getSvnPre()
        Log.info("-------------merge--------------" + workDir)
        return self.execCommandFile(envContext, cmd, app.getId())

class MergeRm(CommandBase):
    def init(self):
        self._commandName = "mergerm"
        self._newThread = False
        self._help = "rm -rf $home/merge/*" 

    def puteCommand(self,commandName):
        return commandName +" :"+ Help.SPACE[0:30-len(commandName)]

    def run(self, envContext):
        cmd = "rm -rf "+envContext.getHomeDir()+"/merge/*"
#        print cmd
        sr = Util.doCommandSystem(cmd)
        return sr

def test():
    conf = Configuration()
    conf.load("config")
    env = EnvContext.build(conf,"myalibaba")
    Help()
    CP().run(env)
    CO().run(env)
    

#test()


