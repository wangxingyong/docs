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

class UpdateAllRepository(CommandBase):
    def init(self):
        self._commandName = "uprepository12"
        self._help = "svn up repository.project, repository, intl-base" 

    def run(self, envContext):
        cmd = "cd /usr/ali/alibaba/.antx/repository.project ; svn up; cd /usr/ali/antx/repository; svn up; cd /usr/ali/alibaba/work/intl-base/; svn up"
        return self.execCommandFile(envContext, cmd)

class UpdateCommonResource(CommandBase):
    def init(self):
        self._commandName = "upresource"
        self._help = "svn up commons, resources, templates, statictpl" 

    def run(self, envContext):
        cmd = "cd /usr/ali/alibaba/work ; svn up intl-commons; svn up intl-resources; svn up intl-templates; svn up statictpl;"
        return self.execCommandFile(envContext, cmd)


class CopyRepository2(CommandBase):
    def init(self):
        self._commandName = "cprepository2"
        self._help = "copy Repository2 to home" 

    def run(self, envContext):
        cmd = "copyRepository "+envContext.getHomeDir()
        return self.execCommandFile(envContext, cmd)

class UpdateRepository2(CommandBase):
    def init(self):
        self._commandName = "uprepository2"
        self._help = "svn up repository.project,intl-base, copy Repository2 to home" 

    def run(self, envContext):
        cmd = "cd /usr/ali/alibaba/.antx/repository.project ; svn up; svn up "+envContext.getWorkDir()+"/intl-base; copyRepository "+envContext.getHomeDir()
        return self.execCommandFile(envContext, cmd)


class UpdateRepository(CommandBase):
    def init(self):
        self._commandName = "uprepository"
        self._help = "uprepository [1 or 2 or all] default 2" 

    def run(self, envContext):
        r = envContext.getArgs().getParameter(0, "2")
        if r == "1":
            cmd = "svn up "+envContext.getWorkDir()+"/intl-base; cd /usr/ali/antx/repository; svn up;"
        elif r == "2":
            cmd = "svn up "+envContext.getWorkDir()+"/intl-base; cd /usr/ali/alibaba/.antx/repository.project; svn up;"
        elif r == "all":
            cmd = "svn up "+envContext.getWorkDir()+"/intl-base; cd /usr/ali/alibaba/.antx/repository.project ; svn up; cd /usr/ali/antx/repository; svn up;"
        else:
            print "uprepository [1 or 2 or all] default 2" 
            return

        return self.execCommandFile(envContext, cmd)


class Eclipse(CommandBase):
    def init(self):
        self._commandName = "eclipseantx"
        self._help = "antx eclipse  all " 

    def runApp(self, envContext, app):
        appConfig = app.getAppConfig()
        if appConfig.isWeb() or appConfig.isWebBiz():
            cmd = "cd "+app.getAllDir()+";antx reactor goals=eclipse"
            return self.execCommandStdout(envContext, cmd, app.getId())
        else:
            return None

class EclipseBak(CommandBase):
    def init(self):
        self._commandName = "eclipse"
        self._help = "antx eclipse  all " 

    def runApp(self, envContext, app):
        appConfig = app.getAppConfig()
        if appConfig.isWeb() or appConfig.isWebBiz():
            cmd = "cd "+app.getAllDir()+";antx reactor goals=eclipse"
        else:
            cmd = "cd "+app.getWorkDir()+";antx eclipse"

        return self.execCommandStdout(envContext, cmd, app.getId())

class AntxClean(CommandBase):
    def init(self):
        self._commandName = "antxclean"
        self._help = "antx clean" 

    def runApp(self, envContext, app):
        appConfig = app.getAppConfig()
        if appConfig.isWeb() or appConfig.isWebBiz():
            cmd = "cd "+app.getAllDir()+";antx reactor goals=clean"
        else:
            cmd = "cd "+app.getWorkDir()+";antx clean"

        return self.execCommandStdout(envContext, cmd, app.getId())

class AntxRelease(CommandBase):
    def init(self):
        self._commandName = "antxr"
        self._help = "rm -rf release.dir; antx -p RELEASE" 

    def runApp(self, envContext, app):
        appConfig = app.getAppConfig()
        sr = None
        if appConfig.isBiz():
            cmd = "rm -rf "+app.getReleaseDir()+"/*; cd "+app.getWorkDir()+";antx -p RELEASE"
            sr = self.execCommandFile(envContext, cmd, app.getId())

        return sr


class AntxAll(CommandBase):
    def init(self):
        self._commandName = "antxall"
        self._help = "cd all , antx" 

    def runApp(self, envContext, app):
        appConfig = app.getAppConfig()
        sr = None
        if appConfig.isWeb() or appConfig.isWebBiz():
            cmd = "cd "+app.getAllDir()+";antx"
            sr = self.execCommandStdout(envContext, cmd, app.getId())

        return sr

class AntxDeploy(CommandBase):
    def init(self):
        self._commandName = "antxdeploy"
        self._help = "cd deploy, antx" 

    def runApp(self, envContext, app):
        appConfig = app.getAppConfig()
        sr = None
        if appConfig.isWeb():
            cmd = "cd "+app.getDeployDir()+";antx"
            sr = self.execCommandStdout(envContext, cmd, app.getId())

        return sr

class StartApp(CommandBase):
    def init(self):
        self._commandName = "startws"
        self._help = "bin/startws" 

    def runApp(self, envContext, app):
        appConfig = app.getAppConfig()
        sr = None
        if appConfig.isWeb():
            cmd = app.getDeployDir()+"/bin/startws"
            sr = self.execCommandStdout(envContext, cmd, app.getId())

        return sr

class StopApp(CommandBase):
    def init(self):
        self._commandName = "killws"
        self._help = "bin/killws" 

    def runApp(self, envContext, app):
        appConfig = app.getAppConfig()
        sr = None
        if appConfig.isWeb():
            cmd = app.getDeployDir()+"/bin/killws"
            sr = self.execCommandStdout(envContext, cmd, app.getId())

        return sr


def test():
    conf = Configuration()
    conf.load("config")
    env = EnvContext.build(conf,"myalibaba")
    Help()
    CP().run(env)
    CO().run(env)
    

#test()


