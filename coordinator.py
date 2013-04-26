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
pig_list = sys.argv[3:]
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

a = c_socket.recv(8888)
conf = open('net.conf','r')
conn_info = u.get_conn_info(conf.readlines())	#Coordinators know the connection parameters to everyone now
c_socket.close()



