MAX_STEERING_ANGLE=30  #1 TO 30
STEERIMG_GRANULARITY=3 #3,5,7
ANGLE_BIAS=(MAX_STEERING_ANGLE*2)/(STEERIMG_GRANULARITY-1) / 2
MAX_SPEED = 8 #1 TO 8
SPEED_GRANULARITY = 3 #1 TO 3
SPEED_BIAS=(MAX_SPEED/SPEED_GRANULARITY)/2
DEMOTIVATE_VALUE = 1e-3

def reward_function(params):
    reward = 1
    if(not params['all_wheels_on_track']):
        reward = lowest_reward(params)
    elif is_on_correct_angle(params) : 
        reward = reward_for_correct_angle(params)
    else:
        reward = lowest_reward(params)

    return float(reward)

#If diference between car angle (prev point [x,y] w/ car [x,y])  and the track angle (prev point [x,y] w/ next point [x,y]) 
#is higher than half of the steering gap the car should correct this
def is_on_correct_angle(params):
    return fit_bias(fullAngle(track_angle(params)),
                    fullAngle(car_angle_over_prev_waypoint(params)), ANGLE_BIAS)

def is_straight_ahead(params):
    return fit_bias(fullAngle(track_angle(params)),
                        fullAngle(track_angle_ahead(params)), 1)

#If there no curve ahead, speed up
def reward_for_correct_angle(params):
    if(SPEED_GRANULARITY == 1):
        return max_reward(params)
    else:
        #Check angle ahead
        angle_ahead = abs(fullAngle(track_angle_ahead(params))-fullAngle(track_angle(params)))
        is_on_high_speed = fit_bias(params['speed'], MAX_SPEED, SPEED_BIAS)
        if(angle_ahead > ANGLE_BIAS): #will need to correct the angle, so reduce speed
            return lowest_reward(params) if is_on_high_speed else max_reward(params)
        else:
            return max_reward(params) if is_on_high_speed else lowest_reward(params)

# If the track angle is on differente signal than the car angle, bad reward
def reward_for_curve(params):
    sterring = params['steering_angle']
    car = fullAngle(params['heading'])
    track = fullAngle(track_angle(params))

    if(fit_bias(track, car+sterring,8)):
        return max_reward(params)
    else:
        return lowest_reward(params)

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

def car_angle_over_prev_waypoint(params):
    closest_waypoints = params['closest_waypoints']
    waypoints =  params['waypoints']
    prev_point = waypoints[closest_waypoints[0]]
    car_point = [params['x'],params['y']]

    return angle(car_point,prev_point)

def track_angle_ahead(params):
    waypoints_ahead = params['closest_waypoints'][1]
    waypoints =  params['waypoints']
    prev_point = waypoints[waypoints_ahead]
    next_point = waypoints[min(waypoints_ahead+1,waypoints.__len__()-1)]#avoid arrayIndexOutOfBounds

    return angle(next_point,prev_point)

#give higher reward if is in a more advanced progress
#TODO: Evaluate if really worth
def max_reward(params):
    return (params['progress']*10) + 1

def parametized_reward(reward,params):
    return reward*params['progress']

def lowest_reward(params):
    return (params['progress']*-10)

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

print(ANGLE_BIAS)
#reward_function(aws_params)