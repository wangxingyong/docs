#!/usr/bin/python
# -*- coding: gbk -*-
from Configuration import Configuration
from ProjectXml import ProjectXml
from CommandFactory import CommandFactory
from AppConfig import AppConfig
from App import App
from EnvContext import EnvContext
from Runner import Runable
from Runner import Runner
from Util import SysResult
from LinkerDir import LinkerDir
import Util
import Svn
import os
import sys
import Log
import time
from EclipseWorkspace import EclipseWorkspace
from IdeaWorkspace import IdeaWorkspace

class AppRun(Runable):
    def __init__(self, envContext, command, app):
        self.envContext = envContext
        self.command = command
        self.app = app

    def run(self):
        self.command.runApp(self.envContext, self.app)

    
class CommandBase:

    def __init__(self):
        self._newThread = True
        self._commandName = "command"
        self._help = "command desc"
        self.init()

    def init(self):
        pass

    def setNewThread(self, newThread):
        self._newThread = newThread

    def getCommandName(self):
        return self._commandName

    def getHelp(self):
        return self._help

    def run(self, envContext):
        self.envContext = envContext
        for appId in envContext.getAppIds():
#            print "run:",appId
            self.execOne(envContext, appId)

	self._endRun(envContext)

    def _endRun(self, envContext):
	pass

    def execOne(self, envContext, appId):
        try:
#	    print appId,"------"
            app = envContext.buildApp(appId)
#            print "execOne",app,self._newThread
            if self._newThread:
                ra = AppRun(envContext, self, app)
                Runner(ra).start()
            else:
#		print app, self
                self.runApp(envContext, app)

        except Exception, e:
            print "exception stack:",e
#            raise e
            print e,sys.exc_info()[0],sys.exc_info()[1],sys.exc_info()[2]
            Log.error("exec: ["+appId+"] error")
        finally:
            pass


    def runApp(self, envContext, app):
        print "====",app,sys.exc_info()
        print app.getSvn()
        print "work dir : ", envContext.getWorkDir()

    def execCommandStdout(self, envContext, cmd, subName=""):
        Log.debug("exec ["+self.getCommandName()+", "+ subName + "]: start")
        sr = Util.doCommandSystem(cmd)
        Log.debug("exec ["+self.getCommandName()+", "+ subName + "]: end ,  isSucceed="+str(sr.isSucceed))
        self._logOutput(envContext, cmd, subName, sr)
        return sr

    def execCommandFile(self, envContext, cmd, subName=""):
        Log.debug("exec ["+self.getCommandName()+", "+ subName + "]: start")
        sr = Util.doCommandSubprocess(cmd)
        Log.debug("exec ["+self.getCommandName()+", "+ subName + "]: end ,  isSucceed="+str(sr.isSucceed))
        self._logOutput(envContext, cmd, subName, sr)
        return sr

    def _logOutput(self, envContext, cmd, subName, sr):
        commandKey = self.getCommandName()+"_"+subName
        Util.execOutput(cmd, sr, envContext, commandKey)

class Help(CommandBase):
    SPACE="                                                                              "
    def init(self):
        self._commandName = "help"
        self._help = "list this help info." 

    def puteCommand(self,commandName):
        return commandName +" :"+ Help.SPACE[0:30-len(commandName)]

    def run(self, envContext):
        allCommands = CommandFactory.getAllCommands()
        keys = allCommands.keys()
        keys.sort()
        print "useage: jsvn -c configName -apps app1,app2 commandName parameter1 parameter1\n"
        for key in keys:
            print "\t",self.puteCommand(key),allCommands[key].getHelp()

        sr = Util.SysResult()
        sr.isSucceed = True
        return sr

class GoHome(CommandBase):
    def init(self):
        self._commandName = "gohome"
        self._help = "go to user home." 

    def run(self, envContext):
        cmd = "nautilus "+envContext.getHomeDir()
        sr = Util.doCommandSystem(cmd)
        return sr

