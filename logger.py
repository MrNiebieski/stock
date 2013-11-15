"""

Logger lib

Author: Kavin Autar
Version: 0.1
Created: 24/10/2013
Last Modified: 24/10/2013

"""

# imports
import datetime

logDebug = True

def appendLog(logMessage):
    with open("stock.log", "a") as logfile:
        logfile.write("%s %s\n" % (str(datetime.datetime.now()), logMessage.replace("\n", " ")))

def debug(*args):
    global logDebug
    if logDebug:
        logMessage = "DEBUG: %s" % " ".join(args)
        appendLog(logMessage)

def info(*args):
    logMessage = "INFO: %s" % " ".join(args)
    appendLog(logMessage)

def error(*args):
    logMessage = "ERROR: %s" % " ".join(args)
    appendLog(logMessage)

def main():
    logMsg("this is my first log message!")

if __name__ == "__main__":
    main()
