#!/usr/bin/python
# -*- coding: gbk -*-
from Configuration import Configuration
from Command import CommandBase
from AppConfig import AppConfig
from App import App
from EnvContext import EnvContext
from LinkerDir import LinkerDir
import Util
import Svn
import os
import Log


class MavenAllPom(CommandBase):
    def init(self):
    	self._newThread = False
        self._commandName = "pom"
        self.allPomData="""<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/maven-v4_0_0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <artifactId>alibaba.intl.jsvn.all.pom</artifactId>
    <packaging>pom</packaging>
    <groupId>com.alibaba.intl.app</groupId>
    <version>1.0-SNAPSHOT</version>
    <name>jsvn_all</name>
    <description>jsvn all project</description>
    
    <modules>
"""

    def runApp(self, envContext, app):
        sr = None
        mavenDest = envContext.getHomeDir()+"/.m2/repository"
        mavenLd = LinkerDir("/wxy/my_work_home/alibaba/.m2/repository", mavenDest)
        appReleasePath = app.getReleasePathMaven();
#        print appReleasePath
#        return sr
        mavenLd.makeDir(appReleasePath)
        if app.isBiz():
	    self.allPomData += "<module>"+app.getWorkPath()+"/pom.xml</module>\n"
        else:
	    self.allPomData += "<module>"+app.getWorkPath()+"/all/pom.xml</module>\n"
        return sr

    def _endRun(self,envContext):
	self.allPomData +=     "\n</modules>"
	self.allPomData += "\n</project>"

#	print self.allPomData
	
	allPomFilePath = envContext.getWorkDir()+"/pom.xml"
	allPomFile = open(allPomFilePath, "w")
	allPomFile.write(self.allPomData+"\n")
	allPomFile.close()



class MavenBase(CommandBase):
    def init(self):
        self._newThread = False
        self.allPomData="""<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/maven-v4_0_0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <artifactId>alibaba.intl.jsvn.all.pom</artifactId>
    <packaging>pom</packaging>
    <groupId>com.alibaba.intl.app</groupId>
    <version>1.0-SNAPSHOT</version>
    <name>jsvn_all</name>
    <description>jsvn all project</description>
    
    <modules>
"""
#       <module>../web/pfs</module>
#   </modules>


    def runApp(self, envContext, app):
        sr = None
        mavenDest = envContext.getHomeDir()+"/.m2/repository"
        mavenLd = LinkerDir("/wxy/my_work_home/alibaba/.m2/repository", mavenDest)
        appReleasePath = app.getReleasePathMaven();
#        print appReleasePath
#        return sr
        mavenLd.makeDir(appReleasePath)
        if app.isBiz():
            self.allPomData += "<module>../../../../.."+app.getWorkDir()+"/pom.xml</module>\n"
        else:
            self.allPomData += "<module>../../../../.."+app.getWorkDir()+"/all/pom.xml</module>\n"
        return sr

    def _endRun(self,envContext):
        self.allPomData +=     "\n</modules>"
        self.allPomData += "\n</project>"

#   print self.allPomData
    
        allPomFilePath = envContext.getLogDir()+"/pom.xml"
        allPomFile = open(allPomFilePath, "w")
        allPomFile.write(self.allPomData+"\n")
        allPomFile.close()
        self._execCmd(envContext, envContext.getLogDir())
   
    def _execCmd(self,envContext, allPomDir):
        pass	


class Eclipse(MavenBase):
    def init(self):
	MavenBase.init(self)
        self._commandName = "eclipse"
        self._help = "mvn eclipse:eclpse -DdownloadSources=true" 

    def _execCmd(self,envContext, pomDir):
	cmd = "cd "+pomDir+ "; mvn eclipse:eclipse"
        sr = self.execCommandStdout(envContext, cmd, "eclipse")

    def runAppdddd(self, envContext, app):
        appConfig = app.getAppConfig()
        if app.isBiz():
            cmd = "cd "+app.getWorkDir()+ "; mvn eclipse:eclipse"
            sr = self.execCommandStdout(envContext, cmd, app.getId())
        else:
            cmd = "cd "+app.getWorkDir()+ "/all; mvn eclipse:eclipse"
            sr = self.execCommandStdout(envContext, cmd, app.getId())

        return sr

class Idea(MavenBase):
    def init(self):
	MavenBase.init(self)
        self._commandName = "idea"
        self._help = "mvn idea:module -DdownloadSources=true" 

    def _execCmd(self,envContext, pomDir):
	cmd = "cd "+pomDir+ "; mvn idea:module"
        sr = self.execCommandStdout(envContext, cmd, "idea")

    def runAppdddd(self, envContext, app):
        appConfig = app.getAppConfig()
        if app.isBiz():
            cmd = "cd "+app.getWorkDir()+ "; mvn idea:module"
            sr = self.execCommandStdout(envContext, cmd, app.getId())
        else:
            cmd = "cd "+app.getWorkDir()+ "/all; mvn idea:module"
            sr = self.execCommandStdout(envContext, cmd, app.getId())

        return sr


class EclipseProject(CommandBase):
    def init(self):
        self._commandName = "eclipseproject"
        self._help = "mvnproject eclipse:eclpse -DdownloadSources=true" 

    def runApp(self, envContext, app):
        appConfig = app.getAppConfig()
        if app.isBiz():
            cmd = "cd "+app.getWorkDir()+ "; mvnproject eclipse:eclipse"
            sr = self.execCommandStdout(envContext, cmd, app.getId())
        else:
            cmd = "cd "+app.getWorkDir()+ "/all; mvnproject eclipse:eclipse"
            sr = self.execCommandStdout(envContext, cmd, app.getId())

        return sr

class MavenInstall(MavenBase):
    def init(self):
	MavenBase.init(self)
        self._commandName = "install"
        self._help = "mvn clean install -Dmaven.test.skip -e" 
	
    def _execCmd(self,envContext, pomDir):
	cmd = "cd "+pomDir+ "; mvn clean install -Dmaven.test.skip -e"
#	print cmd
        sr = self.execCommandStdout(envContext, cmd, "pom")
	return sr
    
class MavenInstall__Old_thread(CommandBase):
    def init(self):
        self._commandName = "install"
        self._help = "mvn clean install -Dmaven.test.skip -e" 

    def runApp(self, envContext, app):
        sr = None
        mavenDest = envContext.getHomeDir()+"/.m2/repository"
        mavenLd = LinkerDir("/wxy/my_work_home/alibaba/.m2/repository", mavenDest)
        appReleasePath = app.getReleasePathMaven();
#        print appReleasePath
#        return sr
        mavenLd.makeDir(appReleasePath)
        if app.isBiz():
            cmd = "cd "+app.getWorkDir()+ "; mvn clean install -Dmaven.test.skip -e"
            sr = self.execCommandStdout(envContext, cmd, app.getId())
        else:
            cmd = "cd "+app.getWorkDir()+ "/all; mvn clean install -Dmaven.test.skip -e"
            sr = self.execCommandStdout(envContext, cmd, app.getId())
        return sr


class MavenInstallToAntx(CommandBase):
    def init(self):
        self._commandName = "installtoantx"
        self._help = "mvn a2m:install-antx-module-intl" 

    def runApp(self, envContext, app):
        sr = None
        if app.isBiz():
            cmd = "cd "+app.getWorkDir()+ "; mvn a2m:install-antx-module-intl -Dmaven.test.skip -e -Drepository.project="+app.getHomeDir()+"/.antx/repository.project"
            sr = self.execCommandStdout(envContext, cmd, app.getId())

        return sr


#test()


