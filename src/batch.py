from slam import *
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
        action='store_true',
        help="Option to show result graph"
    )
    parser.add_argument(
        "-op",
        "--origin_position",
        nargs='+',
        type=int,
        default=(26,19),
        help="Origin coordinator of ground truth map (x,y)"
    )
    parser.add_argument(
        "-or",
        "--origin_rotate",
        default=0,
        type=int,
        help="Rotation of ground truth map (degree)"
    )
    parser.add_argument(
        "-f",
        "--flip",
        action='store_true',
        help="Option to flip map"
    )

    args = parser.parse_args()

    folder_name = os.path.splitext(os.path.basename(args.data.name))[0]
    path_name = os.path.join("../images/batch/", folder_name)
    os.makedirs(path_name, exist_ok=True)

    iter_1_particle = 500
    iter_2_particle = 1500
    iter_3_particle = args.n_particle

    fig_1, iter_1 = plot_map(map_resolution=args.map_resolution,n_particle=iter_1_particle,data=args.data.name,graph=args.graph,origin_position=args.origin_position,origin_rotate=args.origin_rotate,flip=args.flip,disable_bar=True)
    fig_2, iter_2 = plot_map(map_resolution=args.map_resolution,n_particle=iter_1_particle,data=args.data.name,graph=args.graph,origin_position=args.origin_position,origin_rotate=args.origin_rotate,flip=args.flip,disable_bar=True)
    fig_3, iter_3 = plot_map(map_resolution=args.map_resolution,n_particle=iter_3_particle,data=args.data.name,graph=args.graph,origin_position=args.origin_position, origin_rotate=args.origin_rotate,flip=args.flip,disable_bar=True)

    fig_1.savefig(os.path.join(path_name, str(iter_1_particle)+".png"))
    fig_2.savefig(os.path.join(path_name, str(iter_2_particle)+".png"))
    fig_3.savefig(os.path.join(path_name, str(iter_3_particle)+".png"))

    print(iter_1)
    print(iter_2)
    print(iter_3)