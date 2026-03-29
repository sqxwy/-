import getpass
import logging

class MyLog(object):
    def __init__(self):
        user=getpass.getuser()
        self.logger=logging.getLogger(user)
        self.logger.setLevel(logging.DEBUG)
        logFile=r'D:\vscode专用\movie\mylog.log'
        formatter=logging.Formatter(' %(asctime) -12s %(levelname) -8s %(name) -10s %(message) -12s')

        logHand=logging.FileHandler(logFile)
        logHand.setFormatter(formatter)
        logHand.setLevel(logging.ERROR)

        logHandSt=logging.StreamHandler()
        logHandSt.setFormatter(formatter)
        self.logger.addHandler(logHand)
        self.logger.addHandler(logHandSt)                      

    def debug(self,msg):
        self.logger.debug(msg)

    def info(self,msg):
        self.logger.info(msg)

    def warning(self,msg):
        self.logger.warning(msg)

    def error(self,msg):
        self.logger.error(msg)

    def critical(self,msg):
        self.logger.critical(msg)

if __name__ == "__main__":
    mylog=MyLog()
    mylog.debug("I'm debug")
    mylog.info("I'm info")
    mylog.warning("I'm warn")
    mylog.error("I'm error")
    mylog.critical("I'm critical")