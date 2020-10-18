import copy
def loadFromFile(filepath):
    f = open(filepath, "r")
    lines = f.readlines()
    N = lines[0].strip()
    final_list = []
    if len(lines) - 1 != int(N):
        return None
    holeExist = False
    for i in range(1,len(lines)):
        lines[i] = lines[i].strip()
        temp = lines[i].split("\t")
        if len(temp) > int(N):
            return None
        for x in lines[i]:
            if x == "*":
                holeExist = True
        final_list.append(temp)
    if not holeExist:
        return None
    return final_list   

def computeNeighbors(state):
    hole_coords = [0,0]
    adjacent_coords = []
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
    for y in state:
        for x in y: 
            if x != "*":
                state_modified.append(x)
                original.append(x)
            else:
                state_modified.append("0")
                original.append("0")
    #for loop to return from computeNeighbors properly            
    for y in range(len(state)):
        for x in range(len(state[y])):
            if (x,y) in adjacent_coords:
                #find x,y in state modified and then swap it with hole. 
                location = state_modified.index(state[y][x])
                location2 = state_modified.index('0')
                state_modified[location], state_modified[location2] = state_modified[location2], state_modified[location]
                final_list.append((state[y][x],state_modified))    
                state_modified = copy.deepcopy(original)
    return final_list

def checkNext(state, hole_coords):
    adjacent_coords = []
    for y in range(len(state)): 
        for z in range(len(state[y])):
            if z != "*":
                if (abs(hole_coords[0] - z) == 1 and hole_coords[1] == y) or (hole_coords[0] == z and abs(hole_coords[1] - y) == 1):
                    adjacent_coords.append((z,y))
    return adjacent_coords

def BFS(state):
    frontier = [state]
    discovered = set(state)
    parents = {state: None}
    while len(frontier) != 0:
        current_state = frontier.pop(0)
        discovered.add(current_state)
        if isGoal(current_state):
            return get_key(current_state, parents)
        for neighbor in computeNeighbors(current_state):
            if neighbor in discovered:
                frontier.append(neighbor)
                discovered.add(neighbor)
                parents[neighbor:current_state]
        
     
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
    return goal == state

def get_key(val, dictionary): 
    for key, value in dictionary.items(): 
         if val == value: 
             return key 
#print(isGoal(loadFromFile("/home/pranav/Solving-n-puzzle/input.txt")))
print(BFS(loadFromFile("/home/pranav/Solving-n-puzzle/input.txt")))
            
        

    

        
    
    
