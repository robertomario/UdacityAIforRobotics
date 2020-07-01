# ----------
# User Instructions:
# 
# Implement the function optimum_policy2D below.
#
# You are given a car in grid with initial state
# init. Your task is to compute and return the car's 
# optimal path to the position specified in goal; 
# the costs for each motion are as defined in cost.
#
# There are four motion directions: up, left, down, and right.
# Increasing the index in this array corresponds to making a
# a left turn, and decreasing the index corresponds to making a 
# right turn.

forward = [[-1,  0], # go up
           [ 0, -1], # go left
           [ 1,  0], # go down
           [ 0,  1]] # go right
forward_name = ['up', 'left', 'down', 'right']

# action has 3 values: right turn, no turn, left turn
action = [-1, 0, 1]
action_name = ['R', '#', 'L']

# EXAMPLE INPUTS:
# grid format:
#     0 = navigable space
#     1 = unnavigable space 
grid = [[1, 1, 1, 0, 0, 0],
        [1, 1, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 1, 1],
        [1, 1, 1, 0, 1, 1]]

init = [4, 3, 0] # given in the form [row,col,direction]
                 # direction = 0: up
                 #             1: left
                 #             2: down
                 #             3: right
                
goal = [2, 0] # given in the form [row,col]

cost = [2, 1, 20] # cost has 3 values, corresponding to making 
                  # a right turn, no turn, and a left turn

#grid = [[0, 0, 0, 0, 1, 1],
#        [0, 0, 1, 0, 0, 0],
#        [0, 0, 0, 0, 1, 0],
#        [0, 0, 1, 1, 1, 0],
#        [0, 0, 0, 0, 1, 0]]
#init = [4, 5, 0]
#goal = [4, 3]
#cost = [1, 1, 1]

# EXAMPLE OUTPUT:
# calling optimum_policy2D with the given parameters should return 
# [[' ', ' ', ' ', 'R', '#', 'R'],
#  [' ', ' ', ' ', '#', ' ', '#'],
#  ['*', '#', '#', '#', '#', 'R'],
#  [' ', ' ', ' ', '#', ' ', ' '],
#  [' ', ' ', ' ', '#', ' ', ' ']]
# ----------

# ----------------------------------------
# modify code below
# ----------------------------------------

def optimum_policy2D(grid,init,goal,cost):
    value = [[[999 for i in range(len(grid[0]))] for j in range(len(grid))] for k in range(4)]
    closed = [[[0 for i in range(len(grid[0]))] for j in range(len(grid))] for k in range(4)]
    policy2D = [[' ' for i in range(len(grid[0]))] for j in range(len(grid))]
    policy2D[goal[0]][goal[1]] = '*'
    current_value = 0
    opened = [[0, goal[0], goal[1], 0],
              [0, goal[0], goal[1], 1],
              [0, goal[0], goal[1], 2],
              [0, goal[0], goal[1], 3]]
    
    while(len(opened)>0):
        current_position = opened.pop(0)
        closed[current_position[3]][current_position[1]][current_position[2]] = 1
        value[current_position[3]][current_position[1]][current_position[2]] = current_position[0]
        for i in range(len(action)):
            x2 = current_position[1]-forward[current_position[3]][0]
            y2 = current_position[2]-forward[current_position[3]][1]
            new_orientation = current_position[3]-action[i]
            new_orientation %= 4
            
            neighbor = [ x2, y2, new_orientation ]
            if(neighbor[0]>=0 and neighbor[0]<len(grid) and neighbor[1]>=0 and neighbor[1]<len(grid[0])):
                if(closed[neighbor[2]][neighbor[0]][neighbor[1]]==0 and grid[neighbor[0]][neighbor[1]]==0):
                    v2 = current_position[0]+cost[i]
                    opened.append([v2, neighbor[0], neighbor[1], neighbor[2]])
                    value[neighbor[2]][neighbor[0]][neighbor[1]] = v2
#    for i in range(4):
#        for row in value[i]:
#            print(row)
#        print('--')

    current_position=init
    flag=False
    while(not flag):
        x=current_position[0]
        y=current_position[1]
        o=current_position[2]
        possible_new_actions=[]
        possible_new_positions=[]
        possible_new_values=[]
        for i in range(len(action)):
            o2 = o+action[i]
            o2 %= 4
            x2 = x+forward[o2][0]
            y2 = y+forward[o2][1]
            if(x2>=0 and x2<len(grid) and y2>=0 and y2<len(grid[0])):
                if(grid[x2][y2]==0):
                    possible_new_actions.append(i)
                    possible_new_positions.append([x2, y2, o2])
                    possible_new_values.append(value[o2][x2][y2]+cost[i])
        next_index=possible_new_values.index(min(possible_new_values))
        policy2D[x][y]=action_name[possible_new_actions[next_index]]
        current_position=possible_new_positions[next_index]
        if(current_position[0]==goal[0] and current_position[1]==goal[1]):
            flag=True
    return policy2D
    
#x=optimum_policy2D(grid,init,goal,cost)
#for row in x:
#    print(row)