#!/usr/bin/python
import random
 
def getServicesToRun():
	srvToRun = ""
	with open("./Inetsim/services-basic.txt") as f:
		for line in f:
			srvToRun += "start_service " + line 
	return srvToRun

def generateFtpConf(offset, version, banner, allow_rec):
	port = offset + 21
	ret_str = "ftp_bind_port " + str(port) + "\n\n"
	ret_str += "ftp_version " + "\"" + version + "\"" + "\n\n"
	ret_str += "ftp_banner " + "\"" + banner + "\"" + "\n\n"
	val = ""
	if (allow_rec == True):
		val = "yes"
	else:
		val = "no"
	ret_str += "ftp_recursive_delete " + val + "\n\n"
	return ret_str

def generatePopConf(offset, banner):
	port = offset + 110
	ret_str = ""
	ret_str += "pop3_bind_port " + str(port) + "\n\n"
	ret_str += "pop3_banner " + "\"" + banner + "\"" + "\n\n\n"
	return ret_str;

def generateSmtpConf(offset, banner):
	port = offset + 25
	ret_str = ""
	ret_str += "smtp_bind_port " + str(port) + "\n\n"
	ret_str += "smtp_banner " +  "\"" + banner + "\"" + "\n\n\n"
	return ret_str;

def generateHttpConf(offset, banner):
	port = offset + 80
	ret_str = ""
	ret_str += "http_bind_port " + str(port) + "\n\n"
	ret_str += "http_version " + "\"" + banner + "\"" + "\n\n" 
	return ret_str

def generateHttpsConf(offset, banner, key_file, cert_file):
	port = offset + 443
	ret_str = ""
	ret_str += "https_bind_port " + str(port) + "\n\n"
	ret_str += "https_version " + "\"" + banner + "\"" + "\n\n\n" 
	#ret_str += "https_ssl_keyfile " + key_file + "\n\n\n" 
	#ret_str += "https_ssl_certfile " + cert_file + "\n\n\n" 
	
	return ret_str

def getRandomBanner(fileName):
	ret_str = ""
	num_lines = sum(1 for line in open(fileName))
	rndLine = random.randint(1, num_lines)
	f = open(fileName)
	lines = f.readlines()
	return lines[rndLine-1].rstrip('\n')

def getRandomBool():
	return bool(random.getrandbits(1))	

def interface(offset, configFileName): 
	outFile = open(configFileName, 'w')
	srvToRun = getServicesToRun()
	outFile.write(srvToRun+"\n\n")
	path = "./Inetsim/"
	ftpBannersFile   = path + "ftp-banners-linux.txt"
	smtpBannersFile  = path + "smtp-banners-linux.txt"
	pop3BannersFile  = path + "pop3-banners-linux.txt"
	httpBannersFile  = path + "http-banners-linux.txt"
	httpsBannersFile = path + "http-banners-linux.txt"
	## for now fix ftp_versiont string to FTP Server
	ftpVersionString = "FTP Server"
	ftpBannerString = getRandomBanner(ftpBannersFile)
	outFile.write(generateFtpConf(offset, ftpVersionString, ftpBannerString,  getRandomBool()))
	popBannerString = getRandomBanner(pop3BannersFile)
	outFile.write(generatePopConf(offset, popBannerString))
	smtpBannerString = getRandomBanner(smtpBannersFile)
	outFile.write(generateSmtpConf(offset, smtpBannerString))
	httpBannerString = getRandomBanner(httpBannersFile)
	outFile.write(generateHttpConf(offset, httpBannerString))
	httpsBannerString = getRandomBanner(httpsBannersFile)
	outFile.write(generateHttpsConf(offset, httpsBannerString, "default_key.pem", "default_cert.pem"))
	outFile.close()

#if __name__ == '__main__':
#	offset = 4000
#	fileName = "inetsim_linux.config"
#	interface(offset, fileName)

