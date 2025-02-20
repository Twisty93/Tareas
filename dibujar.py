import cv2 as cv
import numpy as np

img = np.ones((500, 500, 3), dtype=np.uint8) * 255
cv.circle(img, (250, 250), 50, (0, 234, 21), -1)
cv.circle(img, (250, 250), 30, (0, 0, 0), -1)

cv.line(img, (1, 1), (230, 240), (0, 234, 21), 3)
cv.rectangle(img, (20, 20), (50, 60), (0, 0, 0), 3)

pts = np.array([[10, 5], [20, 30], [70, 20], [50, 10]], np.int32)
pts = pts.reshape(-1, 1, 2)
cv.polylines(img, [pts], True, (0, 0, 0), 3)

cv.imshow('img', img)
cv.waitKey()
cv.destroyAllWindows()
