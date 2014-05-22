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

class CDHome(CommandBase):
    def init(self):
        self._commandName = "cdhome"
        self._help = "cd {user.home}" 

    def run(self, envContext):
        #cmd = "source cd "+envContext.getHomeDir()
        cmd = "cd "+envContext.getHomeDir()
        return self.execCommandStdout(envContext, cmd)

