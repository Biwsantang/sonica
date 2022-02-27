import scipy.io as sio

def run():
    straight = sio.loadmat("2x2_7s_straight.mat")
    curve = sio.loadmat("2x2_7s_curve.mat")

    sio.savemat("2x2_7s_straight_w_curve.mat", {
        'init_pose': straight["init_pose"],
        'pose': curve["pose"],
        'ranges': straight["ranges"],
        'scanAngles': straight["scanAngles"],
        't': straight["t"]
    })

    sio.savemat("2x2_7s_curve_w_straight.mat", {
        'init_pose': curve["init_pose"],
        'pose': straight["pose"],
        'ranges': curve["ranges"],
        'scanAngles': curve["scanAngles"],
        't': curve["t"]
    })

if __name__ == '__main__':
    run()