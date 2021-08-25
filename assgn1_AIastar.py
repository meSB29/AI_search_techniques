from queue import PriorityQueue
import copy
from math import factorial
from time import time

#Hash function used to save a unique ID for a state . Since the 2nd arguement to a
#priority queue can not be a 2d list, hence a unique string is used .
def hash(node): 
	string=""
	for i in range(len(node)):
		for j in range(len(node[i])):
			string=string+str(node[i][j])+'$'
	return string

#find_marker() : Takes arguement a state node and outputs the (X,Y) coordinates of Blank space/Marker.
# Note that the cordinates are 0-indexed
def find_marker(node):
	# print("find_marker")
	marker_pos=list()
	for i in range(len(node)):
		for j in range(len(node[i])):
			if(node[i][j]=='B'):
				marker_pos=[i,j]
				break
	return marker_pos

#find_pos() : Takes arguement fix_node and val
#			  fix_node : a state node , val : any of the allowed values of a node
#Returns the the (X,Y) coordinates of 'val' in fix_node.
def find_pos(fix_node,val):
	for i in range(len(fix_node)):
		for j in range(len(fix_node)):
			if(fix_node[i][j]==val):
				return [i,j]

#g() : Takes arguement a var_node and a fix_node.
#		var_node: a state node , fix_node 
#Returns least cost from the fix_node to the var_node.
def g(var_node,fix_node):
	# print("heuristic")
	sm=0
	for i in range(len(var_node)):
		for j in range(len(var_node[i])):
			if(str(var_node[i][j])!='B' and var_node[i][j]!=fix_node[i][j]):
				sm=sm+1
	return int(sm)

#h1() : Takes arguement a var_node and a fix_node.
#		var_node: a state node , fix_node 
#Returns : number of displaced tiles between the fix_node and var_node.
def h1(var_node,fix_node):
	sm=0
	for i in range(len(var_node)):
		for j in range(len(var_node[i])):
			if(str(var_node[i][j])!='B' and var_node[i][j]!=fix_node[i][j]):
				sm=sm+1
	return int(sm)

#h2() : Takes arguement a var_node and a fix_node.
#		var_node: a state node , fix_node : a state node
#Returns : Manhattan distance between the fix_node and var_node.
def h2(var_node,fix_node):
	sm=0
	for i in range(len(var_node)):
		for j in range(len(var_node[i])):
			if(str(var_node[i][j])!='B' and var_node[i][j]!=fix_node[i][j]):
				t=find_pos(fix_node,var_node[i][j])
				sm=sm+abs(i-t[0])+abs(j-t[1])
	return int(sm)

#swapPositions() : Takes arguement a var_node , xnew , ynew , x , y .
#					 var_node: a state node  . xnew , ynew , x , y  : cordinates 
# Swaps value of var_node[x][y] with var_node[xnew][ynew] .
def swapPositions(var_node,xnew,ynew,x,y): 
	var_node[xnew][ynew], var_node[x][y] = var_node[x][y], var_node[xnew][ynew]
	return var_node

#BuildSearchSpace() : Takes arguement a node.
#					 node : a state node.
# Expands the given node and stores its all valid child nodes.  
def BuildSearchSpace(node):
	marker_pos=find_marker(node)
	graph=[]
	if  marker_pos[0]-1>=0  :
		node=swapPositions(node,marker_pos[0]-1,marker_pos[1],marker_pos[0],marker_pos[1])
		if node not in open_list and node not in closed_list:
			graph.append(copy.deepcopy(node))	
		node=swapPositions(node,marker_pos[0]-1,marker_pos[1],marker_pos[0],marker_pos[1])

	if marker_pos[0]+1<len(node) :
		# print("yo again")
		node=swapPositions(node,marker_pos[0]+1,marker_pos[1],marker_pos[0],marker_pos[1])
		if node not in open_list and node not in closed_list:
			graph.append(copy.deepcopy(node))
		node=swapPositions(node,marker_pos[0]+1,marker_pos[1],marker_pos[0],marker_pos[1])

	if marker_pos[1]-1>=0	:
		node=swapPositions(node,marker_pos[0],marker_pos[1]-1,marker_pos[0],marker_pos[1])
		if node not in open_list and node not in closed_list:
			graph.append(copy.deepcopy(node))
		node=swapPositions(node,marker_pos[0],marker_pos[1]-1,marker_pos[0],marker_pos[1])

	if marker_pos[1]+1 < len(node):
		node=swapPositions(node,marker_pos[0],marker_pos[1]+1,marker_pos[0],marker_pos[1])
		if node not in open_list and node not in closed_list:
			graph.append(copy.deepcopy(node))
		node=swapPositions(node,marker_pos[0],marker_pos[1]+1,marker_pos[0],marker_pos[1])	
	
	return graph

