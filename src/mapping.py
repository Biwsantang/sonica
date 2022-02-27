# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import numpy as np
from scipy.io import loadmat
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib
import math
from tqdm import tqdm
from crazyslam.mapping import *

def bresenham_line(start, end):
    """Find the cells that should be selected to form a straight line

    Use scikit-image implementation of the Bresenham line algorithm

    Args:
        start: (x, y) INDEX coordinates of the starting point
        end: ((x, y), n) INDEX coordinates of the ending points

    Returns:
        List of (x, y) INDEX coordinates that form the straight lines
    """
    path = list()
    for target in end.T:  # TODO: delete for loop
        tmp = bresenham(start[0], start[1], target[0], target[1])
        path += (list(zip(tmp[0], tmp[1]))[1:-1])  # start + end points removed
    return path

def update_grid_map(grid, ranges, angles, state, params):
    """Update the grid map given a new set on sensor data

    Args:
        grid: Grid map to be updated
        ranges: Set of range inputs from the sensor
        angles: Angles at which the range points are captured
        state: State estimate (x, y, yaw)
        params: Parameters dictionary

    Returns:
        Updated occupancy grid map
    """
    LOG_ODD_MAX = 4 #100
    LOG_ODD_MIN = -2 #-50
    LOG_ODD_OCCU = 1 #1
    LOG_ODD_FREE = 0.3 #0.3

    # compute the measured position
    targets = target_cell(state, ranges, angles)
    targets = discretize(targets, params)

    # find the affected cells
    position = discretize(state[:2], params)
    cells = bresenham_line(position.reshape(2), targets)

    # update log odds
    grid[tuple(np.array(cells).T)] -= LOG_ODD_FREE
    grid[targets[0], targets[1]] += LOG_ODD_OCCU
    grid[position[0], position[1]] = LOG_ODD_MIN  # LOG_ODD_FREE


    return np.clip(grid, a_max=LOG_ODD_MAX, a_min=LOG_ODD_MIN)

def run():
    # Use a breakpoint in the code line below to debug your script.

    data = loadmat("../data/receive/62_real_robot.mat")
    states = np.array(data["pose"])
    ranges = np.array(data["ranges"])
    angles = np.array(data["scanAngles"])
    timestamp = np.array(data["t"])

    #start fill
    '''
    num_of_angle = 30
    num_of_sensor = 7

    round = [0] * (num_of_sensor * num_of_angle)
    ranges_fill = []
    time = ranges.shape[1]

    for j in range(time):
        for i in range(num_of_sensor):
            round[num_of_angle * i:num_of_angle * (i + 1)] = [ranges[:, j][i]] * num_of_angle
        ranges_fill.append(round.copy())

    ranges_fill = np.array(np.array(ranges_fill).T)

    angles_fill = np.array(np.array(range(-15,195), dtype=np.double).reshape(-1,1))

    for i in range(angles_fill.shape[0]):
        angles_fill[i] = math.radians(angles_fill[i])

    ranges = ranges_fill
    angles = angles_fill
    '''
    #end

    states[0] = states[0] * 1
    states[1] = states[1] * -1
    states[2] = (states[2]-math.radians(90))

    ranges = ranges * 0.01

    params = init_params_dict(5, 100)
    occupancy_grid = create_empty_map(params)

    idx_pose = discretize(states[:2, :], params)

    matplotlib.rc('xtick', labelsize=5)
    matplotlib.rc('ytick', labelsize=5)
    fig, ax = plt.subplots()
    #ax.imshow(occupancy_grid, cmap="gray")
    #ax.plot(idx_pose[1, :], idx_pose[0, :], "-y", label="pose")
    #plt.show()

    ims = []

    for i in tqdm(range(states.shape[1])): #for i in tqdm(range(states.shape[1])):
        occupancy_grid = update_grid_map(
            occupancy_grid,
            ranges[:, i],
            angles,
            states[:, i],
            params
        )
        #im = ax.imshow(occupancy_grid, animated=True)
        #ims.append([im])

    #ani = animation.ArtistAnimation(fig, ims, interval=10, blit=True, repeat_delay=1000)

    ax.imshow(occupancy_grid, cmap="gray")
    ax.plot(idx_pose[1, :], idx_pose[0, :], "-y", label="pose")
    plt.show()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    run()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
