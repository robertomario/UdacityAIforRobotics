# ----------
# User Instructions:
# 
# Create a function compute_value which returns
# a grid of values. The value of a cell is the minimum
# number of moves required to get from the cell to the goal. 
#
# If a cell is a wall or it is impossible to reach the goal from a cell,
# assign that cell a value of 99.
# ----------

grid = [[0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0]]
goal = [len(grid)-1, len(grid[0])-1]
cost = 1 # the cost associated with moving from a cell to an adjacent one

delta = [[-1, 0 ], # go up
         [ 0, -1], # go left
         [ 1, 0 ], # go down
         [ 0, 1 ]] # go right

delta_name = ['^', '<', 'v', '>']

def compute_value(grid,goal,cost):
    # ----------------------------------------
    # insert code below
    # ----------------------------------------
    value = [[99 for i in range(len(grid[0]))] for j in range(len(grid))]
    closed = [[0 for i in range(len(grid[0]))] for j in range(len(grid))]
    current_value = 0
    opened = [[0, goal[0], goal[1]]]
    
    while(len(opened)>0):
        current_position = opened.pop(0)
        closed[current_position[1]][current_position[2]] = 1
        value[current_position[1]][current_position[2]] = current_position[0]
        for i in range(len(delta)):
            neighbor = [ current_position[1]+delta[i][0], current_position[2]+delta[i][1] ]
            if(neighbor[0]>=0 and neighbor[0]<len(grid) and neighbor[1]>=0 and neighbor[1]<len(grid[0])):
                if(closed[neighbor[0]][neighbor[1]]==0 and grid[neighbor[0]][neighbor[1]]==0):
                    opened.append([current_position[0]+cost, neighbor[0], neighbor[1]])
        
    # make sure your function returns a grid of values as 
    # demonstrated in the previous video.
    return value 

x = compute_value(grid,goal,cost)
for row in x:
    print(row)