# Segmentación de color mediante el modelo de color HSV

#+BEGIN_SRC python
import cv2 as cv

img = cv.imread('man1.jpg', 1)
hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

uba = (10, 255, 255)
ubb = (0, 40, 40)
uba2 = (180, 255, 255)
ubb2 = (170, 40, 40)

mask1 = cv.inRange(hsv, ubb, uba)
mask2 = cv.inRange(hsv, ubb2, uba2)

mask = mask1 + mask2

res = cv.bitwise_and(img, img, mask=mask)

cv.imshow('mask1', mask1)
cv.imshow('mask2', mask2)
cv.imshow('mask',mask)
cv.imshow('res', res)

cv.waitKey(0)
cv.destroyAllWindows
