import copy
import math
import cProfile
import math

#takes in a filepath
#returns a 2d tuple representing the starting game state
def loadFromFile(filepath):
    f = open(filepath, "r")
    lines = f.readlines()
    N = lines[0].strip()
    final_list = []
    #check if it is the same length as N vertically
    if len(lines) - 1 != int(N):
        return None
    holeExist = False
    for i in range(1,len(lines)):
        lines[i] = lines[i].strip()
        temp = lines[i].split("\t")
        #checks if it is the same length as N horizontally 
        if len(temp) > int(N):
            return None
        #marks it as True if the hole exists 
        for x in lines[i]:
            if x == "*":
                holeExist = True
        final_list.append(tuple(temp))
    #we know for sure that if this is false the hole is not there
    if not holeExist:
        return None
    #checks for redundancy by converting to a set and seeing if the set removes any elements 
    if len(set(flatten(final_list))) != len(flatten(final_list)):
        return None
    return tuple(map(tuple,final_list))

#takes in a game state
#returns a list containing n tuples, where each tuple is a pair with the swapped tile and a 1d representation of how the state would look after the swap
def computeNeighbors(state):
    hole_coords = [0,0]
    adjacent_coords = []
    #finds the coordinates of the hole
    for y in range(len(state)):
        for x in range(len(state[y])):
            if state[y][x] == "*":  
                hole_coords[0] = x
                hole_coords[1] = y     
    adjacent_coords = checkNext(state, hole_coords)
    final_list = []
    state_modified = []
    original = []
    location = 0
    location2 = 0
    original = flatten(state)
    state_modified = flatten(state)
    #for loop to return from computeNeighbors properly            
    for y in range(len(state)):
        for x in range(len(state[y])):
            if (x,y) in adjacent_coords:
                #find x,y in state modified and then swap it with hole. 
                location = state_modified.index(state[y][x])
                location2 = state_modified.index('*')
                state_modified[location], state_modified[location2] = state_modified[location2], state_modified[location]
                final_list.append((state[y][x],tuple(state_modified)))   
                state_modified = copy.copy(original)
    return tuple(final_list)
    
#takes in a gamestate and the hole's coordinates 
#returns a 2d tuple where each element is a tuple of coordinates adjacent to the hole 
def checkNext(state, hole_coords):
    adjacent_coords = []
    for y in range(len(state)): 
        for z in range(len(state[y])):  
            if z != "*":
                if (abs(hole_coords[0] - z) == 1 and hole_coords[1] == y) or (hole_coords[0] == z and abs(hole_coords[1] - y) == 1):
                    adjacent_coords.append((z,y))
    return adjacent_coords

#takes in the starting gamestate
#returns a tuple where each element is a tile that you have to move, from first tile to the last, in order to reach the goal state from the starting state
def BFS(state):    
    frontier = [state]
    #discovered needs to be a set with tuples that represent 1d states 
    discovered = set(map(tuple, flattensp(state)))  
    #state is a 2d tuple already, so since it is hashable I can immediately add it
    parents = {state : ()}
    while len(frontier) != 0:
        current_state = frontier.pop(0)
        discovered.add(tuple(flatten(current_state)))
        if isGoal(current_state):
            #return every key in the dictionary (node) in the order of most recently to last recently placed nodes
            return parents[tuple(map(tuple, current_state))]
        neighbors = convertStates(computeNeighbors(current_state))  
        for neighbor in range(len(neighbors)):
            active_state = neighbors[neighbor]
            if tuple(flatten(active_state)) not in discovered:
                frontier.append(active_state)
                discovered.add(tuple(flatten(active_state)))
                new_path = list(parents[(tuple(map(tuple, current_state)))])
                new_path.append(computeNeighbors(current_state)[neighbor][0])
                parents[tuple(map(tuple, active_state))] = tuple(new_path)


#takes in the starting gamestate
#returns a tuple where each element is a tile that you have to move, from first tile to the last, in order to reach the goal state from the starting state
def DFS(state):
    frontier = [state]
    #discovered needs to be a set with tuples that represent 1d states 
    discovered = set(map(tuple, flattensp(state)))  
    #state is a 2d tuple already, so since it is hashable I can immediately add it
    parents = {state : ()}
    while len(frontier) != 0:
        current_state = frontier.pop(0)
        discovered.add(tuple(flatten(state)))
        if isGoal(current_state):
            #return every key in the dictionary (node) in the order of most recently to last recently placed nodes
            return parents[tuple(map(tuple, current_state))][::-1]
        neighbors = convertStates(computeNeighbors(current_state))  
        for neighbor in range(len(neighbors)):
            active_state = neighbors[neighbor]
            if tuple(flatten(active_state)) not in discovered:
                frontier.insert(0,active_state)
                discovered.add(tuple(flatten(active_state)))
                new_path = list(parents[(tuple(map(tuple, current_state)))])
                #neighbor is 0
                new_path.insert(0, computeNeighbors(current_state)[neighbor][0])
                parents[tuple(map(tuple, active_state))] = tuple(new_path)

