#!/usr/bin/python
import os
from IdeaProjectClasspath import IdeaProjectClasspath
from ProjectXml import ProjectXml

class IdeaProject:
    def __init__(self, envContext, ideaImlPath):
    	self.envContext = envContext
        self._initSuccess = True;
        self.ideaImlPath = ideaImlPath.replace("$PROJECT_DIR$", self.envContext.getHomeDir())
        self.ideaProjectName = None
        self._parseLocation()
        self._initClassPath()
        self._initMaven()

    def isInitSuccess(self):
        return self._initSuccess

    def getIdeaProjectName(self):
        return self.ideaProjectName

    def _parseLocation(self):
        realImlPath = self.ideaImlPath
        
        if(not os.path.exists(realImlPath)):
            self._initSuccess = False;
            return
#$PROJECT_DIR$/work/shipping/carrier/modules.shipping.carrier.iml
        ia = realImlPath.rfind('/')
        self.projectRealDir = realImlPath[0:ia]
       	self.ideaProjectName = realImlPath[ia+1:len(realImlPath)-4]


    def _initClassPath(self):
        if(not self._initSuccess):
            return

        self.classpath = IdeaProjectClasspath(self.ideaImlPath, self)

    def _initMaven(self):
        if(not self._initSuccess):
            return

        mavenXml = self.projectRealDir+"/pom.xml"
        if(not os.path.exists(mavenXml)):
            self._initSuccess = False;
            return

        self.maven = ProjectXml()
        self.maven.parse(mavenXml)

    def getClasspath(self):
        return self.classpath

    def getProjectRealDir(self):
        return self.projectRealDir

    def getGroupArtifactIdPath(self):
        return self.maven.getGroupArtifactIdPath()


