import matplotlib.pyplot as plt
import numpy as np
from scipy.io import loadmat
import math


def run():
    data = loadmat("../data/receive/25_real_robot.mat")
    ranges = np.array(data["ranges"])
    angles = np.array(data["scanAngles"])

    num_of_angle = 30
    num_of_sensor = 7

    round = [0] * (num_of_sensor*num_of_angle)
    ranges_fill = []
    time = ranges.shape[1]

    for j in range(time):
        for i in range(num_of_sensor):
            round[num_of_angle * i:num_of_angle * (i+1)] = [ranges[:,j][i]] * num_of_angle
        ranges_fill.append(round)

    ranges_fill = np.array(ranges_fill).T
    print(ranges_fill[:,0])
    print(ranges[:,0])

    angles_fill = np.array(range(-15,195), dtype=np.double).reshape(-1,1)

    for i in range(angles.shape[0]):
        angles_fill[i] = math.radians(angles_fill[i])

    print(angles)
    print(angles_fill)

if __name__ == "__main__":
    run()