# -------------------
# Background Information
#
# In this problem, you will build a planner that helps a robot
# find the shortest way in a warehouse filled with boxes
# that he has to pick up and deliver to a drop zone.
#
# For example:
#
# warehouse = [[ 1, 2, 3],
#              [ 0, 0, 0],
#              [ 0, 0, 0]]
# dropzone = [2,0]
# todo = [2, 1]
#
# The robot starts at the dropzone.
# The dropzone can be in any free corner of the warehouse map.
# todo is a list of boxes to be picked up and delivered to the dropzone.
#
# Robot can move diagonally, but the cost of a diagonal move is 1.5.
# The cost of moving one step horizontally or vertically is 1.
# So if the dropzone is at [2, 0], the cost to deliver box number 2
# would be 5.

# To pick up a box, the robot has to move into the same cell as the box.
# When the robot picks up a box, that cell becomes passable (marked 0)
# The robot can pick up only one box at a time and once picked up
# it has to return the box to the dropzone by moving onto the dropzone cell.
# Once the robot has stepped on the dropzone, the box is taken away,
# and it is free to continue with its todo list.
# Tasks must be executed in the order that they are given in the todo list.
# You may assume that in all warehouse maps, all boxes are
# reachable from beginning (the robot is not boxed in).

# -------------------
# User Instructions
#
# Design a planner (any kind you like, so long as it works!)
# in a function named plan() that takes as input three parameters:
# warehouse, dropzone, and todo. See parameter info below.
#
# Your function should RETURN the final, accumulated cost to do
# all tasks in the todo list in the given order, which should
# match with our answer. You may include print statements to show
# the optimum path, but that will have no effect on grading.
#
# Your solution must work for a variety of warehouse layouts and
# any length of todo list.
#
# Add your code at line 76.
#
# --------------------
# Parameter Info
#
# warehouse - a grid of values, where 0 means that the cell is passable,
# and a number 1 <= n <= 99 means that box n is located at that cell.
# dropzone - determines the robot's start location and the place to return boxes
# todo - list of tasks, containing box numbers that have to be picked up
#
# --------------------
# Testing
#
# You may use our test function below, solution_check(),
# to test your code for a variety of input parameters.

warehouse = [[1, 2, 3], [0, 0, 0], [0, 0, 0]]
dropzone = [2, 0]
todo = [2, 1]

# ------------------------------------------
# plan - Returns cost to take all boxes in the todo list to dropzone
#
# ----------------------------------------
# modify code below
# ----------------------------------------
from math import sqrt

delta = [
    [1, 0],  # Go down
    [-1, 0],  # Go up
    [0, 1],  # Go right
    [0, -1],  # Go left
    [1, 1],  # Go down-right
    [1, -1],  # Go down-left
    [-1, 1],  # Go up-right
    [-1, -1],
]  # Go up-left

costs = [1.0, 1.0, 1.0, 1.0, 1.5, 1.5, 1.5, 1.5]


def find_box(warehouse, box_number):
    solution = [-1, -1]
    for i in range(len(warehouse)):
        for j in range(len(warehouse[0])):
            if warehouse[i][j] == box_number:
                solution = [i, j]
    return solution


def find_cost(grid, init, goal):
    for row in grid:
        print (row)
    print (init)
    print (goal)
    cost = 0.0
    # heuristic = [[max(abs(col - goal[0]), abs(row - goal[1])) for col in range(len(grid[0]))] for row in range(len(grid))]
    heuristic = [
        [
            sqrt((col - goal[1]) ** 2 + (row - goal[0]) ** 2)
            for col in range(len(grid[0]))
        ]
        for row in range(len(grid))
    ]
    closed = [[0 for col in range(len(grid[0]))] for row in range(len(grid))]
    closed[init[0]][init[1]] = 1
    expand = [[-1 for col in range(len(grid[0]))] for row in range(len(grid))]
    action = [[-1 for col in range(len(grid[0]))] for row in range(len(grid))]
    x = init[0]
    y = init[1]
    g = 0
    f = heuristic[x][y] + g
    opened = [[f, g, x, y]]
    found = False  # flag that is set when search is complete
    resign = False  # flag set if we can't find expand
    count = 0

    while not found and not resign:
        if len(opened) == 0:
            resign = True
            return "Fail"
        else:
            opened.sort()
            opened.reverse()
            next_point = opened.pop()
            f = next_point[0]
            g = next_point[1]
            x = next_point[2]
            y = next_point[3]
            expand[x][y] = count
            count += 1

            if x == goal[0] and y == goal[1]:
                found = True
            else:
                for i in range(len(delta)):
                    x2 = x + delta[i][0]
                    y2 = y + delta[i][1]
                    if x2 >= 0 and x2 < len(grid) and y2 >= 0 and y2 < len(grid[0]):
                        if closed[x2][y2] == 0 and grid[x2][y2] == 0:
                            g2 = g + costs[i]
                            f2 = heuristic[x2][y2] + g2
                            opened.append([f2, g2, x2, y2])
                            closed[x2][y2] = 1
    for row in expand:
        print (row)
    for row in heuristic:
        print (row)
    x = goal[0]
    y = goal[1]
    flag = False
    while not flag:
        print ("(" + str(x) + ", " + str(y) + ")")
        possible_actions = []
        possible_score = []
        for i in range(len(delta)):
            x2 = x + delta[i][0]
            y2 = y + delta[i][1]
            if x2 >= 0 and x2 < len(grid) and y2 >= 0 and y2 < len(grid[0]):
                if grid[x2][y2] == 0 and expand[x2][y2] > -1:
                    possible_actions.append(i)
                    possible_score.append(expand[x2][y2])
        best_action = possible_actions[possible_score.index(min(possible_score))]
        x = x + delta[best_action][0]
        y = y + delta[best_action][1]
        cost += costs[best_action]
        if x == init[0] and y == init[1]:
            flag = True
    return cost


