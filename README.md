CS 460 - Spring 2014
Magnanimous Bastard

Address: spring2014azure.cloudapp.net


Features
	
	Upon each connection, either an accept or drop is selected.  This is done randomly by our handler code which then records this choice in our database.  For the next five minutes, any connection from this IP will result in this same response.  Due to the nature of our code and how dropping a response works, our dropping is not perfect at the moment; we cannot decide whether to drop a connection until we see it come in, at which point it is too late.  As a result we send an RST as soon as we decide we want to drop the connection.   
	
	Our databse is configured on the machine to log all incoming connections (time, source, destination) along with the responses made to each of these connections.  Please see /logging/sqlstatements.txt for our schemas.  Kippo also has its own logging functionality which is similarly recorded in the database.


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
		- Chooses one of four reponses.
		- It should be noted that Port 139 does not allow conenctions from the outside but connecting to the public IP from interally will alow a connection.  Also nmaping will show that Samba is running
		- 
	We could not get Labrea working because it will not listen on the local machine.  Labrea works perfectly for listening on the network for IPs that aren't being used since it can just sniff traffic and respond if no one else does. However, labrea does not bind to any ports on the host machine. Becaues of this, the OS will automatically send a SYNRST before labrea is able to see the packet and respond itself. Because of this, the outside world will just see the port as closed. Without changing the labrea source code, it would be impossible to get this to work. In addition, labrea does not compile from source in linux 12.04 or 14.04 so we had to use the prepackaged binary. As a result, we could not use labrea in our code.

Things to be fixed
	
	- Modify Kippo to be more of a mock shell.  
	- Add functionality  to allow for drops rather than denys
	- Fix Samba port 139 issue

How to run
	
	Run python main.py in MagBastard to get start up the handler.
	Run start.sh in MagBastard/kippo-0.8 to start kippo
	

