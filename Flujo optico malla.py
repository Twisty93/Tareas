import numpy as np
import cv2 as cv

cap = cv.VideoCapture(0)

lkparm = dict(winSize=(15,15), maxLevel=2,
              criteria=(cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 0.03))

_, vframe = cap.read()
vgris = cv.cvtColor(vframe, cv.COLOR_BGR2GRAY)

p0 = np.array([(50,50), (100,50), (150,50), (200,50), (250,50),(300,50),(300,50),
               (50,100), (100,100), (150,100), (200,100), (250,100),(300,100),(300,100),
               (50,150), (100,150), (150,150), (200,150), (250,150),(300,150),(300,150),
               (50,200), (100,200), (150,200), (200,200), (250,200),(300,200),(300,200),
               (50,250), (100,250), (150,250), (200,250), (250,250),(300,250),(300,250),
               (50,300), (100,300), (150,300), (200,300), (250,300),(300,300),(300,300),
               (50,350), (100,350), (150,350), (200,350), (250,350),(300,350),(300,350),
               (50,400), (100,400), (150,400), (200,400), (250,400),(300,400),(300,400),
               ])

p0 = np.float32(p0[:, np.newaxis, :])

mask = np.zeros_like(vframe)

while True:
    _, frame = cap.read()
    fgris = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    p1, st, err = cv.calcOpticalFlowPyrLK(vgris, fgris, p0, None, **lkparm)

    if p1 is None:
        vgris = cv.cvtColor(vframe, cv.COLOR_BGR2GRAY)
        mask = np.zeros_like(vframe)
        cv.imshow('ventana', frame)
    else:
        bp1 = p1[st == 1]
        bp0 = p0[st == 1]


        num_cols = 5  

        for i, (nv, vj) in enumerate(zip(bp1, bp0)):
            a, b = (int(x) for x in nv.ravel())
            c, d = (int(x) for x in vj.ravel())

            frame = cv.circle(frame, (c, d), 2, (255, 0, 0), -1)  
            frame = cv.circle(frame, (a, b), 3, (0, 255, 0), -1)  
            
           
            if (i + 1) % num_cols != 0: 
                next_idx = i + 1
                if next_idx < len(bp1):
                    x2, y2 = (int(x) for x in bp1[next_idx].ravel())
                    frame = cv.line(frame, (a, b), (x2, y2), (0, 255, 255), 1)

            
            down_idx = i + num_cols
            if down_idx < len(bp1): 
                x3, y3 = (int(x) for x in bp1[down_idx].ravel())
                frame = cv.line(frame, (a, b), (x3, y3), (255, 0, 255), 1)

        cv.imshow('ventana', frame)
        vgris = fgris.copy()

        if (cv.waitKey(1) & 0xff) == 27:
            break

cap.release()
cv.destroyAllWindows()
