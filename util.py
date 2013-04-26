#This is a class file which will have functions used across files
from collections import Counter

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

