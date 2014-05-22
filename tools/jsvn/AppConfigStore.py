from Configuration import Configuration
from AppConfig import AppConfig
import Log

class AppConfigStore:

    conf = None
    
    @staticmethod
    def build(fileName="apps.cfg"):
        if AppConfigStore.conf == None:
            AppConfigStore.conf = Configuration()
            AppConfigStore.conf.load(fileName)

    @staticmethod
    def getAppConfig(appId):
        if AppConfigStore.hasAppConfig(appId):
            subConf = AppConfigStore.conf.getSub(appId)
            appConfig = AppConfig(appId)
            appConfig.init(subConf)
            return appConfig
        else:
            Log.error("not found "+appId+"'s config in apps.cfg")
            raise Exception, "not found ["+appId+"]'s config in apps.cfg"

    @staticmethod
    def hasAppConfig(appId):
        return AppConfigStore.conf.hasKey(appId+".svn")

def test():
    ma = AppConfigStore.getAppConfig("myalibaba")
    print ma.isBiz() ," false"
    print ma.isWeb() ," true"
    print ma.isWebBiz() ," false"
    

#test()

