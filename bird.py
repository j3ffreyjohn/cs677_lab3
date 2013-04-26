#This is the bird process which spawns all other processes

import sys
import random

N = int(sys.argv[1])		# N is the number of pigs in the system
M = int(sys.argv[2])		# M is the number of bird launches in one game

#Choose two pigs to be the coordinators at random
coordinators = random.sample(range(1,N+1),2)	
pigs = list(set(range(1,N+1)) - set(coordinators))

#Assign the rest of the pigs to one of these coordinators
random.shuffle(pigs)
pigs_split = [pigs[i::2] for i in range(2)]	#Assign the pigs randomly to one of the coordinators

