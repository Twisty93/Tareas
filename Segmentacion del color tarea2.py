# Segmentación de color mediante el modelo de color HSV

#+BEGIN_SRC python
import cv2 as cv

img = cv.imread('casa.jpg', 1)
hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)




cv.imshow('imagen original',img)
#segmentacion para el color rojo


uba = (10, 255, 255)
ubb = (0, 40, 40)
uba2 = (180, 255, 255)
ubb2 = (170, 40, 40)

mask1 = cv.inRange(hsv, ubb, uba)
mask2 = cv.inRange(hsv, ubb2, uba2)

mask = mask1 + mask2

res = cv.bitwise_and(img, img, mask=mask)


cv.imshow('maskrojo',mask)
cv.imshow('resrojo', res)

#segmentacion para el color azul

uba = (100, 255, 255)
ubb = (90, 40, 40)
uba2 = (135, 255, 255)
ubb2 = (110, 40, 40)

mask1 = cv.inRange(hsv, ubb, uba)
mask2 = cv.inRange(hsv, ubb2, uba2)

mask = mask1 + mask2

res = cv.bitwise_and(img, img, mask=mask)


cv.imshow('maskazul',mask)
cv.imshow('resazul', res)

#segmentacion para el color amarillo
uba = (30, 255, 255)
ubb = (28, 40, 40)
uba2 = (36, 255, 255)
ubb2 = (31, 40, 40)

mask1 = cv.inRange(hsv, ubb, uba)
mask2 = cv.inRange(hsv, ubb2, uba2)

mask = mask1 + mask2

res = cv.bitwise_and(img, img, mask=mask)


cv.imshow('maskamarillo',mask)
cv.imshow('resamarillo', res)

#segmentacion para el color verde
uba = (50, 255, 255)
ubb = (40, 40, 40)
uba2 = (75, 255, 255)
ubb2 = (55, 40, 40)

mask1 = cv.inRange(hsv, ubb, uba)
mask2 = cv.inRange(hsv, ubb2, uba2)

mask = mask1 + mask2

res = cv.bitwise_and(img, img, mask=mask)


cv.imshow('maskverde',mask)
cv.imshow('resverde', res)
cv.imshow('maskamarillo',mask)
cv.imshow('resamarillo', res)

#segmentacion para el color naranja
uba = (20, 255, 255)
ubb = (11, 40, 40)
uba2 = (25, 255, 255)
ubb2 = (20, 40, 40)

mask1 = cv.inRange(hsv, ubb, uba)
mask2 = cv.inRange(hsv, ubb2, uba2)

mask = mask1 + mask2

res = cv.bitwise_and(img, img, mask=mask)


cv.imshow('masknaranja',mask)
cv.imshow('resnaranja', res)

cv.waitKey(0)
cv.destroyAllWindows