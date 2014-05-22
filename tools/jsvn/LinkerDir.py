#!/usr/bin/python

import os

LOG_LEVEL = "info"

def log(msg):
    if LOG_LEVEL == "debug":
        print "log:", msg

class LinkerDir:
    
    def __init__(self, src, dest):
		self._src = src
		self._dest = dest

    def linkDir(self, path=""):
        src = os.path.join(self._src,path)
        dest = os.path.join(self._dest,path)

        self._linkDir(src, dest, path)

    def _linkDir(self, src, dest, path):
        if not os.path.isdir(src):
            log("src dir is not found : "+src)
            return

        if os.path.islink(dest):
            os.remove(dest)

        if not os.path.isdir(dest):
            log("mkdirs dest: "+dest)
            os.makedirs(dest)

        fileList = os.listdir(src)
        for f in fileList:
            sf = os.path.join(src,f)
            df = os.path.join(dest,f)
            if not os.path.exists(df):
                lnCmd = "ln -s "+ sf +" " + df
                log(lnCmd)
                os.system(lnCmd)

    def copyDir(self, path=""):
        src = os.path.join(self._src, path)
        if not os.path.isdir(src):
            log("copyDir src dir is not found : "+src)
            return

        src = os.path.join(src, "*")
        dest = os.path.join(self._dest,path)

        if os.path.islink(dest):
            log("mkdir dir is link, remove it : "+src)
            os.remove(dest)

        if os.path.isfile(dest):
            log("mkdir dir is file, remove it : "+src)
            os.remove(dest)

        if os.path.isdir(dest):
            log("copyDir dest is exist: "+dest)
            return
        else:
            log("mkdirs dest: "+dest)
            os.makedirs(dest)

            cpCmd = "cp -r " + src + " " + dest
            log(cpCmd)
            os.system(cpCmd)


    def makeDir(self, dirPath):
        if not os.path.isdir(self._dest):
            self.linkDir()

        if dirPath == None:
            return

        path = ""
        fs = dirPath.split("/")
        index = 0
        for name in fs:
            index = index+1
            if len(name) == 0:
                continue
            path = os.path.join(path, name)
            log("make dir, check path: "+path)
            dest = os.path.join(self._dest, path)
            if os.path.islink(dest):
                os.remove(dest)

            if index<len(fs):
                self.linkDir(path)
            else:
                self.copyDir(path)





def test():
    ld = LinkerDir("/home/wxy/test_link_dir/src/mock-test","/home/wxy/test_link_dir/dest")
    ld.linkDir()
    ld.makeDir("admin/services/com.alibaba.http.ISearch/v1/lib")
    ld.makeDir("saaspt/services")
#test()

