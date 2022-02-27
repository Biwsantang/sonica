# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from tqdm import tqdm
from scipy.io import loadmat
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import math
from crazyslam.slam import SLAM
from crazyslam.localization import get_state_estimate
from crazyslam.mapping import *

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
    LOG_ODD_MAX = 100 #100
    LOG_ODD_MIN = -50 #-50
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
    grid[position[0], position[1]] = LOG_ODD_MIN #LOG_ODD_FREE

    return np.clip(grid, a_max=LOG_ODD_MAX, a_min=LOG_ODD_MIN)

class newSLAM(SLAM):
    def update_state(self, ranges, angles, motion_update):
        """
        Update state estimate. One iteration of the SLAM algorithm

        Args:
            ranges: Set on range inputs from sensor
            angles: Scan angles
            motion_update: Update to apply to the current state

        Returns:
            Updated state estimate

        """
        # map update
        self.map = update_grid_map(
            self.map,
            ranges,
            angles,
            self.current_state,
            self.params,
        )

        # motion model update
        self.particles[:3, :] += motion_update.reshape((3, 1)) \
                                 * np.ones((3, self.n_particles))

        # state update
        self.current_state, self.particles = get_state_estimate(
            self.particles,
            self.system_noise_variance,
            self.correlation_matrix,
            self.map,
            self.params,
            ranges,
            angles,
            self.resampling_threshold
        )
        return self.current_state

def run():
    # Use a breakpoint in the code line below to debug your script.

    data = loadmat("../data/2x2_straight_w_curve.mat")
    states = np.array(data["pose"])
    ranges = np.array(data["ranges"])
    angles = np.array(data["scanAngles"])

    # start fill
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

    angles_fill = np.array(np.array(range(-15, 195), dtype=np.double).reshape(-1, 1))

    for i in range(angles_fill.shape[0]):
        angles_fill[i] = math.radians(angles_fill[i])

    ranges = ranges_fill
    angles = angles_fill
    '''
    # end

    states[0] = states[0] * 1
    states[1] = states[1] * 1
    states[2] = (states[2] - math.radians(90))

    #ranges = ranges * 0.01

    # add noise to the ground truth
    motion_updates = np.diff(states, axis=1, prepend=np.zeros((3, 1)))
    noise = np.concatenate([
        np.random.normal(
            loc=0,
            scale=0,
            size=states.shape[1]*2
        ).reshape((2, -1)),
        np.random.normal(
            loc=0,
            scale=0,
            size=states.shape[1]
        ).reshape((1, -1))
    ], axis=0)
    motion_updates += noise
    states_noise = np.cumsum(motion_updates, axis=1)

    # Useful values

    system_noise_variance = np.diag([0.01, 0.01, 0.01]) #0.2
    correlation_matrix = np.array([
        [0, -1],
        [-1, 10], #10
    ])
    slam_states = np.zeros_like(states_noise)

    #motion_updates[2, 0] = 0

    # Init the SLAM agent
    slam_agent = newSLAM(
        params=init_params_dict(size=5, resolution=10),
        n_particles=int(5000),
        current_state=states_noise[:, 0],
        system_noise_variance=system_noise_variance,
        correlation_matrix=correlation_matrix,
    )

    params = init_params_dict(5, 10)
    occupancy_grid = create_empty_map(params)

    for t in tqdm(range(states_noise.shape[1])): #states_noise.shape[1]
        slam_states[:, t] = slam_agent.update_state(
            ranges[:, t],
            angles,
            motion_updates[:, t],
        )
        occupancy_grid = update_grid_map(
            occupancy_grid,
            ranges[:, t],
            angles,
            states_noise[:, t],
            params
        )

    slam_map = slam_agent.map
    idx_slam = discretize(slam_states[:2, :], slam_agent.params)
    idx_noise = discretize(states_noise[:2, :], slam_agent.params)

    fig, ax = plt.subplots(1, 3)
    ax[0].imshow(slam_map, cmap="gray")
    ax[0].plot(idx_slam[1, :], idx_slam[0, :], "-r", label="slam")
    ax[0].plot(idx_noise[1, :], idx_noise[0, :], "-y", label="pose")
    ax[0].legend()

    ax[1].imshow(occupancy_grid, cmap="gray")
    ax[1].plot(idx_noise[1, :], idx_noise[0, :], "-y", label="pose")
    ax[1].legend()

    ax[2].plot(states_noise[1, :], states_noise[0, :], "-y", label="noise")
    ax[2].plot(slam_states[1, :], slam_states[0, :], "-r", label="pose")
    ax[2].legend()
    plt.show()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    run()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
