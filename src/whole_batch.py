from slam import *
from numpy import genfromtxt
import os

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-m",
        "--map_resolution",
        default=10,
        help="Number of cells to subdivide 1 meter into",
    )
    parser.add_argument(
        "-n1",
        "--n_particle_1",
        default=500,
        help="Number of particles in the particle filter",
    )
    parser.add_argument(
        "-n2",
        "--n_particle_2",
        default=1000,
        help="Number of particles in the particle filter",
    )
    parser.add_argument(
        "-n3",
        "--n_particle_3",
        default=1500,
        help="Number of particles in the particle filter",
    )

    args = parser.parse_args()

    param = genfromtxt('../data/receive/production/param.csv', delimiter=',')

    iter = []

    for i in tqdm(range(len(param))): # len(param)
        file_number = int(param[i][0])
        folder_name = str(file_number)+"_real_robot"
        file_name = folder_name+".mat"

        path_name = os.path.join("../images/production/", folder_name)
        path_file = os.path.join("../data/receive/production", file_name)
        os.makedirs(path_name, exist_ok=True)

        iter_1_particle = args.n_particle_1
        iter_2_particle = args.n_particle_2
        iter_3_particle = args.n_particle_3

        origin_position = (int(param[i][1]),int(param[i][2]))
        origin_rotate = int(param[i][3])
        flip = int(param[i][4])

        fig_1, iter_1 = plot_map(map_resolution=args.map_resolution, n_particle=iter_1_particle, data=path_file,
                                 graph=False, origin_position=origin_position,
                                 origin_rotate=origin_rotate, flip=flip, disable_bar=True)
        fig_2, iter_2 = plot_map(map_resolution=args.map_resolution, n_particle=iter_1_particle, data=path_file,
                                 graph=False, origin_position=origin_position,
                                 origin_rotate=origin_rotate, flip=flip, disable_bar=True)
        fig_3, iter_3 = plot_map(map_resolution=args.map_resolution, n_particle=iter_3_particle, data=path_file,
                                 graph=False, origin_position=origin_position,
                                 origin_rotate=origin_rotate, flip=flip, disable_bar=True)

        fig_1.savefig(os.path.join(path_name, str(iter_1_particle) + ".png"))
        fig_2.savefig(os.path.join(path_name, str(iter_2_particle) + ".png"))
        fig_3.savefig(os.path.join(path_name, str(iter_3_particle) + ".png"))

        iter_1.insert(0, iter_1_particle)
        iter_1.insert(0, file_number)

        iter_2.insert(0, iter_2_particle)
        iter_2.insert(0, file_number)

        iter_3.insert(0, iter_3_particle)
        iter_3.insert(0, file_number)
        
        iter.append(iter_1)
        iter.append(iter_2)
        iter.append(iter_3)

    np.savetxt('../images/production/result.csv', np.array(iter), fmt='%10.5f' , delimiter=',')