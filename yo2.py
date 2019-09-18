import cv2
import numpy as np
import sys

from matplotlib import pyplot as plt

def pushToJS(data):
    print(str(data));
    sys.stdout.flush()

def none(value):
    pass

thresholdValue = 0

cv2.namedWindow("test")

cv2.createTrackbar("thresh", "test", thresholdValue, 255, none)

camera = cv2.VideoCapture(0)

def centroid(max_contour):
    moment = cv2.moments(max_contour)
    if(moment['m00'] != 0):
       cx = int(moment['m10'] / moment['m00'])
       cy = int(moment['m01'] / moment['m00'])
       return cx, cy
    else:
       return None

def farthest_point(defects, contour, centroid):
    if defects is not None and centroid is not None:
        s = defects[:, 0][:, 0]
        cx, cy = centroid

        x = np.array(contour[s][:, 0][:, 0], dtype=np.float)
        y = np.array(contour[s][:, 0][:, 1], dtype=np.float)

        xp = cv2.pow(cv2.subtract(x, cx), 2)
        yp = cv2.pow(cv2.subtract(y, cy), 2)
        dist = cv2.sqrt(cv2.add(xp, yp))

        dist_max_i = np.argmax(dist)

        if dist_max_i < len(s):
            farthest_defect = s[dist_max_i]
            farthest_point = tuple(contour[farthest_defect][0])
            return farthest_point
        else:
            return None


while(True):
    _, frame = camera.read()
    frame = frame[0:0+300,0:0+300]
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    retval, thresh1 = cv2.threshold(frame, cv2.getTrackbarPos("thresh", "test"), 255, cv2.THRESH_BINARY_INV)

    newFrame, contours, h = cv2.findContours(thresh1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    xcoord = 0
    ycoord = 0
    for cnt in contours:
        hull = cv2.convexHull(cnt)

        cnt_centroid = centroid(cnt)
        
        try:
            hull = cv2.convexHull(cnt, returnPoints=False)
            defects = cv2.convexityDefects(cnt, hull)
            far_point = farthest_point(defects, cnt, cnt_centroid)
            cv2.circle(frame, far_point, 5, [0, 255, 255], -1)
            xcoord = far_point[0]
            ycoord = far_point[1]
            if len(defects) is 1 or len(defects) is 2:
                pass
        except TypeError:
            pass

    pushToJS(str(xcoord) + "-"+str(ycoord))
    flippedFrame = frame
    flippedThresh = thresh1

    flippedFrame = cv2.flip(flippedFrame, 1)
    flippedThresh = cv2.flip(flippedThresh, 1)
    cv2.imshow("test", flippedFrame)
    cv2.imshow("mask", flippedThresh)
    if(cv2.waitKey(30) >= 0): break;

sys.exit()
