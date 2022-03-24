import numpy as np
from skimage.metrics import structural_similarity as ssim

def mse(map1, map2):
    err = np.sum((map1.astype("float") - map2.astype("float")) ** 2)
    err /= float(map1.shape[0] * map2.shape[1])

    return err

def compare_map(map1, map2):
    # compute the mean squared error and structural similarity
    # index for the images
    m = mse(map1,map2)
    s = ssim(map1, map2)

    return m,s