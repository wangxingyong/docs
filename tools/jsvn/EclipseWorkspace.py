#!/usr/bin/python
import os
from EclipseProject import EclipseProject
from EclipseProjectClasspath import EclipseProjectClasspath

class EclipseWorkspace:
    def __init__(self, eclipseWorkspace):
        self.eclipseWorkspace = eclipseWorkspace
        self.projects=[]
        self._parseProjects()

    def _parseProjects(self):
        projectsPath = self.eclipseWorkspace+"/.metadata/.plugins/org.eclipse.core.resources/.projects"
        ps = os.listdir(projectsPath)
        for p in ps:
            if p.startswith("."):
                continue

            project = EclipseProject(projectsPath, p)

            if(project.isInitSuccess()):
                self.projects.append(project)

    def doReplaceProject(self):
        for project in self.projects:
#            if not (project.getEclipseProjectName() == "alibaba.intl.bopsassembly.biz.crm-1.0-SNAPSHOT"):
#                continue
#            print project.getProjectRealDir()
            self._replaceProjectClassPath(project)

    def _replaceProjectClassPath(self, project):
        cp = project.getClasspath();
        for p in self.projects:
            groupArtifactIdPath = p.getGroupArtifactIdPath()
            eclipseProjectName = p.getEclipseProjectName()
            cp.replaceProject(groupArtifactIdPath, eclipseProjectName)

        cp.replaceClasspath()

def test():
    workspace="/home/leo/work1/assessment_2_0_yi_qi_2011-12-12_16-24-12_workspace"
    ep = EclipseWorkspace(workspace)
    ep.doReplaceProject()
