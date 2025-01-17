# --------------
# USER INSTRUCTIONS
#
# Write a function called stochastic_value that 
# returns two grids. The first grid, value, should 
# contain the computed value of each cell as shown 
# in the video. The second grid, policy, should 
# contain the optimum policy for each cell.
#
# --------------
# GRADING NOTES
#
# We will be calling your stochastic_value function
# with several different grids and different values
# of success_prob, collision_cost, and cost_step.
# In order to be marked correct, your function must
# RETURN (it does not have to print) two grids,
# value and policy.
#
# When grading your value grid, we will compare the
# value of each cell with the true value according
# to this model. If your answer for each cell
# is sufficiently close to the correct answer
# (within 0.001), you will be marked as correct.

delta = [[-1, 0 ], # go up
         [ 0, -1], # go left
         [ 1, 0 ], # go down
         [ 0, 1 ]] # go right

delta_name = ['^', '<', 'v', '>'] # Use these when creating your policy grid.

# ---------------------------------------------
#  Modify the function stochastic_value below
# ---------------------------------------------

def stochastic_value(grid,goal,cost_step,collision_cost,success_prob):
    failure_prob = (1.0 - success_prob)/2.0 # Probability(stepping left) = prob(stepping right) = failure_prob
    value = [[collision_cost for col in range(len(grid[0]))] for row in range(len(grid))]
    policy = [[' ' for col in range(len(grid[0]))] for row in range(len(grid))]
    
    change = True

    while change:
        change = False

        for x in range(len(grid)):
            for y in range(len(grid[0])):
                if goal[0] == x and goal[1] == y:
                    if value[x][y] > 0:
                        value[x][y] = 0
                        change = True
                elif grid[x][y] == 0:
                    for a in range(len(delta)):
                        x2 = []
                        y2 = []
                        v2 = []
                        
                        x2.append(x + delta[a][0])
                        y2.append(y + delta[a][1])
                        x2.append(x + delta[(a-1)%4][0])
                        y2.append(y + delta[(a-1)%4][1])
                        x2.append(x + delta[(a+1)%4][0])
                        y2.append(y + delta[(a+1)%4][1])

                        for b in range(len(x2)):
                            if x2[b] >= 0 and x2[b] < len(grid) and y2[b] >= 0 and y2[b] < len(grid[0]) and grid[x2[b]][y2[b]] == 0:
                                v2.append(value[x2[b]][y2[b]])
                            else:
                                v2.append(collision_cost)
                        v3 = success_prob*v2[0] + failure_prob*v2[1] + failure_prob*v2[2] + cost_step

                        if v3 < value[x][y]:
                            change = True
                            value[x][y] = v3
    
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if(value[i][j]<collision_cost):
                base_action_value = []
                for a in range(len(delta)):
                    x2 = i + delta[a][0]
                    y2 = j + delta[a][1]

                    if x2 >= 0 and x2 < len(grid) and y2 >= 0 and y2 < len(grid[0]) and grid[x2][y2]==0:
                        base_action_value.append(value[x2][y2])
                    else:
                        base_action_value.append(collision_cost)
                action_value = []
                for a in range(len(delta)):
                    action_value.append(success_prob*base_action_value[a]+failure_prob*base_action_value[(a-1)%4]+failure_prob*base_action_value[(a+1)%4])
                min_action_value=min(action_value)
                best_action=action_value.index(min_action_value)
                policy[i][j] = delta_name[best_action]
    policy[goal[0]][goal[1]] = '*'
    
    return value, policy

# ---------------------------------------------
#  Use the code below to test your solution
# ---------------------------------------------

grid = [[0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 1, 1, 0]]
goal = [0, len(grid[0])-1] # Goal is in top right corner
cost_step = 1
collision_cost = 1000
success_prob = 0.5

value,policy = stochastic_value(grid,goal,cost_step,collision_cost,success_prob)
for row in value:
    print row
for row in policy:
    print row

# Expected outputs:
#
#[471.9397246855924, 274.85364957758316, 161.5599867065471, 0],
#[334.05159958720344, 230.9574434590965, 183.69314862430264, 176.69517762501977], 
#[398.3517867450282, 277.5898270101976, 246.09263437756917, 335.3944132514738], 
#[700.1758933725141, 1000, 1000, 668.697206625737]


#
# ['>', 'v', 'v', '*']
# ['>', '>', '^', '<']
# ['>', '^', '^', '<']
# ['^', ' ', ' ', '^']
