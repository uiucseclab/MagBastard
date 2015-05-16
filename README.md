
CS 460 - Spring 2015
Magnanimous Bastard
IP: 52.10.246.52

Features

1) Service Emulation through inetsim and dionaea
   For the honeypot to emulate a real system, we repond to requests using inetsim and dionaea. 
   Applicable services are: HTTP, HTTPS, FTP, SMTP, POP3. 
   SSH service remains to be ported to Kippo. Scripts were written for the east of usage

   Usage: ./insetsim-daemon start|stop [path_to_pid] [path_to_conf_file]
   Usage: ./opt/dionaea/bin/dionaea
          (configuration file for dionaea can be found in /opt/dionaea/etc/dionaea/dionaea.conf

2) Collect Banner data.
   Using the list of sites from Alexa-1000sites, we collect HTTP and HTTPS banners from real sites
   From the site listed in www.ftp-sites.org, we collect FTP banners from real sites
   From the lists in liveport.com/smtp-servers, we collect SMTP/POP3 banners

   Usage: python get-http-banners.py > all-http.txt
         (http can be replaced with other services. Refer to the list of scripts in the root folder)

          python banner-grabbing.py nameofsite port_num # grabs the banner of the specific site : port

3) Random cofig file generation
   Using the banners collected from 2), we generate the configuration files for inetsim. Each configuration file represents a distinct server
   Usage: Inetsim/gen_conf_linux.py platform_id, platform_id.conf (where platform_id is an integer)

4) Magbastard Update
   After the update, Magbastard runs up to 10 inetsim processes where each process represents a distinct server.
   Upon receiving a request, MagBastard checks if there is a valid session from the src of the request. 
       If so, it forwards the request accordingly.
       Else, it checks how many inetsim processes are running
           If less than max, initiate a new process with a new config file generated from 3)
           Else, assigns a random server from list of existin, and forwards the request accordingly.
   Upon timeout, MagBastard checks if the inetsim mapped to this session has other valid sessions.
       If not, it terminates the inetsim process.

TODO:
   MagBastard need update to forward a portion of requests to Dionaea, which is otherwise fully functional.
   Other services remain for extended service.
   If you can find an alternative to labrea mentioned in the readme from 2014, you can map different IPs with a different inetsim process.  


CS 460 - Spring 2014
Magnanimous Bastard

Address: spring2014azure.cloudapp.net


Features
	
	Upon each attempted connection from another machine, either an accept or drop is selected.  This is done randomly by our handler code which then records this choice in our database.  For the next five minutes, any subsequent connections from this IP will result in this same response.  Due to the nature of our code and how dropping a response works, our dropping is not perfect at the moment; we cannot decide whether to drop a connection until we see it come in, at which point it is too late.  As a result we send an RST as soon as we decide we want to drop the connection.   
	
	Our database is configured on the machine to log all incoming connections (time, source, destination) along with the responses made to each of these connections.  Please see /logging/sqlstatements.txt for our schemas.  Kippo also has its own logging functionality which is similarly recorded in the database.


	Port 21 FTP 
		- FTP is configured to either send a response packet (one of five randomly selected) 

	Port 22 SSH 
		- Kippo is installed on here to offer a fake ssh terminal for those connecting.  Kippo provides its own logs of connections and commands to the database.  THe following are our two kippo logins

			user: root
			password: 123456

			user: bambi
			password: notbambi

	Port 25 SMTP
		- Chooses one of two responses to send back.

	Port 80 HTTP
		- Chooses response packet.  Website also exists on port 80 for any visitors.

	Port 139 NetBIOS
		- Chooses one of four responses.
		- It should be noted that Port 139 does not allow connections from the outside, but connecting to the public IP internally will allow a connection.  Also nmap-ing will show that Samba is running.
		- 
	We could not get Labrea working because it will not listen on the local machine.  Labrea works perfectly for listening on the network for IPs that aren't being used since it can just sniff traffic and respond if no one else does. However, labrea does not bind to any ports on the host machine. Because of this, upon an attempted connection the OS will automatically send a SYNRST back before labrea is able to see the incoming packet and respond itself. Because of this, the outside world will just see the port as closed and will not get tarpitted. Without changing the labrea source code, it would be impossible to get this to work. In addition, labrea does not compile from source in linux 12.04 or 14.04 so we couldn't change the source. Instead, we had to use the prepackaged binary. As a result, we could not use labrea in our code.

Things to be fixed
	
	- Modify Kippo to be more of a mock shell.  
	- Add functionality to allow for drops rather than denys
	- Fix Samba port 139 issue

How to run
	
	Run python main.py in MagBastard to get start up the handler.
	Run start.sh in MagBastard/kippo-0.8 to start kippo
	

