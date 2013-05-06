#This is the database server
#Takes as argument the number of pigs in the game (N)
import sqlite3;
class database:
    #This constructor is used (ideally) for updates.
	def __init__(self, N):                              #N: Number of pigs
        	conn=sqlite3.connect('database.db')             #Establish connection with the database
        	c=conn.cursor()
        	for i in range(1,N+1):                          #Construct query string
            		if i==1:
                		strr='(Iteration real PRIMARY KEY, Pig1 real,'
            		elif i!=N:
                		strr=strr+'Pig'+str(i)+' real,'
            		else:
                		strr=strr+'Pig'+str(i)+' real)'

        	try:
            		create_str='CREATE TABLE HITSTATUS'+strr;   #Query string to create table
            		c.execute(create_str);                      #Create table HITSTATUS
            		conn.commit();                              #Commit changes to database
        	except:                                     #If table already exists
            		print 'DATABASE TABLE EXISTS'

        	#Create table PIGLOCATION
        	#The table stores the location of each pig
        	try:
            		c.execute("""CREATE TABLE PIGLOCATION (PigID Integer PRIMARY KEY, location_X Integer, location_Y Integer)""");
            		conn.commit()
        	except:
            		print 'DATABASE ALREADY EXISTS'
        	conn.close()

            
	#Function to update status of each pig at each iteration
    	def update_Status(self,PigID, status,iter_num):
        	conn=sqlite3.connect('database.db')             #Establish connection with the database
        	c=conn.cursor()
        	query="SELECT * FROM HITSTASTUS WHERE ITERATION='"+iter_num+"'" #Check to see if  the Iteration number has been published before
        	#query="\"\""+query+"\"\""
        	c.execute(query)
        	t=c.fetchone()
        	if t==None:                                                     #If iteration number doesn't exist
			#INSERT NEW ROW FOR THIS ITERATION
            		query="INSERT INTO HITSTATUS (Iteration, Pig"+str(PigID)+") values("+str(iter_num)+","+str(status)+")" 
 			c.execute(query);
            		conn.commit()
        	else:
			#UPDATE STATUS FOR THE PIG IN THE CURR    ENT ITERATION
            		query="UPDATE HITSTATUS SET Pig"+str(PigID)+"="+"\'"+str(status)+"\'"+"WHERE Iteration="+"\'"+str(iter_num)+"\'"
            		#query="\"\""+query+"\"\""
            		c.execute(query);
            		conn.commit()
        	conn.close()
    
	#Function to update location of each pig after each iteration.
	def update_location(self,PigID, loc_x, loc_y):
        	conn=sqlite3.connect('database.db')             #Establish connection with the database
        	c=conn.cursor()
        	query="SELECT * FROM PIGLOCATION WHERE PigID='"+str(PigID)+"'";             #Check if the PigID exists
        	#query="\"\""+query+"\"\"";
        	c.execute(query)
        	t=c.fetchone()
		#If the PigID doesnt exist, add a new row with this PigID and insert its location
        	if t==None:                                                                 
            		query="INSERT INTO PIGLOCATION (PigID, location_X, location_Y) values("+str(PigID)+","+str(loc_x)+","+str(loc_y)+")";
            		c.execute(query);
            		conn.commit()   
        	else:                                                                     #If the PigID exists, update location of the Pig
            		query="UPDATE PIGLOCATION SET location_X='"+str(loc_x)+"', location_Y='"+str(loc_y)+"' WHERE PigID='"+str(PigID)+"'";
            		#query="\"\""+query+"\"\""
            		c.execute(query);
            		c.commit()
        	conn.close()

	#Function returns the status of the Pig. !0 if hit and 0 if not hit
	def get_status(self,PigID):
        	conn=sqlite3.connect('database.db')             #Establish connection with the database
        	c=conn.cursor()
        	is_hit=0;
        	query="SELECT * FROM HITSTATUS WHERE Pig"+str(PigID)+"='1'";
        	#query="\"\""+query+"\"\"";
        	for row in c.execute(query):
            		is_hit=is_hit+1;

        	conn.close()
        	return is_hit

    
	#Function returns the location of the Pig
	def get_loc(self,PigID):
        	conn=sqlite3.connect('database.db')             #Establish connection with the database
        	c=conn.cursor()
        	query="SELECT * from PIGLOCATION WHERE PigID='"+str(PigID)+"'";
        	#query="\"\""+query+"\"\""
        	c.execute(query)
        	row=c.fetchone()
		#print 'Row = = ', row
        	loc=[row[1],row[2]]
        	conn.close()
        	return loc
                
            
##    def update_Status(PigID,status,iter_num):
##        f=open('database.txt','r+');                    #Open File
##        temp=f.read().splitlines();                     #read lines from the file. The content is unformatted
##        f.close()
##        open('database.txt', 'w').close();                  #Clear the file. Everything will be re-written after update.
##        stat=[]
##        for n in range(0,len(temp)):                    #Begin formatting.
##            stat.append([])                             #Creating an empty list of lists. The contents of the file will be stored here in proper format.
##            
##        for i in temp:                                  #Get each line of the file and store in 'stat' as a list.                             
##            j=i.split();
##            for elm in j:
##                stat[temp.index(i)].append(int(elm))    
##        
##        updated=False;                                  #flag
##        for i=0:len(stat):                              #Updating info about current pig in the database
##            if(stat[i][0]==PigId):                      #Check if the current pig has a record in the database
##                if(status=='HIT'):
##                    stat[i].append(1);                  #1 means hit and 0 means not hit
##                else:
##                    stat[i].append(0);
##                updated=True;                           #Set flag if the current pig has a record in the database
##
##        if updated==False:                              #Indicates that the pig doesn't have a record
##            if status=='HIT':
##                stat.append([PigID, 1]);                #Append information about the current pig
##            else:
##                stat.append([PigID, 0]);
##
##        #Write the status into the file
##        f=open('database.txt','w');
##        for l in stat:
##            for e in l:
##		f.writelines(str(e)+' ')
##            f.writelines('\n')
##        f.close();                                      #Update complete.


    

        
            
            

        
                
        
        
        
        
    
    
