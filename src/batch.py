from slam import *

if __name__ == '__main__':
    args = parser.parse_args()

    iter_1_particle = 500
    iter_2_particle = 1500

    iter_1 = plot_map(map_resolution=args.map_resolution,n_particle=iter_1_particle,data=args.data,graph=args.graph,origin_position=args.origin_position,origin_rotate=args.origin_rotate)
    iter_2 = plot_map(map_resolution=args.map_resolution,n_particle=iter_1_particle,data=args.data,graph=args.graph,origin_position=args.origin_position,origin_rotate=args.origin_rotate)
    iter_3 = plot_map(map_resolution=args.map_resolution,n_particle=args.n_particle,data=args.data,graph=args.graph,origin_position=args.origin_position, origin_rotate=args.origin_rotate)

    print(iter_1)
    print(iter_2)
    print(iter_3)