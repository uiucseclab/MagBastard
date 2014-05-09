from threading import Thread

from resources import ServiceListener
from HTTP import HTTPService
from SSH import SSHService
from NetBIOS import NetBIOSService
from SMTP import SMTPService
from FTP import FTPService

def SSHThreadFunc():
    ServiceListener.startListener(SSHService.sshHandler, 10022, "SSH/servers.config")
    
def HTTPThreadFunc():
    ServiceListener.startListener(HTTPService.httpHandler, 10080, "HTTP/servers.config")

def FTPThreadFunc():
    ServiceListener.startListener(FTPService.ftpHandler, 10021, "FTP/servers.config")

def SMTPThreadFunc():
    ServiceListener.startListener(SMTPService.smtpHandler, 10025, "SMTP/servers.config")

def NetBIOSThreadFunc():
    ServiceListener.startListener(NetBIOSService.netbiosHandler, 10139, "NetBIOS/servers.config")


SSHthread = Thread(target = SSHThreadFunc)
SSHthread.start()

HTTPthread = Thread(target = HTTPThreadFunc)
HTTPthread.start()

FTPthread = Thread(target = FTPThreadFunc) 
FTPthread.start()

SMTPthread = Thread(target = SMTPThreadFunc)
SMTPthread.start()

NetBIOSthread = Thread(target = NetBIOSThreadFunc)
NetBIOSthread.start()


SSHthread.join()
HTTPthread.join()
FTPthread.join()
SMTPthread.join()
NetBIOSthread.join()
