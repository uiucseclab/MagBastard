from threading import Thread
from ConfigParser import ConfigParser

from resources import ServiceListener
from HTTP import HTTPService
from SSH import SSHService
from NetBIOS import NetBIOSService
from SMTP import SMTPService
from FTP import FTPService

config = ConfigParser()
config.read("magbastard.cfg")

def SSHThreadFunc():
    ServiceListener.startListener(SSHService.sshHandler, int(config.get("default", "SSHPort")), "SSH/servers.config")
    
def HTTPThreadFunc():
    ServiceListener.startListener(HTTPService.httpHandler, int(config.get("default", "HTTPPort")), "HTTP/servers.config")

def FTPThreadFunc():
    ServiceListener.startListener(FTPService.ftpHandler, int(config.get("default", "FTPPort")), "FTP/servers.config")

def SMTPThreadFunc():
    ServiceListener.startListener(SMTPService.smtpHandler, int(config.get("default", "SMTPPort")), "SMTP/servers.config")

def NetBIOSThreadFunc():
    ServiceListener.startListener(NetBIOSService.netbiosHandler, int(config.get("default", "NetBIOSPort")), "NetBIOS/servers.config")


SSHthread = Thread(target = SSHThreadFunc)
SSHthread.daemon = True
SSHthread.start()

HTTPthread = Thread(target = HTTPThreadFunc)
HTTPthread.daemon = True
HTTPthread.start()

FTPthread = Thread(target = FTPThreadFunc) 
FTPthread.daemon = True
FTPthread.start()

SMTPthread = Thread(target = SMTPThreadFunc)
SMTPthread.daemon = True
SMTPthread.start()

NetBIOSthread = Thread(target = NetBIOSThreadFunc)
NetBIOSthread.daemon = True
NetBIOSthread.start()


SSHthread.join()
HTTPthread.join()
FTPthread.join()
SMTPthread.join()
NetBIOSthread.join()

