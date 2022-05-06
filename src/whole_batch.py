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
        "-n",
        "--n_particle",
        nargs='+',
        type=int,
    )

    args = parser.parse_args()

    params = genfromtxt('../data/receive/production/param.csv', delimiter=',')

    all_result = []

    print(len(args.n_particle))

    for particle in args.n_particle:
        print("Start generating map with {particle}".format(particle=particle))
        for param in tqdm(params): # len(param)
            file_number = int(param[0])
            folder_name = str(file_number)+"_real_robot"
            file_name = folder_name+".mat"

            path_name = os.path.join("../images/production/", folder_name)
            path_file = os.path.join("../data/receive/production", file_name)
            os.makedirs(path_name, exist_ok=True)

            iter_particle = particle

            origin_position = (int(param[1]),int(param[2]))
            origin_rotate = int(param[5])
            post_position = (int(param[3]),int(param[4]))
            flip = int(param[6])

            fig, iter = plot_map(map_resolution=args.map_resolution, n_particle=iter_particle, data=path_file,
                                    graph=False, origin_position=origin_position, post_position=post_position, post_rotate=origin_rotate,
                                    origin_rotate=origin_rotate, flip=flip, disable_bar=True)

            fig.savefig(os.path.join(path_name, str(iter_particle) + ".png"))

            result = []

            result.insert(0, iter[2])
            result.insert(0, iter[1])
            result.insert(0, iter[0])
            result.insert(0, iter_particle)
            result.insert(0, file_number)
            
            all_result.append(result)

    np.savetxt('../images/production/result.csv', np.array(all_result), fmt='%10.5f' , delimiter=',')