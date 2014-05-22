#!/usr/bin/python

class Args:
    OPTION_USERHOME = "userhome"
    OPTION_CONFIG = "c"
    OPTION_APPS = "apps"

    PARAM_KEY = "-param"

    def __init__(self, args=None):
        self.baseLine = None
        self.dataMap = {}
        self.command = None
        if args != None:
            self.parse(args)

    def getBaseLine(self):
        return self.baseLine

    def setCommand(self, commandName):
        self.command = commandName

    def getCommand(self, default=None):
        if self.command == None:
            self.command = default
            return default
        else:
            return self.command

    def getOption(self, option, default=None):
        if self.dataMap.get(option) == None:
            return default
        else:
            return self.dataMap.get(option)

    def hasOption(self, option):
        if self.dataMap.get(option) == None:
            return False
        else:
            return True
                
    def getParameters(self):
        return self.dataMap.get(Args.PARAM_KEY)

    def getParameter(self,index, default=None):
        params = self.dataMap.get(Args.PARAM_KEY)
        if params == None:
            return default
        else:
            try:
                return params[index]
            except Exception, e:
                return default


    def addParameter(self, param):
        params = self.dataMap.get(Args.PARAM_KEY)
        if params == None:
            params=[param]
            self.dataMap[Args.PARAM_KEY] = params
        else:
            params.append(param)
    
    def addOption(self, option, value):
        self.dataMap[option] = value


    def parse(self,args):
        self.baseLine = args[0]
        argsLength = len(args)
        argsRange = range(1, argsLength)
        for i in argsRange:
            a = args[i]
            if a.startswith("-"):
                je = a.find("=")
                if je != -1:
                    self.addOption(a[1:je], a[je+1:1000])                    
                elif (i+1) < argsLength:
                    self.addOption(a[1:1000], args[i+1])
                    argsRange.remove(i+1)
                else:
                    raise Exception, "command error. :" + a
            elif self.command == None:
                self.command = a
            else:
                self.addParameter(args[i])


def test():
    args = Args()
    a = ["a","b","c","myalibaba","-c","2","-config","work2config"]
    args.parse(a)
    print args.getParameters()
    print args.getParameter(0)
    print args.getParameter(1)
    print args.getParameter(3)
    print args.getOption("c"),"option"
    print args.getOption("config"),"option"
    print args.getOption("dddd"),"option"

#test()

