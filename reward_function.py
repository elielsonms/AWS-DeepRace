MAX_SPEED = 5
SPEED_GRANULARITY = 3
BIAS_ANGLE_DIFF = 5
DEMOTIVATE_VALUE = 1e-3

def is_on_straight_line(params):
    #If on distance between two waypoints could exist an curve this won`t work
    return fit_bias(fullAngle(track_angle(params)),
                    fullAngle(params['heading']), BIAS_ANGLE_DIFF)

def is_straight_ahead(params):
    return fit_bias(fullAngle(track_angle(params)),
                        fullAngle(track_angle_ahead(params)), 1)

# If is on straight line, keep increasing the speed
# If is there curve ahead, reduce speed
# Bad reward if is on the lowest granularity
def reward_for_straight_line(params):
    straight_ahead = is_straight_ahead(params)
    if params['speed'] == MAX_SPEED :
        return max_reward(params) if straight_ahead else lowest_reward(params)
    elif params['speed'] > MAX_SPEED/SPEED_GRANULARITY:
        return parametized_reward(0.5,params)
    else:
        return  lowest_reward(params) if straight_ahead else max_reward(params)

# If the track angle is on differente signal than the car angle, bad reward
def reward_for_curve(params):
    sterring = params['steering_angle']
    car = fullAngle(params['heading'])
    track = fullAngle(track_angle(params))

    if(fit_bias(track, car+sterring,8)):
        return max_reward(params)
    else:
        return lowest_reward(params)

def reward_function(params):
    reward = 1
    if(not params['all_wheels_on_track']):
        reward = lowest_reward(params)
    elif is_on_straight_line(params) : 
        reward = reward_for_straight_line(params)
    else:
        reward = reward_for_curve(params)  

    return float(reward)

def angle(p1,p2):
    import math
    arc = math.atan2(p2[1] - p1[1], p2[0] - p1[0])
    return math.degrees(arc)

def angleOn180(angle):
    if(angle > 180):
        return angle - 360
    return angle

def fullAngle(angle):
    if(angle < 0):
        return 360 + angle
    return angle

def track_angle(params):
    closest_waypoints = params['closest_waypoints']
    waypoints =  params['waypoints']
    prev_point = waypoints[closest_waypoints[0]]
    next_point = waypoints[closest_waypoints[1]]

    return angle(next_point,prev_point)

def track_angle_ahead(params):
    waypoints_ahead = params['closest_waypoints'][1]
    waypoints =  params['waypoints']
    prev_point = waypoints[waypoints_ahead]
    next_point = waypoints[min(waypoints_ahead+1,49)]#avoid arrayIndexOutOfBounds

    return angle(next_point,prev_point)

#give higher reward if is in a more advanced progress
#TODO: Evaluate if really worth
def max_reward(params):
    return 1*params['progress']

def parametized_reward(reward,params):
    return reward*params['progress']

def lowest_reward(params):
    return DEMOTIVATE_VALUE

def fit_bias(angle1, angle2, bias):
    return abs(angle1-angle2) <= bias

aws_params = {
    "all_wheels_on_track": True,    # flag to indicate if the vehicle is on the track
    "x": 0,                        # vehicle's x-coordinate in meters
    "y": 0,                        # vehicle's y-coordinate in meters
    "distance_from_center": 11,     # distance in meters from the track center 
    "is_left_of_center": True,      # Flag to indicate if the vehicle is on the left side to the track center or not. 
    "heading": 45,                  # vehicle's yaw in degrees
    "progress": 0.9,                 # percentage of track completed
    "steps": 0,                      # number steps completed
    "speed": 0,                    # vehicle's speed in meters per second (m/s)
    "steering_angle": 0.0,          # vehicle's steering angle in degrees
    "track_width": 3,              # width of the track
    "waypoints": [[1, 1], [3,3],[3,4]], # list of [x,y] as milestones along the track center
    "closest_waypoints": [0, 1]    # indices of the two nearest waypoints.
}



print(fullAngle(angle([1,1],[3,3]))) #45
print(fullAngle(angle([1,1],[0,0]))) #- 135 / 225
print(fullAngle(angle([1,1],[0,1]))) #180 / -180
print(fullAngle(angle([0,1], [1,1]))) #0/360
print(fullAngle(angle([0,1], [2,2]))) #26/360

print(fullAngle(angle([0,1], [0,1]))) #0/360
print(abs(angle([0,1], [2,2])-angle([1,1],[3,3])))
print(fit_bias(angle([0,1], [2,2]),angle([1,1],[3,3]), 18))

print(fit_bias(fullAngle(angle([1,1],[2,2])),
                        fullAngle(angle([2,2],[3,4])), 1))
#reward_function(aws_params)