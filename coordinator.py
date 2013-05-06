#This is the coordinator process

import socket
import sys
from random import random
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
#print 'Coordinator ', cId, ' : target location = ', target_loc
a = c_socket.recv(1)
conf = open('net.conf','r')
conn_info = u.get_conn_info(conf.readlines())
other_c = u.get_other_coordinator(cId)			#Simple util function to get the connection parameters of the other coordinator pig
my_ip = conn_info[cId][0]
my_port = conn_info[cId][1]
pig_list_backup = pig_list


for i in range(M):
	#############################
	# Code for each bird launch #
	#############################
	
	#Sleep Status for the coordinators. O for not sleeping, and 1 for sleeping
	oink_sleep_status = 0
	doink_sleep_status = 0
	pig_list = pig_list_backup
	cache = {}
	#Simple Implementation of Fault Tolerance :: Check to see if the other coordinator is alive or not.
	#Convention :: Coordinator with smaller Id is Oink and the one with higher Id is called Doink
	#The coordinator with lower cId will ping the higher to see his decision (sleep with some probability).
	if int(cId) < int(other_c):
		#Receive the target for this iteration from the bird
		#print 'Oink waiting to receive . . .'
        	target_loc = c_socket.recv(64)
        	print 'Oink : ',' Iteration no : ',i+1,' target : ', target_loc
		#ping the other coordinator and wait for reply
		doink_conn = conn_info[other_c]
		if i==0:
			oink_socket = u.sock_connect(u.get_socket(),doink_conn)
		u.send_message(oink_socket,'0 Are you asleep?')
		doink_sleep_status = oink_socket.recv(64);
		if doink_sleep_status=='1':
			print 'Oink : Doink decided to sleep for this round'
			pig_list = filter(lambda x: x!=int(cId) and x!=int(other_c), range(1,N+1)) 	#Update pig_list to have Doink's pigs as well
		else:
			if random() > 0.7:
				oink_sleep_status = 1
		u.send_message(oink_socket,str(oink_sleep_status))
			
			
		#If not sleeping, tell every pig in pig_list that Oink is their coordinator and send the target location for this iteration
		if oink_sleep_status==0:
			for pig in pig_list:
				pig_conn = conn_info[str(pig)]
				pig_sock = u.sock_connect(u.get_socket(),pig_conn)
				u.send_message(pig_sock,str(cId)+' '+target_loc)
				pig_result = pig_sock.recv(64)
				pig_result = pig_result.split()
				pig_status = int(pig_result[0])
				pig_location = [int(pig_result[1]),int(pig_result[2])]
				cache[pig]=[pig_status,pig_location]
				print 'Oink : Pig ',pig,' : Status : ',pig_status,' Location : ', pig_location
	else:
		#Receive the target for this iteration from the bird
		#iprint 'Doink waiting to receive . . .'
        	target_loc = c_socket.recv(64)
        	print 'Doink :',' Iteration no : ',i+1,' target : ', target_loc
		#wait for a ping from the other coordinator
		if i==0:
			doink_socket = u.sock_bind(u.get_socket(),my_ip,my_port)
			doink_socket.listen(1)
			oink_conn,oink_addr = doink_socket.accept()
		oink_message = oink_conn.recv(64)
	
		#decide whether to sleep of not with some probability
		if random() > 0.5:
			doink_sleep_status = 1
		oink_conn.send(str(doink_sleep_status))
		oink_sleep_status = oink_conn.recv(64)
		if oink_sleep_status=='1':
			print 'Doink : Oink decided to sleep for this round'
			pig_list = filter(lambda x: x!=int(cId) and x!=int(other_c), range(1,N+1))      #Update pig_list to have Oink's pigs as well

		#If not sleeping, tell every pig in pig_list that Doink is their coordinator and send the target location for this iteration
		if doink_sleep_status==0:
			for pig in pig_list:
                		pig_conn = conn_info[str(pig)]
                		pig_sock = u.sock_connect(u.get_socket(),pig_conn)
                		u.send_message(pig_sock,str(cId)+' '+target_loc)
				pig_result = pig_sock.recv(64)
                                pig_result = pig_result.split()
                                pig_status = int(pig_result[0])
                                pig_location = [int(pig_result[1]),int(pig_result[2])]
				cache[pig] = [pig_status,pig_location]
                                print 'Doink : Pig ',pig,' : Status : ',pig_status,' Location : ', pig_location
	u.update_town_register(cache,i+1,N)	
	#Tell the bird process that this iteration is done
	c_socket.sendall('Iteration Done!')		

#For a graceful exit of all processes, every process will tell the bird process that they have completed
c_socket.sendall('Done')
c_socket.close()



