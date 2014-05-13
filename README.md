CS 460 - Spring 2014
Magnanimous Bastard



	Upon each connection, either a deny is made or an accept.  Sessions are enabled, so connections from an IP is kept the same for five minute intervals. 


	Port 21 FTP 
		- FTP is configured to either send a response packet (one of five randomly selected) 

	Port 22 SSH 
		- Kippo is installed on here to offer a fake ssh terminal for those connecting.  Kippo provides its own logs of connections and commands to the database.  THe following are our two kippo logins

			user: root
			password: 123456

			user: bambi
			password:

	Port 25 SMTP
		- Chooses one of two responses to send back.  Sessions apply.  

	Port 80 HTTP
		- Chooses response packet.  Website also exists on port 80 for any visitors.

	Port 139 NetBIOS
		- Chooses one of four reponses.

	Labrea
		- 
		
Things to be fixed
	
	Modify Kippo to be more of a mock shell.  
	Add functionality  to allow for drops rather than denys
	

