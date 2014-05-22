#!/usr/bin/python
import os
import Util
import time

class EclipseProjectClasspath:
    def __init__(self, classpathFile):
        self._isReplace = False
        self.classpathFile = classpathFile
        self.entrys=[]
        self._parseClassPath()

    def _parseClassPath(self):
        try:
            fp = open(self.classpathFile)
            self. _read(fp)
        except IOError:
            Log.error("read SvnConfiguration error filename= "+filename)
            raise Exception, "read SvnConfiguration error filename= "+filename
        fp.close()

    def replaceProject(self, groupArtifactIdPath, eclipseProjectName):
        if groupArtifactIdPath == None:
            return

        for i, en in enumerate(self.entrys):
            index = en.find("/"+groupArtifactIdPath+"/")
#            index = en.find(groupArtifactIdPath)
            if index != -1 :
                self._isReplace = True
#                print "found lib entry=",en
                projectEntry = "       <classpathentry combineaccessrules=\"false\" kind=\"src\" path=\"/"+eclipseProjectName+"\"/>"

                self.entrys[i] = projectEntry

    def _hasContain(self, projectEntry):
        for en in self.entrys:
            if en.endswith(projectEntry):
                return True
        return False

    def replaceClasspath(self):
        if self._isReplace:
	    nowTime=time.strftime('%Y-%m-%d_%H-%M-%S',time.localtime(time.time()))
            cmd = "cp "+self.classpathFile+" "+self.classpathFile+".bak."+nowTime
            Util.doCommandSystem(cmd)

            file_object = open(self.classpathFile, 'w')
	    for line in self.entrys:
		file_object.write(line)
		file_object.write("\n")
#####file_object.writelines(self.entrys)
            file_object.close
    

    def _read(self, fp):
        while True:
            line = fp.readline()
            if not line:
                break
            line = line.strip()
            self.entrys.append(line)
##	print self.entrys

def test():
   c = EclipseProjectClasspath("/wxy/my_work_home/work1/work/intl-bopsassembly/biz/crm/.classpath.bak")
   c.replaceProject("alibaba.intl.bopsassembly.biz.commons","a_b_c")
   print c._isReplace
   c.replaceClasspath()

##test()
