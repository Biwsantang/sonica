"""CheapSLAM controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot

import math
import scipy.io as sio
import numpy as np

def run_robot(robot):

    # get the time step of the current world.
    #timestep = int(robot.getBasicTimeStep())
    timestep = 64
    
    timeLimit = 64
    
    #M_mat = []
    init_pose_mat = []
    pose_mat = []
    ranges_mat = []
    # for 8 sensor robot
    #scanAngles_mat = [0.3926991,1.178097,1.9634954,2.7488936,3.5342917,4.3196899,5.1050881,5.8904862]
    # for 7 sensor robot
    scanAngles_mat = [0,0.3926991,1.178097,1.5708,1.9634954,2.7488936,3.14159265]
    #scanAngles_mat = [3.14159265,2.7488936,1.9634954,1.5708,1.178097,0.03926991,0]
    t_mat = []
    
    
    ds_num = 7
    ds = [None] * ds_num
    ds_values = [None] * ds_num
    for n in range(ds_num):
        ds[n] = robot.getDevice('ds'+str(n))
        ds[n].enable(timestep)
    
    max_speed = 6.28
    
    left_motor = robot.getDevice('left wheel motor')
    right_motor = robot.getDevice('right wheel motor')
    
    left_motor.setPosition(float('inf'))
    left_motor.setVelocity(1)
    
    right_motor.setPosition(float('inf'))
    right_motor.setVelocity(1) # 0.95 for curve
    
    #cReate position sensor instances
    
    left_ps = robot.getDevice('left wheel sensor')
    left_ps.enable(timestep)
    
    right_ps = robot.getDevice('right wheel sensor')
    right_ps.enable(timestep)
    
    ps_values =[0, 0]
    dist_values = [0, 0]
    
    # compute encoder unit
    wheel_radius = 0.025
    distance_between_wheels = 0.09
    
    wheel_cirum = 2 * 3.14 * wheel_radius
    encoder_unit = wheel_cirum/6.28
    
    #robot pose
    robot_pose = [0, 0, 0] # x, y, theta
    last_ps_values = [0, 0]
    
    ps_noise = [115.23751728105348,52.29433975275286]
    #ps_noise[0] = left_ps.getValue()
    #ps_noise[1] = right_ps.getValue()
    
    # Main loop:
    # - perform simulation steps until Webots is stopping the controller
    while robot.step(timestep) != -1:
        
        # Read valus from position sensor
        ps_values[0] = left_ps.getValue() - ps_noise[0]
        ps_values[1] = right_ps.getValue() - ps_noise[1]
        
        print("---------------------")
        t_mat.append(robot.getTime())
        print(robot.getTime())
        print("position sensor values: {} {}".format(ps_values[0], ps_values[1]))

        
        for ind in range(2):
            diff = ps_values[ind] - last_ps_values[ind]
            if diff < 0.001:
                diff = 0
                ps_values[ind] = last_ps_values[ind]
            dist_values[ind] = diff * encoder_unit
            
        print("dist_values: {} {}".format(dist_values[0], dist_values[1]))
        # Compute linear and angular velocity for robot
        v = (dist_values[0] + dist_values[1])/2.0
        w = (dist_values[0] - dist_values[1])/distance_between_wheels
        
        dt = 1
        robot_pose[2] += (w*dt) # w*dt
        
        vx = v * math.cos(robot_pose[2])
        vy = v * math.sin(robot_pose[2])
        
        robot_pose[0] += (vx * dt)
        robot_pose[1] += (vy * dt)
        
        print("robot_pose: {}".format(robot_pose))
        pose_mat.append(robot_pose.copy())

        for ind in range(2):
            last_ps_values[ind] = ps_values[ind]
            
        for n in range(ds_num):
            ds_values[n] = ds[n].getValue()
            
        print("distance values: {}".format(ds_values))
        ranges_mat.append(ds_values.copy())
        
        if robot.getTime() > timeLimit:
            break
        
    left_motor.setVelocity(0)
    right_motor.setVelocity(0)
    
    #print("=======COMPELETE========")
    #print("M: {}".format(M_mat))
    #init_pose_mat = pose_mat[0]
    #print("init_pose: {}".format(init_pose_mat))
    #print("pose: {}".format(pose_mat))
    #print("ranges: {}".format(ranges_mat))
    #print("scanAngles: {}".format(scanAngles_mat))
    #print("t: {}".format(t_mat))
    
    print("==========LEN============")
    #print("M: {}".format(len(M_mat)))
    init_pose_mat = pose_mat[0]
    print("init_pose: {}".format(len(init_pose_mat)))
    print("pose: {}".format(len(pose_mat)))
    print("ranges: {}".format(len(ranges_mat)))
    print("scanAngles: {}".format(len(scanAngles_mat)))
    print("t: {}".format(len(t_mat)))
   
    
    print("=============SAVE==========")
    sio.savemat("2x2_7s_straight.mat", {
    'init_pose':np.array(init_pose_mat).reshape(-1,1),
    'pose':np.array(pose_mat).T,
    'ranges':np.array(ranges_mat).T,
    'scanAngles':np.array(scanAngles_mat).reshape(-1,1),
    't':np.array(t_mat).T
    })
    
    print("=============MAT==========")
    mat = sio.whosmat('test_webot.mat')
    print(mat)
    
    

if __name__ == "__main__":
    # create the Robot instance.
    my_robot = Robot()
    run_robot(my_robot)
    
    
