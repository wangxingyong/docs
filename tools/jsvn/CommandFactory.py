#!/usr/bin/python

class CommandFactory:
    commands = {
    }
    
    @staticmethod
    def registerCommand(command):
        CommandFactory.commands[command.getCommandName()] = command
        
    @staticmethod
    def getCommand(commandId):
        if commandId not in CommandFactory.commands:
            return None
        
        command = CommandFactory.commands[commandId]
        return command

    @staticmethod
    def getAllCommands():
        return CommandFactory.commands


