#This is the pig process
import socket
import sys
import random
from util import *

#Create an object of util function for common tasks
u = util()

#Receive basic info from bird
pigId=sys.argv[1]
N=int(sys.argv[2])
M=int(sys.argv[3])
stones=(sys.argv[4:])
stones=u.clean_list(stones,0)

#Create a pig_socket and send connection details to the bird
try:
	pig_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	pig_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
except sys.error,msg:
	print 'Socket connection failed ' + msg
	exit(1)
bird = socket.gethostname()
port = 8888;      #Agreed upon by both the 
try:
	bird_ip = socket.gethostbyname(bird)
except socket.gaierror:
	print 'Unable to resolve the bird\'s IP'
	exit(1)
pig_socket.connect((bird_ip,port))
try:
	mesg = 'Pig '+pigId+ ' has joined the network'
	pig_socket.sendall(mesg)
except socket.error:
	print 'Unable to send ACK message to bird'
	exit(1)
	
#Once the pigs have joined the network, we will receive the assigned grid location for this process
loc = pig_socket.recv(8888)
loc = loc.split(',')
x = int(loc[0][1:])
y = int(loc[1][:-1])

print 'Pig',pigId,' :','[',str(x),',',str(y),']'

#Every pig wait for a message from the bird saying net.conf is written
a = pig_socket.recv(8888)
conf = open('net.conf','r')
conn_info = u.get_conn_info(conf.readlines())		#Every pig knows about the configurations of others now
my_ip = conn_info[pigId][0]
my_port = conn_info[pigId][1]

for i in range(M):
	#Every pig will wait to hear from their coordinator
	c_sock = u.sock_bind(u.get_socket(),my_ip,my_port)
	c_sock.listen(1)
	c_conn, c_addr = c_sock.accept()
	my_coord  = c_conn.recv(64)
	print 'Pig ',pigId,' Iteration ',i+1,': My coordinator is ',my_coord
	c_sock.close()

#Every process will send a 'Done' message to the bird process for a graceful exit
pig_socket.sendall('Done')
pig_socket.close()