class OpenConfig(CommandBase):
    def init(self):
        self._commandName = "openconf"
        self._help = "open conf file." 
    def run(self, envContext):
        cmd = "gedit "+envContext.getConfFile()+" &"
        return self.execCommandStdout(envContext, cmd)

class OpenOutLog(CommandBase):
    def init(self):
        self._commandName = "openlog"
        self._help = "open up out log file." 
    def runApp(self, envContext, app):
        cn = envContext.getArgs().getParameter(0,"st")
        logOut = envContext.getLogDir()+"/"+cn+"_"+app.getId()+"_out.log"
        if os.path.isfile(logOut):
            cmd = "gedit "+ logOut + "&"
            return self.execCommandStdout(envContext, cmd, app.getId())
        else:
            return None

class RmLogs(CommandBase):
    def init(self):
        self._commandName = "rmlog"
        self._help = "rm logs" 
    def run(self, envContext):
        cmd = "rm -rf "+envContext.getLogDir()+"/*; mkdir -p "+envContext.getLogDir()
        return self.execCommandFile(envContext, cmd)


class ResetWorkSpace(CommandBase):
    def init(self):
        self._commandName = "resetwork"
        self._help = "reset work space" 
    def run(self, envContext):
        msg = envContext.getArgs().getParameter(0, None)
        if msg==None:
            print "pelease set message param..."
            return

        nowTime=time.strftime('%Y-%m-%d_%H-%M-%S',time.localtime(time.time()))
        msg=msg+"_"+nowTime
        cmd = "resetWorkSpaceIDEA "+envContext.getHomeDir()+" "+ msg+";"

        rs = self.execCommandStdout(envContext, cmd)
        return rs
"""
#        antxDest = envContext.getHomeDir()+"/.antx/repository.project"
#        antxLd = LinkerDir("/usr/ali/alibaba/.antx/repository.project", antxDest)
#        antxLd.linkDir()
#        antxLd.makeDir("alibaba/intl/biz/consign")
        loginUserHomeDir = os.environ['HOME']
        mavenDest = envContext.getHomeDir()+"/.m2/repository"
        self.execCommandStdout(envContext, "rm -rf "+mavenDest)
#        mavenLd = LinkerDir("/wxy/my_work_home/alibaba/.m2/repository", mavenDest)
        mavenLd = LinkerDir(loginUserHomeDir+"/.m2/repository", mavenDest)
        mavenLd.linkDir()

        ## intl app Working space between independent
        mavenLd.makeDir("com/alibaba/intl/app")
        mavenLd.makeDir("com/alibaba/intl/sourcing/shared")
        self.execCommandStdout(envContext, "rm -rf "+mavenDest+"/com/alibaba/intl/app")
        self.execCommandStdout(envContext, "rm -rf "+mavenDest+"/com/alibaba/intl/sourcing/shared")
       
        return rs
"""

class ResetLocalRepository(CommandBase):
    def init(self):
        self._newThread = False
        self._commandName = "resetlocalrepository"
        self._help = "reset current pom Local Repository  or jsvn resetlocalrepository app" 
        self.mavenLd = None

    def run(self, envContext):
        mavenDest = envContext.getHomeDir()+"/.m2/repository"
        self.execCommandStdout(envContext, "rm -rf "+mavenDest)
        loginUserHomeDir = os.environ['HOME']
        self.mavenLd = LinkerDir(loginUserHomeDir+"/.m2/repository", mavenDest)

        ## intl app Working space between independent
        self.mavenLd.makeDir("com/alibaba/intl/app")
        self.mavenLd.makeDir("com/alibaba/intl/sourcing/shared")
        return
        ####
        self.envContext = envContext

        args = self.envContext.getArgs()
        if args.hasOption("app"):
            for appId in envContext.getAppIds():
                self.execOne(envContext, appId)
        else:
            cwd = os.getcwd()
            if not os.path.exists(cwd+"/pom.xml") :
                print cwd, " not found pom.xml"
                return;
            project = ProjectXml("MAVEN")
            project.parse(cwd+"/pom.xml")
            releasePath = project.getProjectPath()
            self._dirPath(releasePath)

    def runApp(self, envContext, app):
