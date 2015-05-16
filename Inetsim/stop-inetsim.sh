#/bin/sh

if [ -f /var/run/inetsim.pid ] ; then
	INETPID='cat /var/run/inetsim.pid'
	sudo kill ${INETPID} > /dev/null
	wait ${INETPID}
fi
