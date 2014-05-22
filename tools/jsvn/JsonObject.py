#!/usr/bin/python

import simplejson
import Util

class JsonObject:

    def __init__(self, jsonStr):
        self._jsonObject = self.parse(jsonStr)

    def parse(self, jsonStr):
        sf = StringIO.StringIO(jsonStr)
        self._jsonObject = simplejson.load(sf)
#        print self._jsonObject


    def getObject(self):
        return self._jsonObject

import string
import StringIO

import json
import re

JSON_BUG = re.compile(r'([{,\]]*)(.*?)([}:])')

def bugJson(jsonStr):
    sn = ""
    start=0
    for m in JSON_BUG.finditer(jsonStr):
        sn += jsonStr[start:m.start()]
        sn += m.group(1)

        key = m.group(2).strip()
        print m.group(1),key
        if not key.startswith("\""):
            sn += "\""

        sn += m.group(2).strip()
        sn += "\""
        sn += m.group(3)
        start=m.end()
    sn += jsonStr[start:len(jsonStr)]
    return sn
    
def test():
#    s1="{a:33, b:\"bvdd\"}"
#    print s1
#    print bugJson(s1)
    #sn = reo.sub("\"'$1'\"",s1)
    #print sn
    #re.compile(r'(.*?)(["\\\x00-\x1f])', FLAGS)    
#    print s1
#    s1="{\"a\":33,\"b\":\"bv\"}"
#    jo = json.loads(s1)
#    print jo,jo["a"],jo['b']
#    print simplejson.JSONEncoder().encode(ss)
#    print simplejson.JSONDecodeError().decode(ss)
#    print json.JSONDecoder.encoder(ss)
#    a= json.dumps(ss)
#    sf = StringIO.StringIO(ss)
#    a = simplejson.load(sf)
#    print a["a"]
#    jo = JsonObject(ss)
#    o = jo.getObject()
#    print o["a"]
    ss = Util.httpGet("aone.alibaba-inc.com","/perth/externalapi/externalapi.jsp?action=projectByFgId&projectId=101855")
    ss = ss.strip()
    print ss
    print "..."
    sn= bugJson(ss)
    print sn
    jo = json.loads(sn)
    print jo[0]["startDate"]
   

test()

