from copy import deepcopy
from math import factorial
from time import time

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


def swapPositions(var_node,xnew,ynew,x,y):
#swapPositions() : Takes arguement a var_node , xnew , ynew , x , y .
#					 var_node: a state node  . xnew , ynew , x , y  : cordinates 
# Swaps value of var_node[x][y] with var_node[xnew][ynew] .
	var_node[xnew][ynew], var_node[x][y] = var_node[x][y], var_node[xnew][ynew]
	return var_node

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
		if(abs(find_marker(path[i])[0]-find_marker(path[j])[0])+abs(find_marker(path[i])[1]-find_marker(path[j])[1])==1 and temp<=2):
			optimal_path.append(path[i])
			j=i
			i=i-1			
		else :
			i=i-1
	optimal_path.reverse()
	print(len(optimal_path))
	print("Optimal path : ")
	for i in optimal_path :
		for j in i:
			print(j)
		print("-----------------")
	return optimal_path


def neighbour(node,h):
#neighbour() : Takes arguement a node.
#					node : a state node.
# Expands the given node and returns its lowest cost valid child node.
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
	branch.sort(key= lambda x : x[1])
	return branch[0]

def hill_climbing(node,h):
	path=[]
	op_path=[]
	count=0
	current=deepcopy(node)
	while(1):
		next_state,next_state_cost=neighbour(deepcopy(current),h)
		if next_state_cost>=h(current,goal):
			return (path,current)
		else:
			current=deepcopy(next_state)
			path.append(deepcopy(next_state))
			count=count+1
			
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
		source=[['B','T2','T3'],['T1','T5','T6'],['T4','T7','T8']]
		goal=[['T1','T2','T3'],['T4','T5','T6'],['T7','T8','B']]
	functions=[h1,h2,h3]
	for h in functions:
		t0=time()
		if h==h1:
			print("Using heuristic : number of displaced tiles")
		elif h==h2:
			print("Using heuristic : Manhattan distance ")
		elif h==h3:
			print("Using heuristic : h1(Number of displaced tiles) X h2(Manhattan distance)")
		path,res=hill_climbing(deepcopy(source),h)
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
			print("Optimal Path Cost :")
			print(op_cost)
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