#!/usr/bin/python
import os
from IdeaProject import IdeaProject
from IdeaProjectClasspath import IdeaProjectClasspath
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


class IdeaWorkspace:
    def __init__(self, ideaWorkspace, envContext):
    	self.envContext = envContext
        self.ideaWorkspace = ideaWorkspace
        self.projects=[]
        self._parseProjects()

    def _parseProjects(self):
        moduleXmlFile = self.ideaWorkspace+"/.idea/modules.xml"
        tree = ET.ElementTree(file=moduleXmlFile)
        for m in tree.iterfind('component/modules/module'):
        	project = IdeaProject(self.envContext, m.attrib['filepath'])
        	if(project.isInitSuccess()):
        		self.projects.append(project)

    def doReplaceProject(self):
        for project in self.projects:
#            if not (project.getIdeaProjectName() == "alibaba.intl.bopsassembly.biz.crm-1.0-SNAPSHOT"):
#                continue
#            print project.getProjectRealDir()
            self._replaceProjectClassPath(project)

    def _replaceProjectClassPath(self, project):
        cp = project.getClasspath();
        for p in self.projects:
            groupArtifactIdPath = p.getGroupArtifactIdPath()
            ideaProjectName = p.getIdeaProjectName()
            cp.replaceProject(groupArtifactIdPath, ideaProjectName, p)

        cp.replaceClasspath()

def test():
    workspace="/home/leo/work1/assessment_2_0_yi_qi_2011-12-12_16-24-12_workspace"
    ep = IdeaWorkspace(workspace)
    ep.doReplaceProject()


'''
$PROJECT_DIR$/work/intl-shippingma/web/solution/alibaba.intl.shippingma.web.solution-1.0-SNAPSHOT.iml
$PROJECT_DIR$/work/shipping/carrier/modules.shipping.carrier.iml
$PROJECT_DIR$/work/shipping/order/modules.shipping.order.iml
'''