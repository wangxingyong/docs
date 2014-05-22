#!/usr/bin/python
from Configuration import  ConfigParser
from CommandFactory import CommandFactory
import CommandStore
from Configuration import Configuration
from EnvContext import EnvContext
import Command
import Log
import os

class Main:

    def __init__(self, args):
        self.init(args)

    def init(self, args):
        self.args = args
        self.envContext = EnvContext(args)
        Log.init(self.envContext)
        self._loginfo()

    def _loginfo(self):
        Log.info("config file:" + self.envContext.getConfFile())
        Log.info("user home dir:" + self.envContext.getHomeDir())
        Log.info("===========================================")

    def execute(self):
        commandName = self.args.getCommand()
        command = CommandFactory.getCommand(commandName)
        if command == None:
            Log.error("not found command : "+ commandName)
            return

        Log.info("exec command : \""+commandName+"\"")

        command.run(self.envContext)





