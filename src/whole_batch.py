from slam import *
from numpy import genfromtxt
import os

if __name__ == '__main__':
    args = parser.parse_args()

    param = genfromtxt('../data/receive/param.csv', delimiter=',')

    for i in tqdm(range(len(param))): # len(param)
        folder_name = str(int(param[i][0]))+"_real_robot"
        file_name = folder_name+".mat"

        path_name = os.path.join("../images/batch/", folder_name)
        path_file = os.path.join("../data/receive/", file_name)
        os.makedirs(path_name, exist_ok=True)

        iter_1_particle = 500
        iter_2_particle = 1500
        iter_3_particle = args.n_particle

        origin_position = (int(param[i][1]),int(param[i][2]))
        origin_rotate = int(param[i][3])
        flip = int(param[i][4])

        fig_1, iter_1 = plot_map(map_resolution=args.map_resolution, n_particle=iter_1_particle, data=path_file,
                                 graph=args.graph, origin_position=origin_position,
                                 origin_rotate=origin_rotate, flip=flip, disable_bar=True)
        fig_2, iter_2 = plot_map(map_resolution=args.map_resolution, n_particle=iter_1_particle, data=path_file,
                                 graph=args.graph, origin_position=origin_position,
                                 origin_rotate=origin_rotate, flip=flip, disable_bar=True)
        fig_3, iter_3 = plot_map(map_resolution=args.map_resolution, n_particle=iter_3_particle, data=path_file,
                                 graph=args.graph, origin_position=origin_position,
                                 origin_rotate=origin_rotate, flip=flip, disable_bar=True)

        fig_1.savefig(os.path.join(path_name, str(iter_1_particle) + ".png"))
        fig_2.savefig(os.path.join(path_name, str(iter_2_particle) + ".png"))
        fig_3.savefig(os.path.join(path_name, str(iter_3_particle) + ".png"))