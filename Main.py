from resources import ServiceListener
from HTTP import HTTPService
#from SSH import SSHService
#from NetBIOS import NetBIOSService
#from SMTP import SMTPService
#from FTP import FTPService

ServiceListener.startListener(HTTPService.httpHandler, 80, "HTTP/servers.config")
