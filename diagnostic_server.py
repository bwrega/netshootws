#!/usr/bin/env python2
import web
import os
import requests
import getopt
import sys

urls = (
    "/", "ShowOthers",
    "/test", "Test"
)

def printUsage():
    sys.stderr.write("Usage: "+sys.argv[0]+' --my-name=node1 --others-names="node2:8080;node3" [--listen-on=0.0.0.0:8081]\n')

def parseArgs():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "", ["my-name=", "others-names=", "listen-on="])
    except getopt.GetoptError as err:
        sys.stderr.write(str(err))
        sys.stderr.write("\n")
        printUsage()
        sys.exit(1)
    for opt, arg in opts:
        if opt == "--my-name":
            sys.MY_NAME=arg
        elif opt == "--others-names":
            sys.OTHERS_NAMES = arg.split(";")
        elif opt == "--listen-on":
            sys.LISTEN_ON = arg

    if sys.MY_NAME == "" or len(sys.OTHERS_NAMES) == 0:
        printUsage()
        sys.exit(1)

class Test:
    def GET(self):
        return "OK"

def testOther(host):
    url = "http://"+host+"/test"
    statusCode = -1
    try:
        res = requests.get(url, timeout=1.0)
        statusCode = res.status_code
        res.raise_for_status()
        return {"isSuccess": res.status_code == 200, 'statusCode': statusCode, "errorMessage": ""}
    except (KeyboardInterrupt, SystemExit):
        raise
    except Exception as err:
        return {"isSuccess": False, 'statusCode': statusCode, "errorMessage": str(err)}

def formatErrorDetails(res):
    return "response code: "+str(res["statusCode"])+'<br>\n'+"error message: "+res["errorMessage"]+"<br><br>\n"

def othersInfo():
    myName = sys.MY_NAME
    othersNames = sys.OTHERS_NAMES
    resHtml = "<html><body>\n"
    for host in othersNames:
        testResult = testOther(host)
        resHtml = resHtml + myName + " =&gt; " + host
        if testResult["isSuccess"]:
            resHtml = resHtml + '<span style="color: #00FF00;padding-left: 16px;">OK</span><br>\n'
        else:
            resHtml = resHtml + '<span style="color: red;padding-left: 16px">ERROR</span><br>\n'
            resHtml = resHtml + formatErrorDetails(testResult)
    return resHtml + "</body></html>\n"


class ShowOthers:
    def GET(self):
        return othersInfo()
        

if __name__ == "__main__": 
    sys.MY_NAME=""
    sys.OTHERS_NAMES=[]
    sys.LISTEN_ON="0.0.0.0:8080"
    parseArgs()
    sys.argv=[sys.argv[0], sys.LISTEN_ON]
    app = web.application(urls, globals())
    app.run()
