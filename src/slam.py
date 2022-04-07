# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from tqdm import tqdm
from scipy.io import loadmat
import matplotlib.pyplot as plt
import math
from crazyslam.slam import SLAM
from crazyslam.localization import get_state_estimate
import argparse
import numpy as np

from scipy import ndimage

from inject import *

from compare import *

parser = argparse.ArgumentParser()
parser.add_argument(
    "-m",
    "--map_resolution",
    default=10,
    help="Number of cells to subdivide 1 meter into",
)
parser.add_argument(
    "-n",
    "--n_particle",
    default=1000,
    help="Number of particles in the particle filter",
)
parser.add_argument(
    "-d",
    "--data",
    type=argparse.FileType('r'),
    default="../data/receive/120_real_robot.mat",
    help="data file to plot as occupancy map"
)
parser.add_argument(
    "-g",
    "--graph",
    action='store_true'
)
parser.add_argument(
    "-op",
    "--origin_position",
    nargs='+',
    type=int,
    required=True
)
parser.add_argument(
    "-or",
    "--origin_rotate",
    default=0,
    type=int
)

class newSLAM(SLAM):
    def view_particles(self):
        return self.particles
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

def plot_map(map_resolution,n_particle,data,graph,origin_position,origin_rotate):
    # Use a breakpoint in the code line below to debug your script.

    data = loadmat(data.name)
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
    states[1] = states[1] * -1
    states[2] = (states[2] - math.radians(90))

    ranges = ranges * 0.01

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
    motion_updates[2, 0] = 0


    # Useful values

    system_noise_variance = np.diag([0.000002, 0.000002, 0.000002]) #0.000002
    correlation_matrix = np.array([
        [0, -1],
        [-1, 10], #10
    ])
    slam_states = np.zeros_like(states_noise)

    #motion_updates[2, 0] = 0

    # Init the SLAM agent
    slam_agent = newSLAM(
        params=init_params_dict(size=4, resolution=map_resolution),
        n_particles=int(n_particle),
        current_state=states_noise[:, 0],
        system_noise_variance=system_noise_variance,
        correlation_matrix=correlation_matrix,
    )

    params = init_params_dict(4, 10)
    occupancy_grid = create_empty_map(params)

    for t in tqdm(range(1,states_noise.shape[1])): #states_noise.shape[1]
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

    groundTruth_raw = np.genfromtxt('../data/receive/groundTruth.csv', delimiter=',')
    groundTruth_raw = np.flip(groundTruth_raw,1)
    groundTruth_raw = ndimage.rotate(groundTruth_raw, origin_rotate)
    groundTruth = np.zeros((40, 40))
    offset = np.array((origin_position[0]-7, origin_position[1]-7)) #19, 12
    groundTruth[offset[0]:offset[0] + groundTruth_raw.shape[0], offset[1]:offset[1] + groundTruth_raw.shape[1]] = groundTruth_raw

    slam_map[slam_map >= 50] = 100 #50
    slam_map[slam_map <= -20] = -50 #-10
    #slam_map[slam_map > -10 & slam_map < 50] = 0
    slam_map[np.where((slam_map > -20) & (slam_map < 50))] = 0

    mse_slam_occu, ssim_slam_occu = compare_map(slam_map, occupancy_grid)

    mse_slam_ground, ssim_slam_ground = compare_map(slam_map, groundTruth)
    mse_occu_ground, ssim_occu_ground = compare_map(occupancy_grid, groundTruth)

    if (graph):
        fig, ax = plt.subplots(1, 4)
        ax[0].imshow(slam_map, cmap="gray")
        ax[0].plot(idx_slam[1, :], idx_slam[0, :], "-r", label="slam")
        ax[0].plot(idx_noise[1, :], idx_noise[0, :], "-y", label="pose")
        ax[0].legend()
        ax[0].annotate("MSE| SLAM->OCCU_MAP:\n"
                       "    {}\n"
                       "MSE| SLAM->GROUND:\n"
                       "    {}\n"
                       "MSE| OCCU_MAP->GROUND:\n"
                       "    {}\n"
                       "MS_SSIM| SLAM->OCCU_MAP:\n"
                       "    {}%\n"
                       "MS_SSIM| SLAM->GROUND:\n"
                       "    {}%\n"
                       "MS_SSIM| OCCU_MAP->GROUND:\n"
                       "    {}%\n"
                       .format(mse_slam_occu, mse_slam_ground, mse_occu_ground, ssim_slam_occu.real*100, ssim_slam_ground.real*100, ssim_occu_ground.real*100),[0,-5],annotation_clip=False)
        ax[0].set_title("SLAM")

        #"""
        ax[1].imshow(occupancy_grid, cmap="gray")
        ax[1].plot(idx_noise[1, :], idx_noise[0, :], "-y", label="pose")
        #ax[1].legend()
        ax[1].set_title("OCCUPANCY")

        ax[2].imshow(groundTruth, cmap="gray")
        #ax[2].legend()
        ax[2].set_title("GROUND TRUTH")

        ax[3].plot(states_noise[1, :], states_noise[0, :], "-y", label="noise")
        ax[3].plot(slam_states[1, :], slam_states[0, :], "-r", label="pose")
        #ax[3].legend()
        #"""
        plt.show()

    return mse_slam_occu, mse_slam_ground, mse_occu_ground, ssim_slam_occu.real*100, ssim_slam_ground.real*100, ssim_occu_ground.real*100

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    args = parser.parse_args()

    print(plot_map(map_resolution=args.map_resolution,n_particle=args.n_particle,data=args.data,graph=args.graph,origin_position=args.origin_position,origin_rotate=args.origin_rotate))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
