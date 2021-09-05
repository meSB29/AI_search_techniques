from copy import deepcopy
from math import factorial,exp
from time import time
import random
import sys 



def find_marker(node):
#find_marker() : Takes arguement a state node and outputs the (X,Y) coordinates of Blank space/Marker.
# Note that the cordinates are 0-indexed
	marker_pos=list()
	for i in range(len(node)):
		for j in range(len(node[i])):
			if(node[i][j]=='B'):
				marker_pos=[i,j]
				break
	return marker_pos

def h1(var_node,fix_node):
#h1() : Takes arguement a var_node and a fix_node.
#		var_node: a state node , fix_node 
#Returns : number of displaced tiles between the fix_node and var_node.	
	sm=0
	for i in range(len(var_node)):
		for j in range(len(var_node[i])):
			if(str(var_node[i][j])!='B' and var_node[i][j]!=fix_node[i][j]):
				sm=sm+1
	return int(sm)

def h2(var_node,fix_node):
#h2() : Takes arguement a var_node and a fix_node.
#		var_node: a state node , fix_node : a state node
#Returns : Manhattan distance between the fix_node and var_node.	
	sm=0
	for i in range(len(var_node)):
		for j in range(len(var_node[i])):
			if(str(var_node[i][j])!='B' and var_node[i][j]!=fix_node[i][j]):
				t=find_pos(fix_node,var_node[i][j])
				sm=sm+abs(i-t[0])+abs(j-t[1])
	return int(sm)

def h3(var_node,fix_node):
	return h1(var_node,fix_node)*h2(var_node,fix_node)

def find_pos(fix_node,val):
#find_pos() : Takes arguement fix_node and val
#			  fix_node : a state node , val : any of the allowed values of a node
#Returns the the (X,Y) coordinates of 'val' in fix_node.
	for i in range(len(fix_node)):
		for j in range(len(fix_node)):
			if(fix_node[i][j]==val):
				return [i,j]


def op_path(path):
# op_path() : Takes arguement path(a list containing all the explored states)
#			prints the optimal path from source to goal
	optimal_path=[]
	optimal_path.append(path[-1])
	j=len(path)-1
	i=len(path)-2
	while(i>=0 and j>i):
		temp=0
		for x in range(len(path[i])):
			for y in range(len(path[i][0])):
				if path[i][x][y] != path[j][x][y]:
					temp=temp+1
		if(abs(find_marker(path[i])[0]-find_marker(path[j])[0])+abs(find_marker(path[i])[1]-find_marker(path[j])[1])==1 and temp<=2 ):
			optimal_path.append(path[i])
			j=i
			i=i-1			
		else :
			i=i-1
	optimal_path.reverse()
	print(len(optimal_path))
	return optimal_path

def swapPositions(var_node,xnew,ynew,x,y):
#swapPositions() : Takes arguement a var_node , xnew , ynew , x , y .
#					 var_node: a state node  . xnew , ynew , x , y  : cordinates 
# Swaps value of var_node[x][y] with var_node[xnew][ynew] .
	var_node[xnew][ynew], var_node[x][y] = var_node[x][y], var_node[xnew][ynew]
	return var_node

def random_state_generator(node,h):
#random_state_generator() : Takes arguement a node.
#					node : a state node.
# Expands the given node and returns a random valid child node.
	branch=[]
	marker_pos=find_marker(node)
	if  marker_pos[0]-1>=0  :
		node=swapPositions(node,marker_pos[0]-1,marker_pos[1],marker_pos[0],marker_pos[1])
		branch.append([deepcopy(node),h(node,goal)])
		node=swapPositions(node,marker_pos[0]-1,marker_pos[1],marker_pos[0],marker_pos[1])
	if marker_pos[0]+1<len(node) :
		node=swapPositions(node,marker_pos[0]+1,marker_pos[1],marker_pos[0],marker_pos[1])
		branch.append([deepcopy(node),h(node,goal)])
		node=swapPositions(node,marker_pos[0]+1,marker_pos[1],marker_pos[0],marker_pos[1])
	if marker_pos[1]-1>=0	:
		node=swapPositions(node,marker_pos[0],marker_pos[1]-1,marker_pos[0],marker_pos[1])
		branch.append([deepcopy(node),h(node,goal)])
		node=swapPositions(node,marker_pos[0],marker_pos[1]-1,marker_pos[0],marker_pos[1])
	if marker_pos[1]+1 < len(node):
		node=swapPositions(node,marker_pos[0],marker_pos[1]+1,marker_pos[0],marker_pos[1])
		branch.append([deepcopy(node),h(node,goal)])
		node=swapPositions(node,marker_pos[0],marker_pos[1]+1,marker_pos[0],marker_pos[1])
	
	return branch[random.randint(0,len(branch)-1)]


def anneal(node,h):

	path=[]
	path.append(deepcopy(node))
	C=factorial(len(node)**2)/2
	current=deepcopy(node)
	while(1) :
		T=min(h(current,goal),C)
		if T<=0:
			return (path,current)
		next_state,next_state_cost=random_state_generator(deepcopy(current),h)
		deltaE=h(current,goal)-next_state_cost
		if deltaE>0:
			current=deepcopy(next_state)
			path.append(deepcopy(current))
		else :
			Rnum=random.randint(0,10**6)/10**6
			probNextState=exp(deltaE/T)
			if Rnum<=probNextState :
				current=deepcopy(next_state)
				path.append(deepcopy(current))
		C=C-1

#OUTPUT GETS STORED IN SA_output.txt
#INPUT OF START STATE AND GOAL STATE IS TAKEN FROM myfile.txt
if __name__ == '__main__':
	st=""
	try:
		with open("myfile.txt",'r') as file:
			st=st+file.read()
		List=list(st.split('\n'))
		source=[str(List[i]).split(' ') for i in range(1,4)]
		goal=[str(List[i]).split(' ') for i in range(5,8)]
		assert len(source)==3 and len(source[0])==3 and len(goal)==3 and len(goal[0])==3
	except:
		source=[['T5','T4','T6'],['T2','T3','T1'],['B','T7','T8']]
		goal=[['T1','T2','T3'],['T4','T5','T6'],['T7','T8','B']]
	stdoutOrigin=sys.stdout 
	sys.stdout = open("SA_output.txt", "w")
	print("Temperature chosen : minimum(Cost(current,goal),maximum number of states)")
	print("Cooling function : maximum number of states - 1")
	functions=[h1,h2,h3]
	for h in functions:
		t0=time()
		if h==h1:
			print("Using heuristic : Number of displaced tiles")
		elif h==h2:
			print("Using heuristic : Manhattan distance ")
		elif h==h3:
			print("Using heuristic : h1(Number of displaced tiles) X h2(Manhattan distance)")
		path,res=anneal(deepcopy(source),h)
		if(res==goal):
			print("Success!!")
			print("Start State : ")
			for i in source:
				print(i)
			print("Goal State : ")
			for i in goal:
				print(i)
			print("Total number of states explored: ")
			print(len(path))
			print("Total number of states to optimal path")
			op=op_path(path)
			op_cost=0
			for x in op:
				op_cost=op_cost+int(h(x,goal))	
		else:
			print("Failure! Goal state not reached")
			print("Start State : ")
			for i in source:
				print(i)
			print("Goal State : ")
			for i in goal:
				print(i)
			print("Total number of states explored before termination :", end=" ")
			print(len(path))
		t1=time()-t0
		print('Time taken for execution :')
		print(t1)
		print("\n")
	sys.stdout.close()
	sys.stdout=stdoutOrigin