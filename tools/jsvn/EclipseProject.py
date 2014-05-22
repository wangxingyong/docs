#!/usr/bin/python
import os
from EclipseProjectClasspath import EclipseProjectClasspath
from ProjectXml import ProjectXml

class EclipseProject:
    def __init__(self, eclipsEprojectsPath, eclipseProjectName):
        self._initSuccess = True;
        self.eclipsEprojectsPath = eclipsEprojectsPath
        self.eclipseProjectName = eclipseProjectName
        self._parseLocation()
        self._initClassPath()
        self._initMaven()

    def isInitSuccess(self):
        return self._initSuccess

    def getEclipseProjectName(self):
        return self.eclipseProjectName

    def _parseLocation(self):
        locationPath = self.eclipsEprojectsPath+"/"+self.eclipseProjectName+"/.location"
        if(not os.path.exists(locationPath)):
            self._initSuccess = False;
            return

        f = file(locationPath)
        buf = f.read(1024)
        s = buf.index("URI//file:")
        e = buf.index('\x00'+'\x00'+'\x00')
        self.projectRealDir = buf[s+10 : e]
#	print         self.projectRealDir
        f.close()

    def _initClassPath(self):
        if(not self._initSuccess):
            return

        classpathFile = self.projectRealDir+"/.classpath"
        if(not os.path.exists(classpathFile)):
            self._initSuccess = False;
            return

        self.classpath = EclipseProjectClasspath(classpathFile)

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


