from Configuration import Configuration
from CommandFactory import CommandFactory
from AppConfig import AppConfig
from App import App
from EnvContext import EnvContext
import threading

class Runable:
    def run():
        pass

class Runner(threading.Thread):

    def __init__(self, runable):
        threading.Thread.__init__(self) 
        self.runable = runable

    def run(self):
        self.runable.run()



def test():
    conf = Configuration()
    conf.load("config")
    env = EnvContext.build(conf,"myalibaba")
    command = CommandFactory.getCommand("cp")
    r = Runner(command, env)
    r.start()

#test()



