#This is the coordinator process

import socket
import sys
import random
from util import *

#Create an object of util class for helper functions
u = util()

#Receive basic info from bird
cId = sys.argv[1]
N = sys.argv[2]
M = sys.argv[3]
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

#Simple Implementation of Fault Tolerance :: Check to see if the other coordinator is alive or not.
#The coordinator with lower cId will ping the higher to see his decision (sleep with some probability).
#If that coordinator is asleep, then this coordinator cannot sleep (since we have only two coordinators in this case).
#if that coordinator is alive, decide to sleep with some probability and let the other coordinator know about it.
if int(cId) < int(other_c):
	#ping the other coordinator and wait for reply
	if other_c_sleep:
		#other coordinator has decided to sleep, update pig_list for this iteration
	else:
		#decide with some probability whether to sleep or not
		#let the other coordinator know about decision
else:
	#wait for a ping from the other coordinator
	#decide whether to sleep or not with probability
	#reply back to other coordinator and wait for response
	if other_c_sleep:
		#update pig_list for this iteration
	



c_socket.close()



