#This is the coordinator process

import socket
import sys
import random
from util import *
#Create an object of util class for helper functions
u = util()

#Receive basic info from bird
cId = sys.argv[1]
N = int(sys.argv[2])
M = int(sys.argv[3])
pig_list = sys.argv[4:]
pig_list = u.clean_list(pig_list,1)

#Create a coordinator_socket and send connection details to the bird
try:
	c_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	c_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
except sys.error,msg:
	print 'Socket connection failed ' + msg
	exit(1)
bird=socket.gethostname()
port=8888;      #Agreed upon by everyone in the system 
try:
	bird_ip=socket.gethostbyname(bird)
except socket.gaierror:
	print 'Unable to resolve the bird\'s IP'
	exit(1)
c_socket.connect((bird_ip,port))
try:
	mesg='Coordinator '+cId+ ' has joined the network'
	c_socket.sendall(mesg)
except socket.error:
	print 'Unable to send ACK message to bird'
	exit(1)

print 'Coordinator ', cId, ': ',pig_list

target_loc = c_socket.recv(8888)
print 'Coordinator ', cId, ' : target location = ', target_loc
a = c_socket.recv(8888)
conf = open('net.conf','r')
conn_info = u.get_conn_info(conf.readlines())
other_c = u.get_other_coordinator(cId)			#Simple util function to get the connection parameters of the other coordinator pig
my_ip = conn_info[cId][0]
my_port = conn_info[cId][1]

#############################
# Code for each bird launch #
#############################
#Sleep Status for the coordinators. O for not sleeping, and 1 for sleeping
oink_sleep_status = 0
doink_sleep_status = 0

#Simple Implementation of Fault Tolerance :: Check to see if the other coordinator is alive or not.
#Convention :: Coordinator with smaller Id is Oink and the one with higher Id is called Doink
#The coordinator with lower cId will ping the higher to see his decision (sleep with some probability).
if int(cId) < int(other_c):
	#ping the other coordinator and wait for reply
	doink_conn = conn_info[other_c]
	oink_socket = u.sock_connect(u.get_socket(),doink_conn)
	u.send_message(oink_socket,'0 Are you asleep?')
	print 'Coordinator Oink pinged Coordinator Doink'
	doink_sleep_status = oink_socket.recv(1024);
	if doink_sleep_status=='1':
		print 'Oink : Doink decided to sleep for this round'
		pig_list = filter(lambda x: x!=int(cId) and x!=int(other_c), range(1,N+1)) 	#Update pig_list to have Doink's pigs as well
	
	#Tell every pig in pig_list that Oink is their coordinator
	for pig in pig_list:
		pig_conn = conn_info[str(pig)]
		pig_sock = u.sock_connect(u.get_socket(),pig_conn)
		u.send_message(pig_sock,str(cId))
else:
	#wait for a ping from the other coordinator
	doink_socket = u.sock_bind(u.get_socket(),my_ip,my_port)
	doink_socket.listen(1)
	oink_conn,oink_addr = doink_socket.accept()
	oink_message = oink_conn.recv(oink_addr[1])
	print 'Coordinator Doink received from Coordinator Oink : ', oink_message
	
	#decide whether to sleep of not with some probability
	if random.random() > 0.5:
		doink_sleep_status = 1
	oink_conn.send(str(doink_sleep_status))

	#If not sleeping, tell every pig in pig_list that Doink is their coordinator
	if doink_sleep_status==0:
		for pig in pig_list:
                	pig_conn = conn_info[str(pig)]
                	pig_sock = u.sock_connect(u.get_socket(),pig_conn)
                	u.send_message(pig_sock,str(cId))
		
		

#For a graceful exit of all processes, every process will tell the bird process that they have completed
c_socket.sendall('Done')
c_socket.close()



