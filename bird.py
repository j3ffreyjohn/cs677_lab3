#This is the bird process which spawns all other processes

import os
import sys
from random import randint, shuffle, sample, choice
import socket
from util import *
from database import *
from time import sleep

N = int(sys.argv[1])		# N is the number of pigs in the system
M = int(sys.argv[2])		# M is the number of bird launches in one game

print 'Angry Birds Game Started ... '

#Create objects of the util and database class
u = util()
d = database(N)

#Choose two pigs to be the coordinators at random
coordinators = sample(range(1,N+1),2)	
pigs = list(set(range(1,N+1)) - set(coordinators))

#Assign the rest of the pigs to one of these coordinators
shuffle(pigs)
pigs_split = [pigs[i::2] for i in range(2)]	#Assign the pigs randomly to one of the coordinators

#Generate random [x,y] coordinates for all the pigs in the NX3 grid
pos=[];
while(len(pos) < N-2):
	p=[randint(1,N),randint(1,3)];
	if p not in pos:
		pos.append(p);

#Generate grid locations for the stone columns
stones=[];
while(len(stones)<3):
	p=[randint(1,N),randint(1,3)];
	if p not in pos and p not in stones:
		stones.append(p);

#Open a socket called bird_socket for the pigs to tell the bird their network info
HOST = socket.gethostname()
PORT = 8888
bird_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
bird_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
try:
	socket.socket()
	bird_socket.bind((HOST,PORT))
except socket.error, msg:
	print 'Bind with port failed'
	exit(1)
bird_socket.listen(N)		#This socket can receive upto N requests at a time

#Spawn the pigs and the coordinators
conf = open('net.conf','w')		#All network info will be written to the net.conf file
conn_pigs = {}				#Store the connection objects to all peers
for i in range(N-2):
	spawn_pig = 'python pig.py '+ str(pigs[i]) + ' ' + str(N) + ' ' + str(M) + ' ' + str(stones) + ' &'
	os.system(spawn_pig)
	conn,addr = bird_socket.accept()
	conf_info=str(pigs[i])+' '+str(addr[0])+' '+str(addr[1])+'\n'
	conf.write(conf_info)
	msg = conn.recv(addr[1])
	loc=str('['+str(pos[i][0])+','+str(pos[i][1])+']')
	conn.send(loc)
	conn_pigs[pigs[i]]=conn

target_ind = pigs.index(choice(pigs))           #Choose a target at random
target_loc = str('['+str(pos[target_ind][0])+','+str(pos[target_ind][1])+']')

for j in range(2):
	spawn_coordinator = 'python coordinator.py ' + str(coordinators[j]) + ' ' + str(N) + ' ' + str(M) + ' ' + str(pigs_split[j]) + ' &'
	os.system(spawn_coordinator)
	conn,addr = bird_socket.accept()
	conf_info=str(coordinators[j])+' '+str(addr[0])+' '+str(addr[1])+'\n'
	conf.write(conf_info)
	msg = conn.recv(addr[1])
	conn.send(target_loc)
	conn_pigs[coordinators[j]]=conn

conf.close()
print 'All network info written to net.conf'

conf = open('net.conf','r')
conn_info = u.get_conn_info(conf.readlines())

#Let every pig know that the net.conf has been written
for k in range(1,N+1):
	conn_pigs[k].send('1')				

u.init_locations(N,pigs,pos)

#Do M bird launches
for i in range(M):
	print '***** Bird Launch ',i+1,'*****'
	target_loc = '1 2'					#dummy target location
	target_new_loc = d.get_loc(u.get_target(N,pigs))
	print 'TARGET == ', target_new_loc
	#send this target loc to each coordinator
	for j in range(2):
		conn_pigs[coordinators[j]].sendall(target_loc)
	for j in range(2):
		msg = conn_pigs[coordinators[j]].recv(1024)
	sleep(5)
	#select target randomly
#	target_ind = pigs.index(choice(pigs))
#	target_loc = str('['+str(pos[target_ind][0])+','+str(pos[target_ind][1])+']')
	
	#do bird launches
	#wait for status back from coordinator(s)
	

#Termination condition :: Receive Done message from all pigs and coordinators
for k in range(1,N+1):
	msg = conn_pigs[k].recv(1024)

print 'Angry Birds Game Terminated'

