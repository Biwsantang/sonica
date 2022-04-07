from slam import *
import os

if __name__ == '__main__':
    args = parser.parse_args()

    folder_name = os.path.splitext(os.path.basename(args.data.name))[0]
    path_name = os.path.join("../images/batch/", folder_name)
    os.makedirs(path_name, exist_ok=True)

    iter_1_particle = 500
    iter_2_particle = 1500
    iter_3_particle = args.n_particle

    fig_1, iter_1 = plot_map(map_resolution=args.map_resolution,n_particle=iter_1_particle,data=args.data,graph=args.graph,origin_position=args.origin_position,origin_rotate=args.origin_rotate,flip=args.flip)
    fig_2, iter_2 = plot_map(map_resolution=args.map_resolution,n_particle=iter_1_particle,data=args.data,graph=args.graph,origin_position=args.origin_position,origin_rotate=args.origin_rotate,flip=args.flip)
    fig_3, iter_3 = plot_map(map_resolution=args.map_resolution,n_particle=iter_3_particle,data=args.data,graph=args.graph,origin_position=args.origin_position, origin_rotate=args.origin_rotate,flip=args.flip)

    fig_1.savefig(os.path.join(path_name, str(iter_1_particle)+".png"))
    fig_2.savefig(os.path.join(path_name, str(iter_2_particle)+".png"))
    fig_3.savefig(os.path.join(path_name, str(iter_3_particle)+".png"))

    print(iter_1)
    print(iter_2)
    print(iter_3)