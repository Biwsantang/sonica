import cv2
import numpy

background = numpy.zeros((40,40))
img = numpy.genfromtxt('../data/receive/groundTruth.csv', delimiter=',')
offset = numpy.array((0,0), dtype=numpy.uint8)
background[offset[0]:offset[0]+img.shape[0],offset[1]:offset[1]+img.shape[1]] = img

uint_img = numpy.array(background*255).astype('uint8')

grayImage = cv2.cvtColor(uint_img, cv2.COLOR_GRAY2BGR)

edges = cv2.Canny(background, 70, 110, apertureSize=3)
cv2.imshow("test", edges)
cv2.waitKey(0)
cv2.destroyAllWindows()