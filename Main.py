from resources import ServiceListener
#from HTTP import HTTPService
#from SSH import SSHService
from NetBIOS import NetBIOSService
#from SMTP import SMTPService
#from FTP import FTPService

#ServiceListener.startListener(HTTPService.httpHandler, 80, "HTTP/servers.config")
#ServiceListener.startListener(FTPService.ftpHandler, 21, "FTP/servers.config")
#ServiceListener.startListener(SMTPService.smtpHandler, 25, "SMTP/servers.config")
ServiceListener.startListener(NetBIOSService.netbiosHandler, 139, "NetBIOS/servers.config")