#takes in the starting gamestate
#returns a tuple where each element is a tile that you have to move, from first tile to the last, in order to reach the goal state from the starting state
def BDS(state):    
    frontier = [state]
    other_frontier = [constructGoal(state)] 
    #discovered needs to be a set with tuples that represent 1d states 
    discovered = set(map(tuple, flattensp(state))) 
    #print(discovered) 
    other_discovered = set(map(tuple, flattensp(other_frontier[0])))
    #state is a 2d tuple already, so since it is hashable I can immediately add it
    parents = {state : ()}
    other_parents = {other_frontier[0]: ()}
    while len(frontier) != 0 and len(other_frontier) != 0:
        current_state = frontier.pop(0)
        other_current_state = other_frontier.pop(0)
        if (other_discovered & discovered):
            #return the value of the forward dictionary plus the reversed value of the backward 
            key_tuple = onetotwo(tuple(flatten(discovered & other_discovered)))
            forward = parents[key_tuple] 
            backward = other_parents[key_tuple]
            new_tuple = forward + backward[::-1]
            return new_tuple        
        neighbors = convertStates(computeNeighbors(current_state))  
        other_neighbors = convertStates(computeNeighbors(other_current_state))
        for neighbor in range(len(neighbors)):
            active_state1 = neighbors[neighbor]
            if tuple(flatten(active_state1)) not in discovered:
                frontier.append(active_state1)
                discovered.add(tuple(flatten(active_state1)))
                path1 = list(parents[(tuple(map(tuple, current_state)))])    
                path1.append(computeNeighbors(current_state)[neighbor][0])
                parents[tuple(map(tuple, active_state1))] = tuple(path1)
        for other_neighbor in range(len(other_neighbors)):
            active_state2 = other_neighbors[other_neighbor]
            if tuple(flatten(active_state2)) not in other_discovered:
                other_frontier.append(active_state2)
                other_discovered.add(tuple(flatten(active_state2)))
                path2 = list(other_parents[(tuple(map(tuple, other_current_state)))])
                path2.append(computeNeighbors(other_current_state)[other_neighbor][0])
                other_parents[tuple(map(tuple, active_state2))] = tuple(path2)


#takes in the output of computeNeighbors(state)
#returns 3d list, where each element is a 2d list, and each of those 2d lists represents a game state
def convertStates(neighbors):
    n = int(math.sqrt(len(neighbors[0][1])))
    states = []
    for i in neighbors:
        list = i[1]
        state = [[0 for i in range(n)] for j in range(n)]
        line = 0
        for x in range(len(list)):
            if x%n == 0 and x != 0:
                line += 1 
            state[line][x%n] = list[x]
        states.append(state)    
    return states

#turns 1d array into 2d array, given 2d array and n
def onetotwo(value):
    n = int(math.sqrt(len(value)))
    final_list = []
    for x in range(len(value)):
        if (x + 1) % n == 0:
            final_list.append(value[(x + 1 - n) : x + 1])
    final_list = tuple(map(tuple , final_list))
    return final_list

#flatten, only it returns a 2d array that has one element
def flattensp(value):
    final = []
    for y in value:
        for x in y:
                final.append(x)
    #needs to return a 2d list of one 1d element because it is necessary for the discovered set
    return [final]

def flatten(value):
    final = []
    for y in value:
        for x in y:
                final.append(x)
    #needs to return a 2d list of one 1d element because it is necessary for the discovered set
    return final

def isGoal(state):
    goal = []
    latest = 0
    for y in range(len(state)):
        goal_row = []
        for x in range(len(state)):
            if latest == 0:
                goal_row.append("1")
                latest += 1
                continue
            goal_row.append(str(latest + 1))
            latest += 1 
        goal.append(goal_row)
    goal[len(state) - 1][len(state) - 1] = "*"
    #goal = tuple(map(tuple, goal))
    return goal == state

def get_keys(dictionary, goal): 
    final_list = []
    while dictionary[goal] != None:
        final_list.append(dictionary[goal])
        #print(goal, dictionary[goal])
        goal = dictionary[goal]
    return final_list   

#constructs a goal 2d tuple for use in BDS
def constructGoal(state):
    goal = []
    latest = 0
    for y in range(len(state)):
        goal_row = []
        for x in range(len(state)):
            if latest == 0:
                goal_row.append("1")
                latest += 1
                continue
            goal_row.append(str(latest + 1))
            latest += 1 
        goal.append(goal_row)
    goal[len(state) - 1][len(state) - 1] = "*"
    return tuple(map(tuple, goal))