# op_path() : Takes arguement path(a list containing all the explored states)
#			prints the optimal path from source to goal
def op_path(path):
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

#isSolvable() : Takes arguement source_node and goal_node.
#				source_node : start state in the form of list of list.
#				goal_node : goal_state in the form of list of list.
#Returns :  True if given 8 puzzle is solvable else False
def isSolvable(source_node,goal_node):
    inv_count = 0
    priority={}
    pr_val=0
    for i in range(len(goal_node)):
    	for j in range(len(goal_node)):
	    	if(goal_node[i][j]!='B'):
	    		priority[goal_node[i][j]]=pr_val
	    		pr_val=pr_val+1
    flat_list=[]
    for i in source_node:
    	flat_list.extend(i)

    for i in range(0, len(source_node)**2):
        for j in range(i+1, len(source_node)**2):
            if flat_list[j] != 'B' and flat_list[i] != 'B' and priority[flat_list[i]] > priority[flat_list[j]]:
                inv_count += 1
    return (inv_count%2==0)
     
# Astar() : Takes arguemrnt source and h.
#			source : start state in the form of list if list.
#			h : the heuristic function . May have values h1 or h2.
def Astar(source,h):
	path=[]
	statesum=0
	pq.put((int(h(source,goal)+g(source,source)),hash(source)))
	# graph.append(copy.deepcopy(source))
	open_list.append(source)
	while(pq.empty()==False):
		min_node_str=pq.get()[1]
		statesum=statesum+1
		min_node=[[0 for i in range(3)] for j in range(3)]
		min_node_list=list(min_node_str.split('$'))
		min_node_list.pop()
		for i in range(len(min_node_list)):
			if min_node_list[i]=='B':
				min_node[i//3][i%3]='B'
			else :
				min_node[i//3][i%3]=min_node_list[i]
		path.append(min_node)
		closed_list.append(copy.deepcopy(min_node))
		open_list.pop(open_list.index(copy.deepcopy(min_node)))
		if(min_node==goal):
			print("Success!!")
			print("Start State : ")
			for i in source:
				print(i)
			print("Goal State : ")
			for i in goal:
				print(i)
			print("Total number of states explored: ")
			print(statesum)
			print("Total number of states to optimal path")
			op=op_path(path)
			op_cost=0
			for x in op:
				op_cost=op_cost+int(h(x,goal))
			print("Optimal Path Cost :")
			print(op_cost)
			return
		else:
			graph=BuildSearchSpace(copy.deepcopy(min_node))
			for i in graph:
				x=int(h(i,goal)+g(i,source))
				pq.put((x,hash(i)))
				open_list.append(copy.deepcopy(i))

	
#Input is taken from a file named "myfile.txt"
if __name__=='__main__':
	try:
		with open("myfile.txt",'r') as file:
			st=st+file.read()
		List=list(st.split('\n'))
		source=[str(List[i]).split(' ') for i in range(1,4)]
		goal=[str(List[i]).split(' ') for i in range(5,8)]
		assert len(source)==3 and len(source[0])==3 and len(goal)==3 and len(goal[0])==3
	except:
		source=[['T3','T6','T4'],['B','T1','T2'],['T8','T7','T5']]
		goal=[['T1','T2','T3'],['T8','B','T4'],['T7','T6','T5']]

	if not isSolvable(source,goal):
		print("Failure! Goal state not reached")
		print("Start State : ")
		for i in source:
			print(i)
		print("Goal State : ")
		for i in goal:
			print(i)
		print("Total number of states explored before termination :", end=" ")
		print(factorial(len(source)**2)//2)

	else:
		functions=[h1,h2]
		for h in functions:
			t0=time()
			closed_list=[]
			open_list=[]
			if h==h1:
				print("Using heuristic : number of displaced tiles")
			elif h==h2:
				print("Using heuristic : Manhattan distance ")
			pq=PriorityQueue()
			Astar(copy.deepcopy(source),h)
			t1=time()-t0
			print('Time taken for execution :')
			print(t1)
			print("\n")
	
