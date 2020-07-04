# frame.py : gets the frame and preprocesses for background subtraction

import time
import cv2
from imutils.video import VideoStream

def preprocess_frame(frame):
    
    # convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # use gaussian blur to blur frame
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    return gray


def get_contours(firstFrame, gray):
    
    frameDelta = cv2.absdiff(firstFrame, gray)
    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
    
    # dilate the thresholded image to fill in holes, then find contours
    # on thresholded image
    thresh = cv2.dilate(thresh, None, iterations=2)

    # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))  # 定义矩形结构元素
    #
    # thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=1)  # 闭运算1
    
    # contour detection to find the outlines of these white regions
    # filter out the small, irrelevant contours
    major = cv2.__version__.split('.')[0]
    if major == '3':
        _, contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    else:
        contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    return contours