def plan(warehouse, dropzone, todo):
    cost = 0.0
    for i in range(len(todo)):
        box_location = find_box(warehouse, todo[i])
        simple_warehouse = [
            [warehouse[row][col] for col in range(len(warehouse[0]))]
            for row in range(len(warehouse))
        ]
        for i in range(len(simple_warehouse)):
            for j in range(len(simple_warehouse[0])):
                if simple_warehouse[i][j] > 0:
                    simple_warehouse[i][j] = 1
        simple_warehouse[box_location[0]][box_location[1]] = 0
        simple_warehouse[dropzone[0]][dropzone[1]] = 0
        current_cost = find_cost(simple_warehouse, dropzone, box_location)
        cost += 2 * current_cost
        warehouse[box_location[0]][box_location[1]] = 0
    return cost


################# TESTING ##################

# ------------------------------------------
# solution check - Checks your plan function using
# data from list called test[]. Uncomment the call
# to solution_check to test your code.
#
def solution_check(test, epsilon=0.00001):
    answer_list = []

    import time

    start = time.clock()
    correct_answers = 0
    for i in range(len(test[0])):
        user_cost = plan(test[0][i], test[1][i], test[2][i])
        true_cost = test[3][i]
        if abs(user_cost - true_cost) < epsilon:
            print "\nTest case", i + 1, "passed!"
            answer_list.append(1)
            correct_answers += 1
            # print "#############################################"
        else:
            print "\nTest case ", i + 1, "unsuccessful. Your answer ", user_cost, "was not within ", epsilon, "of ", true_cost
            answer_list.append(0)
    runtime = time.clock() - start
    if runtime > 1:
        print "Your code is too slow, try to optimize it! Running time was: ", runtime
        return False
    if correct_answers == len(answer_list):
        print "\nYou passed all test cases!"
        return True
    else:
        print "\nYou passed", correct_answers, "of", len(
            answer_list
        ), "test cases. Try to get them all!"
        return False


# Testing environment
# Test Case 1
warehouse1 = [[1, 2, 3], [0, 0, 0], [0, 0, 0]]
dropzone1 = [2, 0]
todo1 = [2, 1]
true_cost1 = 9
# Test Case 2
warehouse2 = [[1, 2, 3, 4], [0, 0, 0, 0], [5, 6, 7, 0], ["x", 0, 0, 8]]
dropzone2 = [3, 0]
todo2 = [2, 5, 1]
true_cost2 = 21

# Test Case 3
warehouse3 = [
    [1, 2, 3, 4, 5, 6, 7],
    [0, 0, 0, 0, 0, 0, 0],
    [8, 9, 10, 11, 0, 0, 0],
    ["x", 0, 0, 0, 0, 0, 12],
]
dropzone3 = [3, 0]
todo3 = [5, 10]
true_cost3 = 18

# Test Case 4
warehouse4 = [
    [1, 17, 5, 18, 9, 19, 13],
    [2, 0, 6, 0, 10, 0, 14],
    [3, 0, 7, 0, 11, 0, 15],
    [4, 0, 8, 0, 12, 0, 16],
    [0, 0, 0, 0, 0, 0, "x"],
]
dropzone4 = [4, 6]
todo4 = [13, 11, 6, 17]
true_cost4 = 41

testing_suite = [
    [warehouse1, warehouse2, warehouse3, warehouse4],
    [dropzone1, dropzone2, dropzone3, dropzone4],
    [todo1, todo2, todo3, todo4],
    [true_cost1, true_cost2, true_cost3, true_cost4],
]


solution_check(testing_suite)  # UNCOMMENT THIS LINE TO TEST YOUR CODE
