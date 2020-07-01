# ----------
# User Instructions:
# 
# Define a function, search() that returns a list
# in the form of [optimal path length, row, col]. For
# the grid shown below, your function should output
# [11, 4, 5].
#
# If there is no valid path from the start point
# to the goal, your function should return the string
# 'fail'
# ----------

# Grid format:
#   0 = Navigable space
#   1 = Occupied space


grid = [[0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 0],
        [0, 0, 1, 1, 1, 0],
        [0, 0, 0, 0, 1, 0]]
init = [0, 0]
goal = [len(grid)-1, len(grid[0])-1]
cost = 1

delta = [[-1, 0], # go up
         [ 0,-1], # go left
         [ 1, 0], # go down
         [ 0, 1]] # go right

delta_name = ['^', '<', 'v', '>']

def search(grid,init,goal,cost):
    # ----------------------------------------
    # insert code here
    # ----------------------------------------
    flag=False
    new_positions=[]
    to_expand=[0, init[0], init[1]]
    log=[to_expand]
    expanding_position=init
    checked=[init]
    while(not flag):
        #print(log)
        candidate_new_positions=[[expanding_position[0]+move[0], expanding_position[1]+move[1]] for move in delta]
        #print(candidate_new_positions)
        current_cost=to_expand[0]+cost
        for candidate_position in candidate_new_positions:
            if(candidate_position not in checked and candidate_position[0]>=0 and candidate_position[0]<len(grid) and candidate_position[1]>=0 and candidate_position[1]<len(grid[0])): 
                if(grid[candidate_position[0]][candidate_position[1]]==0):
                    new_positions.append([current_cost, candidate_position[0], candidate_position[1]])
                    checked.append(candidate_position)
        #print(new_positions)
        if(new_positions==[]):
            path = 'fail'
            flag = True
        else:
            all_costs=[new_item[0] for new_item in new_positions]
            arg_min_cost=all_costs.index(min(all_costs))
            to_expand = new_positions.pop(arg_min_cost)
            expanding_position=[to_expand[1], to_expand[2]]
            log.append([to_expand[0], expanding_position[0], expanding_position[1]])
            if(expanding_position == goal):
                path=[to_expand[0], expanding_position[0], expanding_position[1]]
                flag=True
            else:
                if(len(checked) == len(grid)*len(grid[0])):
                    path = 'fail'
                    flag = True
            #print('---')    
    return path

#print(search(grid,init,goal,cost))
