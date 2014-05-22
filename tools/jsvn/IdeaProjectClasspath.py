#!/usr/bin/python
import os
import Util
import time
import Log

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


class IdeaProjectClasspath:
    def __init__(self, ideaImlPath, ideaProject):
        self._isReplace = False
        self.ideaProject = ideaProject
        self.ideaImlPath = ideaImlPath
        self.entrys=[]
        self.ideaImlTree = None
        self._parseClassPath()

    def _parseClassPath(self):
    	self.ideaImlTree = ET.ElementTree(file=self.ideaImlPath)
        es = self.ideaImlTree.iterfind('component/orderEntry')
        for lib in es:
        	self.entrys.append(lib)


    def replaceProject(self, groupArtifactIdPath, ideaProjectName, project):
        if groupArtifactIdPath == None:
            return

        for i, en in enumerate(self.entrys):
        	if en.attrib['type'] == 'module-library':
	        	#print en.attrib
	        	jarUrl = en.find('library/CLASSES/root').attrib['url']
	        	
	        	index = jarUrl.find("/"+groupArtifactIdPath+"/")
	        	if index != -1 :
					self._isReplace = True
#                print "found lib entry=",en
					en.remove(en.find('library'))
					en.set('type','module')
					en.set('module-name', project.getIdeaProjectName())
					
					self.entrys[i] = en
#					print "=====",groupArtifactIdPath,ideaProjectName, jarUrl, project.getIdeaProjectName()

    def _hasContain(self, projectEntry):
        for en in self.entrys:
            if en.endswith(projectEntry):
                return True
        return False

    def replaceClasspath(self):
        if self._isReplace:
        	Log.info("classpath module: "+self.ideaProject.getIdeaProjectName())
        	
        	firstIdeaIml = self.ideaImlPath+".0"
        	if(not os.path.exists(firstIdeaIml)):
        		cmd0 = "cp "+self.ideaImlPath+" "+firstIdeaIml
        		Util.doCommandSystem(cmd0)

#	    	nowTime=time.strftime('%Y-%m-%d_%H-%M-%S',time.localtime(time.time()))
#	    	cmd = "cp "+self.ideaImlPath+" "+self.ideaImlPath+".bak."+nowTime
#	    	Util.doCommandSystem(cmd)

	    	tempIdeaIml = self.ideaImlPath+".temp"
	    	file_object = open(tempIdeaIml, 'w')
	    	self.ideaImlTree.write(file_object)
	    	file_object.flush()
	    	file_object.close()
	    	
	    	cmd2 = "cp "+tempIdeaIml+" "+self.ideaImlPath
	    	Util.doCommandSystem(cmd2)


##	print self.entrys

def test():
   c = IdeaProjectClasspath("/wxy/my_work_home/work1/work/intl-bopsassembly/biz/crm/.classpath.bak")
   c.replaceProject("alibaba.intl.bopsassembly.biz.commons","a_b_c")
   print c._isReplace
   c.replaceClasspath()

##test()


'''
	<orderEntry type="module" module-name="modules.shipping.order"/>  
    <orderEntry type="module-library"> 
      <library> 
        <SOURCES> 
          <root url="jar:///Users/leo/.m2/repository/com/alibaba/intl/sourcing/shared/modules.shipping.template/1.0.0/modules.shipping.template-1.0.0-sources.jar!/"/>
        </SOURCES>  
        <CLASSES>
          <root url="jar:///Users/leo/.m2/repository/com/alibaba/intl/sourcing/shared/modules.shipping.template/1.0.0/modules.shipping.template-1.0.0.jar!/"/>
        </CLASSES>
      </library> 
    </orderEntry>  
'''