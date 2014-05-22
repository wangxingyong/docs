#!/usr/bin/python

import os
import string
import xml.sax
from xml.sax.handler import *

LOG_LEVEL = "info"

def log(msg):
    if LOG_LEVEL == "debug":
        print "log:", msg

import codecs
import io
class ProjectHandlerBase:

    def __init__(self):
        self._id = None
        self._groupId = None
        self._artifactId = None
        self._version = None
        self.init()

    def init(self):
        pass

    def _processFile(self, xmlFile):
        return xmlFile;

    def parseXml(self, xmlFile):
        log(xmlFile)
        if not os.path.exists(xmlFile):
            return False
        source = self._processFile(xmlFile)
        parser = xml.sax.make_parser()
        parser.setContentHandler(self)
        parser.parse(source)
        self.checkData()
        return True

    def checkData(self):
        if self._groupId == None:
            print "error project group id. artifactId=",self._artifactId
            self._groupId =self._groupId_parent

    def getProjectId(self):
        return self._id

    def getProjectPath(self):
        return self._groupId+self._artifactId+self._version

class AntxProjectHandler(ProjectHandlerBase,ContentHandler):
    def _processFile(self, xmlFile):
        f = codecs.open(xmlFile,'r','utf8')
        sUtf8 = f.read()
        f.close()
        f = io.StringIO(sUtf8)
        return f;

    def startElement(self, name, attrs):
        if "project" == name:
            self._id = attrs.getValue("id")
            self._groupId = self._id

    def getProjectPath(self):
        return self._groupId.replace(".","/")

class MavenProjectHandler(ProjectHandlerBase,ContentHandler):
    
    def init(self):
        self._level = 0
        self._isParent = False
        self._currName = None

    def startElement(self, name, attrs):
        self._level = self._level + 1
#        print self._level, name

        if "groupId" == name:
            self._currName = "groupId"
        if "artifactId" == name:
            self._currName = "artifactId"
        if "version" == name:
            self._currName = "version"

    def characters(self, data): 
        if self._level == 2 and self._currName != None:
            if "groupId" == self._currName:
                self._groupId = data
                log("groupId value:"+data)
            if "artifactId" == self._currName:
                self._artifactId = data
                log("artifactId value:"+data)
            if "version" == self._currName:
                self._version = data
                log("version value:"+data)
        if self._level == 3 and self._currName != None:
            if "groupId" == self._currName:
                self._groupId_parent = data
#                print "ddddddd11",self._groupId_parent
                log("groupId value:"+data)
            if "artifactId" == self._currName:
                self._artifactId_parent = data
                log("artifactId value:"+data)
            if "version" == self._currName:
                self._version_parent = data
                log("version value:"+data)

    def endElement(self, name):
        self._level = self._level - 1
        self._currName = None

    def getProjectPath(self):
#        print "ddddddddddddddd",self._groupId,self._artifactId, self._version
        groupPath = self._groupId.replace(".","/")
        log("groupPath, "+groupPath)
        path = os.path.join(groupPath, self._artifactId, self._version)
        return path


class ProjectXml:
    TYPE_ANTX = "ANTX"
    TYPE_MAVEN = "MAVEN"

    def __init__(self, projectType="MAVEN"):
        if ProjectXml.TYPE_ANTX == projectType:
            self._projectHandler = AntxProjectHandler()
        else:
            self._projectHandler = MavenProjectHandler()

    def parse(self, xmlFile):
        return self._projectHandler.parseXml(xmlFile)

    def getProjectPath(self):
        log(self._projectHandler)
        return self._projectHandler.getProjectPath()

    def getArtifactId(self):
        return self._projectHandler._artifactId

    def getVersion(self):
        return self._projectHandler._version

    def getGroupId(self):
        return self._projectHandler._groupId

    def getGroupPath(self):
        return self._projectHandler._groupId.replace(".","/")
    
    def getGroupArtifactIdPath(self):
        if self._projectHandler._groupId == None:
            return None

        groupPath = self._projectHandler._groupId.replace(".","/")
        log("groupPath, "+groupPath)
        path = os.path.join(groupPath, self._projectHandler._artifactId)
        return path
    


def testAntx():
    antx = AntxProjectHandler()
    antx.parseXml('/home/leo/work0/work/intl-biz/consign/project.xml')
    path = antx.getProjectPath()
    print path

def testMaven():
    maven = MavenProjectHandler()
    maven.parseXml('/home/leo/work0/work/intl-biz/consign/pom.xml')
    path = maven.getProjectPath()
    print path
def testProjectXml():
    project = ProjectXml("ANTX")
    project.parse("/home/leo/work0/work/intl-biz/consign/project.xml")
    print project.getProjectPath()

    project = ProjectXml("MAVEN")
    project.parse("/home/leo/work0/work/intl-biz/consign/pom.xml")
    print project.getProjectPath()

#testAntx()
#testMaven()
#testProjectXml()

