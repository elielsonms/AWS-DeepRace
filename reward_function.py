MAX_SPEED = 5
SPEED_GRANULARITY = 3

def is_on_straight_line(params):
    return track_angle(params) == params['headings']

# If is on straight line, keep increasing the speed
# Bad reward if is on the lowest granularity
def reward_for_straight_line(params):
    if params['speed'] == MAX_SPEED :
        return 1
    elif params['speed'] > MAX_SPEED/SPEED_GRANULARITY:
        return 0.5
    else:
        return 1e-3
    

# If the track angle is on differente signal than the car angle, bad reward
def reward_for_curve(params):
    car = params['steering_angle']
    track = angleOn180(track_angle(params))

    if car*track < 0 :
        return 1e-3
    else:
         return 1 

def reward_function(params):
    reward = 1
    if(not params['all_wheels_on_track']):
        reward = 1e-3
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

def track_angle(params):
    closest_waypoints = params['closest_waypoints']
    waypoints =  params['waypoints']
    prev_point = waypoints[closest_waypoints[0]]
    next_point = waypoints[closest_waypoints[1]]

    
    return angle(next_point,prev_point)

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



print(angle([1,1],[3,3])) #45
print(angle([1,1],[0,0])) #- 135 / 225
print(angle([1,1],[0,1])) #180 / -180
print(angle([0,1], [1,1])) #0/360
print(angle([0,1], [2,2])) #0/360

#reward_function(aws_params)