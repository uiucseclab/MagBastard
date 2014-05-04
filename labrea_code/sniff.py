from scapy.all import *

pkt = sniff(filter="port 23", iface="lo", count=1, prn=lambda x: x.sprintf("{IP:%IP.src% -> %IP.dst%\n}{Raw:%Raw.load%\n}")) 

new_pkt = IP(dst = pkt[0][IP].src, src = pkt[0][IP].dst)/TCP(dport=pkt[0][TCP].sport, sport = pkt[0][TCP].dport, flags="SA", window=3, ack=1) 

send(new_pkt)

