from threading import Thread
from ConfigParser import ConfigParser

from resources import ServiceListener
from HTTP import HTTPService
from HTTPS import HTTPSService
from SSH import SSHService
from NetBIOS import NetBIOSService
from SMTP import SMTPService
from FTP import FTPService
from POP3 import POP3Service

config = ConfigParser()
config.read("magbastard.cfg")

def SSHThreadFunc():
    ServiceListener.startListener(SSHService.sshHandler, int(config.get("default", "SSHPort")), "SSH/servers.config")
    
def HTTPThreadFunc():
    ServiceListener.startListener(HTTPService.httpHandler, int(config.get("default", "HTTPPort")), "HTTP/servers.config")

def HTTPSThreadFunc():
    ServiceListener.startListener(HTTPSService.httpsHandler, int(config.get("default", "HTTPSPort")), "HTTPS/servers.config")

def FTPThreadFunc():
    ServiceListener.startListener(FTPService.ftpHandler, int(config.get("default", "FTPPort")), "FTP/servers.config")

def SMTPThreadFunc():
    ServiceListener.startListener(SMTPService.smtpHandler, int(config.get("default", "SMTPPort")), "SMTP/servers.config")

def NetBIOSThreadFunc():
    ServiceListener.startListener(NetBIOSService.netbiosHandler, int(config.get("default", "NetBIOSPort")), "NetBIOS/servers.config")

def POP3ThreadFunc():
    ServiceListener.startListener(POP3Service.pop3Handler, int(config.get("default", "POP3Port")), "POP3/servers.config")

SSHthread = Thread(target = SSHThreadFunc)
SSHthread.daemon = True
SSHthread.start()

HTTPthread = Thread(target = HTTPThreadFunc)
HTTPthread.daemon = True
HTTPthread.start()

HTTPSthread = Thread(target = HTTPSThreadFunc)
HTTPSthread.daemon = True
HTTPSthread.start()

FTPthread = Thread(target = FTPThreadFunc) 
FTPthread.daemon = True
FTPthread.start()

SMTPthread = Thread(target = SMTPThreadFunc)
SMTPthread.daemon = True
SMTPthread.start()

NetBIOSthread = Thread(target = NetBIOSThreadFunc)
NetBIOSthread.daemon = True
NetBIOSthread.start()

POP3thread = Thread(target = POP3ThreadFunc)
POP3thread.daemon = True
POP3thread.start()

SSHthread.join()
HTTPthread.join()
HTTPSthread.join()
FTPthread.join()
SMTPthread.join()
NetBIOSthread.join()
POP3thread.join()

