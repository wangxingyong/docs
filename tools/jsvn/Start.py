#!/usr/bin/python
from AppConfigStore import AppConfigStore
import sys
from Main import Main
from Args import Args
import traceback

configDir = "/home/wxy/svn-config"

args = Args(sys.argv)

args.getCommand("help")

config=""
configName = args.getOption(Args.OPTION_CONFIG, "config")
if(configName.isdigit()):
    home = "/home/leo/work"+configName
    config = home+"/jsvn.config"
    args.addOption(Args.OPTION_USERHOME, home)
##    config = configDir+"/"+"work"+configName
elif configName.startswith("/"):
    config = configName
else:
    config = configDir+"/"+configName

args.addOption(Args.OPTION_CONFIG, config)

AppConfigStore.build(configDir+"/apps.cfg")
try:
	main = Main(args)
	main.execute()
except Exception, e:
	exstr = traceback.format_exc(),"======"
	print exstr
except Error, e:
	exstr = traceback.format_exc(),"======"
	print exstr

