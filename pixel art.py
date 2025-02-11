import cv2 as cv  
import numpy as np

pixel_art = np.ones((640, 640), dtype=np.uint8) * 255


colores = [100, 200, 150, 100, 200, 150, 200, 150]


for a in range(0, 640, 80):  
    for index, color in enumerate(colores):
        inicio_col = index * 80   
        fin_col = inicio_col + 80
        pixel_art[a:a+160, inicio_col:fin_col] = color



#eee
for i in range(160, 240):
    for j in range(80, 160):
        pixel_art[i, j] = 0 

for i in range(160, 240):
    for j in range(160, 240):
        pixel_art[i, j] = 0 

for i in range(240, 320):
    for j in range(80, 160):
        pixel_art[i, j] = 0 

for i in range(240, 320):
    for j in range(160, 240):
        pixel_art[i, j] = 25

#ooo
for i in range(160, 240):
    for j in range(480, 560):
        pixel_art[i, j] = 0 

for i in range(160, 240):
    for j in range(400, 480):
        pixel_art[i, j] = 0 

for i in range(240, 320):
    for j in range(480, 560):
        pixel_art[i, j] = 0 

for i in range(240, 320):
    for j in range(400, 480):
        pixel_art[i, j] = 25

#uuuuu

for i in range(560, 640):
    for j in range(400, 480):
        pixel_art[i, j] = 0 

for i in range(560, 640):
    for j in range(160, 240):
        pixel_art[i, j] = 0 

#wwwwww
for i in range(400, 560):
    for j in range(160, 480):
        pixel_art[i, j] = 0 


for i in range(320, 400):
    for j in range(240, 400):
        pixel_art[i, j] = 0 


cv.imshow('Pixel Art', pixel_art)
cv.waitKey(0)

