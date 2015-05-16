#!/usr/bin/python
def getServicesToRun():
	srvToRun = ""
	with open("services-basic.txt") as f:
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


if __name__ == '__main__':
	offset = 3000
	srvToRun = getServicesToRun()
	print srvToRun
	print "\n\n"
	print generateFtpConf(offset, "vsFTDd 2.0.4 - secure, fast, stable", "Welcome to Windows FTP Server", False)
	print generatePopConf(offset, "POP3 Server ready")
	print generateSmtpConf(offset, "Microsoft SMTP MAIL ready at. Version 1.5")
	print generateHttpConf(offset, "Microsoft-IIS/7.0")
	print generateHttpsConf(offset, "Microsoft-IIS/7.a", "default_key.pem", "default_cert.pem")

#banner_version = generate_random_banner()
#fname="inetsim_" + banner_version
#f = open(fname, "w");
#srvToRun = getServicesToRun()

#f.write()
