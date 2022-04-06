import cv2
import numpy as np
from PIL import Image
from matplotlib import cm, pyplot as plt
from sewar.full_ref import msssim, mse
import scipy.ndimage as ndi

def NormalizeData(data):
    return (data - np.min(data)) / (np.max(data) - np.min(data))

def compare_map(map1, map2):
    image1 = np.array(Image.fromarray(np.uint8(cm.gray(NormalizeData(map1)) * 255)))
    image2 = np.array(Image.fromarray(np.uint8(cm.gray(NormalizeData(map2)) * 255)))

    """
    gray = cv2.cvtColor(image1, cv2.COLOR_RGB2GRAY)
    #smooth = ndi.filters.median_filter(gray, size=2)
    edges = gray > 120

    lines = cv2.HoughLines(edges.astype(np.uint8), 1, np.pi / 180, 1)
    
    for rho, theta in lines[0]:
        print(rho, theta)
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + 1000 * (-b))
        y1 = int(y0 + 1000 * (a))
        x2 = int(x0 - 1000 * (-b))
        y2 = int(y0 - 1000 * (a))
        cv2.line(image1, (x1, y1), (x2, y2), (0,255,0), 2)

    minLineLength = 0
    maxLineGap = 5
    lines = cv2.HoughLinesP(edges.astype(np.uint8), 1, np.pi / 180, 0, minLineLength, maxLineGap)
    if lines:
        for x1, y1, x2, y2 in lines[0]:
            cv2.line(image1, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # Show the result
    plt.imshow(image1,cmap='gray')
    """

    m = mse(image1, image2)
    s = msssim(image1, image2)

    return m,s