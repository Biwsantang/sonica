import scipy.io as sio
import math
from turtle import *

def run():

    mat = sio.loadmat("../data/receive/9_real_robot.mat")
    pose = mat["pose"]
    color('red', 'yellow')
    begin_fill()
    for i in range(pose.shape[1]):
        setheading(math.degrees((pose[2,i]-math.radians(90))))
        #setheading(math.degrees(pose[2, i]))
        #delay(100)
        goto(pose[1,i]*100,pose[0,i]*-100)
    end_fill()
    done()

if __name__ == "__main__":
    run()