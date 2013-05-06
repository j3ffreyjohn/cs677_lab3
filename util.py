#This is a class file which will have functions used across files
from collections import Counter
import sys
import socket
from time import sleep
from random import choice
from random import random
from database import *
class util:
	#Function to clean up a list passed over socket
	#l is the list to be "cleaned" and c_flag indicates whether request is from coordinator or pig
	def clean_list(self,l,c_flag):
		l_clean=[]
		if c_flag:
			l = str(l)
			cur_l = l.replace(',','').replace('[','').replace(']','').replace('\'','').split()
			for item in cur_l:
				l_clean.append(int(item))
		else:
			for i in range(0,len(l),2):
				cur_1=l[i].replace('[','').replace(']','').replace(',','')
				cur_2=l[i+1].replace('[','').replace(']','').replace(',','')       #Remove all unwanted characters
				l_clean.append([int(cur_1),int(cur_2)])
		return l_clean
	
	#Function to read the net.conf file and return a dictionary of connection parameters
	#Input is conf :: List of lines of the net.conf file
	def get_conn_info(self, conf):
		conn={}			#Details stored in a dictionary with the pigId as the key
		for item in conf:
			cur = item.split()
			cur_l = []
			cur_l.append(cur[1])
			cur_l.append(cur[2])
			conn[cur[0]]=cur_l
		return conn

	#Function to process the net.conf data and give the connection params of the other coordinator
	#Input is conf :: List of lines of the net.conf file and cId : the pigId of the coordinator calling this function
	def get_other_coordinator(self, cId):
		conf = open('net.conf','r')
		conf = conf.readlines()
		cId1 = conf[-1:][0].split()
		cId2 = conf[-2:-1][0].split()
		if cId==cId1[0]:
			return cId2[0]
		else:
			return cId1[0]
	
	#Function to get a new socket
	def get_socket(self):
		try:
        		new_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        		new_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		except sys.error,msg:
        		print 'Socket connection failed ' + msg
        		exit(1)
		return new_socket

	#Function to send a message on a socket
	#Input is the socket bound to the ip and address of receiver and the message to be sent
	def send_message(self,sock,message):
		try:
        		sock.sendall(message)
		except socket.error:
        		print 'Unable to send ACK message to bird'
        		exit(1)
	
	#Function to bind a socket to a given IP and Port
	#Return the bound socket	
	def sock_bind(self,sock,ip,port):
		try:
 			socket.socket()
			sock.bind((ip,int(port)))
 		except socket.error, msg:
 			print 'Bind with port failed'
 			exit(1)
		return sock

	#Function to connect to another connection till the connection is established
	#Input is the socket with which you want to connect and conn, the connection parameter list of the target
	def sock_connect(self,sock,conn):
		while True:
			try:
				sock = self.get_socket()			#Fixed bug :: once failed socket gets initialized wrongly
				sock.connect((conn[0],int(conn[1])))
				break
			except socket.error,msg:
				sleep(1)
				continue
		return sock

        #Function return a target at random
	#Input N: Number of pigs in the game, Output target: PigID of a pig which has not been hit selected at random
	def get_target(self,N,pigs):
                d=database(N)
                status=[]                
                for i in range(len(pigs)):
                        status.append(d.get_status(pigs[i]));

                not_hit=[]

                for i in range(len(status)):
                        if status[i]==0:
                                not_hit.append(pigs[i]);

                target=choice(not_hit);
                return target
                                
                        
	def init_locations(self,N,pigs,pos):
		d = database(N)
		for i in range(len(pos)):
			d.update_location(int(pigs[i]),pos[i][0],pos[i][1])

        #Function to define the behavior of each pig for each game
        #Input: Pig location, Target location, Stone locations. Output: Hit status, New location
        def play_game(my_loc, target_loc, stones):
                new_loc=[]
                hit_status=0;
                if(my_loc==target_loc):                 #Check if current location is the target
                        if(random()>0.75):              #if target is the location of the pig, it is random with some random probability
                                hit_status=1;
                                new_loc[0]=my_loc[0];
                                new_loc[1]=my_loc[1];
                        else:                                
                                if([my_loc[0]+1,my_loc[1]] not in stones):
                                        new_loc=[my_loc[0]+1,my_loc[1]];
                                elif([my_loc[0]-1,my_loc[1]] not in stones):
                                        new_loc=[my_loc[0]-1,my_loc[1]];
                                elif([my_loc[0],my_loc[1]+1] not in stones):
                                        new_loc=[my_loc[0],my_loc[1]+1];
                                elif([my_loc[0],my_loc[1]-1] not in stones):
                                        new_loc=[my_loc[0],my_loc[1]-1];
                                else:
                                        hit_status=1;
                                        new_loc[0]=my_loc[0];
                                        new_loc[1]=my_loc[1];
                return [hit_status, new_loc]

                        
                                
                        
                        
                

			                        

