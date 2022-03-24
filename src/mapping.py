# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from scipy.io import loadmat
import matplotlib.pyplot as plt
import matplotlib
import math
from tqdm import tqdm
import argparse

from inject import *

parser = argparse.ArgumentParser()
parser.add_argument(
    "--map_resolution",
    default=10,
    help="Number of cells to subdivide 1 meter into",
)
parser.add_argument(
    "--data",
    type=argparse.FileType('r'),
    default="../data/receive/1_real_robot.mat",
    help="data file to plot as occupancy map"
)

def main():

    # Use a breakpoint in the code line below to debug your script.

    args = parser.parse_args()

    data = loadmat(args.data.name)
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

    params = init_params_dict(10, args.map_resolution)
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
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
