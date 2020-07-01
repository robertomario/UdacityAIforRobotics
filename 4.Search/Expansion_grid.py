# -----------
# User Instructions:
# 
# Modify the function search so that it returns
# a table of values called expand. This table
# will keep track of which step each node was
# expanded.
#
# Make sure that the initial cell in the grid 
# you return has the value 0.
# ----------

grid = [[0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 1, 0],
        [0, 0, 1, 0, 1, 0],
        [0, 0, 1, 0, 1, 0]]
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
    # modify code below
    # ----------------------------------------
    result = []
    for i in range(len(grid)):
        result.append([])
        for j in range(len(grid[0])):
            result[i].append(-1)
    count=0
    result[init[0]][init[1]]=count
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
            count+=1
            result[expanding_position[0]][expanding_position[1]] = count
            log.append([to_expand[0], expanding_position[0], expanding_position[1]])
            if(expanding_position == goal):
                path=[to_expand[0], expanding_position[0], expanding_position[1]]
                flag=True
            else:
                if(len(checked) == len(grid)*len(grid[0])):
                    path = 'fail'
                    flag = True

    return result

#print(search(grid,init,goal,cost))