#        print app.isBiz(),app.getId()
        releasePath = app.getReleasePathMaven()
        self._dirPath(releasePath)

    def _dirPath(self, releasePath):
#        print releasePath,111
        self.mavenLd.makeDir(releasePath)

class ResetLocalRepositoryAntx(CommandBase):
    def init(self):
        self._newThread = False
        self._commandName = "resetlocalrepositoryantx"
        self._help = "reset Local Repository antx" 
        self.antxLd = None

    def run(self, envContext):
        antxDest = envContext.getHomeDir()+"/.antx/repository.project"
        self.antxLd = LinkerDir("/usr/ali/alibaba/.antx/repository.project", antxDest)
        self.envContext = envContext
        for appId in envContext.getAppIds():
            self.execOne(envContext, appId)

    def runApp(self, envContext, app):
        if app.isBiz():
            releasePath = app.getAppConfig().getReleaseDir()
            self.antxLd.makeDir(releasePath)

class MsgWorkSpace(CommandBase):
    def init(self):
        self._commandName = "msg"
        self._help = "work message" 
    def run(self, envContext):
        cmd = "echo ----------message: `basename "+envContext.getHomeDir()+"/*.readme`;"
        return self.execCommandStdout(envContext, cmd)


class CopyCommons(CommandBase):
    def init(self):
        self._commandName = "cpcommon"
        self._help = "copy commans project" 
    def run(self, envContext):
        app = envContext.getApp()
        appConfig = envContext.getAppConfig()
        cmd = "copyCommons "+app.getHomeDir()
        return self.execCommandStdout(envContext, cmd)

class CommandGroup(CommandBase):
    def init(self):
        self._commandName = "group"
        self._help = "jsvn group command1 command2 command3" 

    def run(self, envContext):
        self.envContext = envContext
        for appId in envContext.getAppIds():
            self.execOne(envContext, appId)

    def run(self, envContext):
        cmdIds = envContext.getArgs().getParameters()
        if cmdIds == None or len(cmdIds) == 0:
            print "command error. jsvn group command1 command2 command3"
            return

        for cmdId in cmdIds:
            cmd = CommandFactory.getCommand(cmdId)
            if cmd == None:
                print cmdId, " command not found. jsvn group command1 command2 command3"
                return

        self.envContext = envContext
        self.cmdIds = cmdIds
        for appId in envContext.getAppIds():
            self.execOne(envContext, appId)
        return

    def runApp(self, envContext, app):
        for cmdId in self.cmdIds:
            cmd = CommandFactory.getCommand(cmdId)
            cmd.setNewThread(False)
            cmd.runApp(self.envContext, app)

class EclipseClasspathProjectReplace(CommandBase):
    def init(self):
        self._newThread = False
        self._commandName = "eclipseclasspath"
        self._help = "replace ecipse classpath to project" 

    def run(self, envContext):
        workspace = envContext.getHomeDir()+"/inner_workspace"
        ep = EclipseWorkspace(workspace)
        ep.doReplaceProject()

class IdeaClasspathProjectReplace(CommandBase):
    def init(self):
        self._newThread = False
        self._commandName = "ideaclasspath"
        self._help = "replace ecipse classpath to project" 

    def run(self, envContext):
        workspace = envContext.getHomeDir()+"/inner_workspace"
        ep = IdeaWorkspace(workspace, envContext)
        ep.doReplaceProject()

def main():
    Help()
    ResetWorkSpace()
    
if __name__ == '__main__':
    main()


def run():
    GoHome()
    Help()
    CopyCommons()
    OpenConfig()
    ResetWorkSpace()
    
if __name__ == '1Command':
    run()
