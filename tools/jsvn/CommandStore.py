#!/usr/bin/python

from CommandFactory import CommandFactory
import Command
import CommandSvn
import CommandAntx
import CommandBash
import CommandMaven

def initCommand():
    CommandFactory.registerCommand(Command.Help())
#    CommandFactory.registerCommand(Command.CommandGroup())
#    CommandFactory.registerCommand(Command.GoHome())
    CommandFactory.registerCommand(Command.OpenConfig())
    CommandFactory.registerCommand(Command.RmLogs())
    CommandFactory.registerCommand(Command.ResetWorkSpace())
    CommandFactory.registerCommand(Command.NewWorkSpace())
    
#    CommandFactory.registerCommand(Command.ResetLocalRepository())
#    CommandFactory.registerCommand(Command.ResetLocalRepositoryAntx())
    CommandFactory.registerCommand(Command.MsgWorkSpace())
#    CommandFactory.registerCommand(Command.EclipseClasspathProjectReplace())
    CommandFactory.registerCommand(Command.IdeaClasspathProjectReplace())
#    CommandFactory.registerCommand(Command.CopyCommons())
#    CommandFactory.registerCommand(Command.OpenOutLog())


#    CommandFactory.registerCommand(CommandSvn.CP())
    CommandFactory.registerCommand(CommandSvn.CO())
    CommandFactory.registerCommand(CommandSvn.ST())
    CommandFactory.registerCommand(CommandSvn.CI())
    CommandFactory.registerCommand(CommandSvn.UP())
    CommandFactory.registerCommand(CommandSvn.SW())
    CommandFactory.registerCommand(CommandSvn.DryMerge())
    CommandFactory.registerCommand(CommandSvn.Merge())
    CommandFactory.registerCommand(CommandSvn.MergeRm())
    CommandFactory.registerCommand(CommandSvn.MergeCI())

    CommandFactory.registerCommand(CommandMaven.MavenInstall())
    CommandFactory.registerCommand(CommandMaven.Idea())
    CommandFactory.registerCommand(CommandMaven.Eclipse())
#    CommandFactory.registerCommand(CommandMaven.EclipseProject())

#    CommandFactory.registerCommand(CommandMaven.MavenInstallToAntx())

#    CommandFactory.registerCommand(CommandAntx.UpdateAllRepository())
#    CommandFactory.registerCommand(CommandAntx.CopyRepository2())
#    CommandFactory.registerCommand(CommandAntx.UpdateRepository2())
#    CommandFactory.registerCommand(CommandAntx.UpdateCommonResource())
#    CommandFactory.registerCommand(CommandAntx.UpdateRepository())
#    CommandFactory.registerCommand(CommandAntx.Eclipse())
#    CommandFactory.registerCommand(CommandAntx.AntxClean())
#    CommandFactory.registerCommand(CommandAntx.AntxRelease())
#    CommandFactory.registerCommand(CommandAntx.AntxAll())
#    CommandFactory.registerCommand(CommandAntx.AntxDeploy())
#    CommandFactory.registerCommand(CommandAntx.StartApp())
#    CommandFactory.registerCommand(CommandAntx.StopApp())

#    CommandFactory.registerCommand(CommandBash.CDHome())


if __name__ == 'CommandStore':
    initCommand()

