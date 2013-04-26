#This is a class file which will have functions used across files
class util:
	#Function to clean up a list passed over socket
	def clean_list(self,l,c_flag):
		l_clean=[]
		for i in range(0,len(l),2):
			cur_1=l[i].replace('[','').replace(']','').replace(',','')
			cur_2=l[i+1].replace('[','').replace(']','').replace(',','')       #Remove all unwanted characters
			l_clean.append([int(cur_1),int(cur_2)])
		if c_flag:
			return l_clean[0]
		else:
			return l_clean

