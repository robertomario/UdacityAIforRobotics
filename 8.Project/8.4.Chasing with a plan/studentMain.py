# ----------
# Part Four
#
# Again, you'll track down and recover the runaway Traxbot. 
# But this time, your speed will be about the same as the runaway bot. 
# This may require more careful planning than you used last time.
#
# ----------
# YOUR JOB
#
# Complete the next_move function, similar to how you did last time. 
#
# ----------
# GRADING
# 
# Same as part 3. Again, try to catch the target in as few steps as possible.

from robot import *
from math import *
from matrix import *
import random

def next_move(hunter_position, hunter_heading, target_measurement, max_distance, OTHER = None):
    # This function will be called after each time the target moves. 
    next_pos, OTHER = estimate_next_pos(target_measurement, OTHER)
    distance_est = distance_between(hunter_position, next_pos)
    if(distance_est > max_distance):
        distance = max_distance
        if(OTHER["count"]>1):
            flag = False
            num_steps = 2
            future_distance = OTHER["sum_distance_ests"]/OTHER["count"]
            future_turning = OTHER["sum_turning_ests"]/OTHER["count"]
            future_pos = next_pos
            future_heading = OTHER["next_heading"]
            while not flag:
                x_est = future_pos[0] + future_distance * cos(future_heading)
                y_est = future_pos[1] + future_distance * sin(future_heading)
                future_pos = (x_est, y_est)
                future_separation = distance_between(hunter_position, future_pos)
                if(future_separation/num_steps < max_distance):
                    flag = True
                else:
                    num_steps += 1
                    future_heading = angle_trunc(future_heading + future_turning)
            print(num_steps)
            desired_heading = get_heading(hunter_position, future_pos)
        else:
            desired_heading = get_heading(hunter_position, next_pos)
    else:
        distance = distance_est
        desired_heading = get_heading(hunter_position, next_pos)
    turning = desired_heading - hunter_heading
    # The OTHER variable is a place for you to store any historical information about
    # the progress of the hunt (or maybe some localization information). Your return format
    # must be as follows in order to be graded properly.
    return turning, distance, OTHER

def estimate_next_pos(measurement, OTHER = None):
    """Estimate the next (x, y) position of the wandering Traxbot
    based on noisy (x, y) measurements."""
    if OTHER is None:
        xy_estimate = measurement
        OTHER = {"previous_measurement": measurement, "previous_heading": None, "sum_distance_ests": 0, "sum_turning_ests": 0, "count": 0, "next_heading": None}
    else:
        distance_est = distance_between(measurement, OTHER["previous_measurement"])
        heading_est = angle_trunc(atan2(measurement[1]-OTHER["previous_measurement"][1], measurement[0]-OTHER["previous_measurement"][0]))
        x_est, y_est = measurement
        if OTHER["previous_heading"] is None:
            x_est += distance_est * cos(heading_est)
            y_est += distance_est * sin(heading_est)
        else:
            turning_est = angle_trunc(heading_est - OTHER["previous_heading"])
            OTHER["sum_distance_ests"] += distance_est
            OTHER["sum_turning_ests"] += turning_est
            OTHER["count"] += 1
            next_heading = angle_trunc(heading_est + OTHER["sum_turning_ests"]/OTHER["count"])
            OTHER["next_heading"] = next_heading
            x_est += OTHER["sum_distance_ests"]/OTHER["count"] * cos(next_heading)
            y_est += OTHER["sum_distance_ests"]/OTHER["count"] * sin(next_heading)
        xy_estimate = (x_est, y_est)
        OTHER["previous_measurement"] = measurement
        OTHER["previous_heading"] = heading_est
    # You must return xy_estimate (x, y), and OTHER (even if it is None) 
    # in this order for grading purposes.
    return xy_estimate, OTHER

def distance_between(point1, point2):
    """Computes distance between point1 and point2. Points are (x, y) pairs."""
    x1, y1 = point1
    x2, y2 = point2
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def demo_grading(hunter_bot, target_bot, next_move_fcn, OTHER = None):
    """Returns True if your next_move_fcn successfully guides the hunter_bot
    to the target_bot. This function is here to help you understand how we 
    will grade your submission."""
    max_distance = 0.98 * target_bot.distance # 0.98 is an example. It will change.
    separation_tolerance = 0.02 * target_bot.distance # hunter must be within 0.02 step size to catch target
    caught = False
    ctr = 0

    # We will use your next_move_fcn until we catch the target or time expires.
    while not caught and ctr < 1000:

        # Check to see if the hunter has caught the target.
        hunter_position = (hunter_bot.x, hunter_bot.y)
        target_position = (target_bot.x, target_bot.y)
        separation = distance_between(hunter_position, target_position)
        print(hunter_position)
        print(target_position)
        print(separation)
        print("****"+str(ctr)+"****")
        if separation < separation_tolerance:
            print "You got it right! It took you ", ctr, " steps to catch the target."
            caught = True

        # The target broadcasts its noisy measurement
        target_measurement = target_bot.sense()

        # This is where YOUR function will be called.
        turning, distance, OTHER = next_move_fcn(hunter_position, hunter_bot.heading, target_measurement, max_distance, OTHER)
        
        # Don't try to move faster than allowed!
        if distance > max_distance:
            distance = max_distance

        # We move the hunter according to your instructions
        hunter_bot.move(turning, distance)

        # The target continues its (nearly) circular motion.
        target_bot.move_in_circle()

        ctr += 1            
        if ctr >= 1000:
            print "It took too many steps to catch the target."
    return caught



def angle_trunc(a):
    """This maps all angles to a domain of [-pi, pi]"""
    while a < 0.0:
        a += pi * 2
    return ((a + pi) % (pi * 2)) - pi

def get_heading(hunter_position, target_position):
    """Returns the angle, in radians, between the target and hunter positions"""
    hunter_x, hunter_y = hunter_position
    target_x, target_y = target_position
    heading = atan2(target_y - hunter_y, target_x - hunter_x)
    heading = angle_trunc(heading)
    return heading

def naive_next_move(hunter_position, hunter_heading, target_measurement, max_distance, OTHER):
    """This strategy always tries to steer the hunter directly towards where the target last
    said it was and then moves forwards at full speed. This strategy also keeps track of all 
    the target measurements, hunter positions, and hunter headings over time, but it doesn't 
    do anything with that information."""
    if not OTHER: # first time calling this function, set up my OTHER variables.
        measurements = [target_measurement]
        hunter_positions = [hunter_position]
        hunter_headings = [hunter_heading]
        OTHER = (measurements, hunter_positions, hunter_headings) # now I can keep track of history
    else: # not the first time, update my history
        OTHER[0].append(target_measurement)
        OTHER[1].append(hunter_position)
        OTHER[2].append(hunter_heading)
        measurements, hunter_positions, hunter_headings = OTHER # now I can always refer to these variables
    
    heading_to_target = get_heading(hunter_position, target_measurement)
    heading_difference = heading_to_target - hunter_heading
    turning =  heading_difference # turn towards the target
    distance = max_distance # full speed ahead!
    return turning, distance, OTHER

target = robot(0.0, 10.0, 0.0, 2*pi / 30, 1.5)
measurement_noise = .05*target.distance
target.set_noise(0.0, 0.0, measurement_noise)

hunter = robot(-10.0, -10.0, 0.0)

print demo_grading(hunter, target, next_move)





