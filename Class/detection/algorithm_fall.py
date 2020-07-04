from imutils.video import VideoStream
import imutils
import time
import cv2
import numpy as np
import statistics
import queue
import math

        
def fall_detect(cnts, defined_min_area, frame, prevX, prevY, xList, yList, centerV, alert):

    for c in cnts:
        #exclusion
        if cv2.contourArea(c) < defined_min_area:
            continue
        
        # outer bounding box
        (x_b, y_b, w_b, h_b) = cv2.boundingRect(c)
        cv2.rectangle(frame, (x_b, y_b), (x_b + w_b, y_b + h_b), (0, 255, 255), 2) # 黄色矩形

        #rotating bounding box
        rect = cv2.minAreaRect(c) # 得到最小外接矩形的（中心(x,y), (宽,高), 旋转角度）
        box = cv2.boxPoints(rect) # 获取最小外接矩形的4个顶点坐标
        box = np.int0(box)
        cv2.drawContours(frame,[box],0,(0,0,255),2)

        #averaging line
        rows,cols = frame.shape[:2]
        [vx,vy,x,y] = cv2.fitLine(c, cv2.DIST_L2, 0, 0.01, 0.01)
        lefty = (-x * vy/vx) + y
        righty =((cols-x) * vy/vx)+y
        cv2.line(frame,(cols-1,righty),(0,lefty),(255,0,0),2)

        #ellipse
        elps = cv2.fitEllipse(c)
        (x, y), (MA, ma), angle = cv2.fitEllipse(c)
        cv2.ellipse(frame, elps,(255,0,0),3) #red

        #Aspect Ratio
        AR = MA/ma 

        #Center Speed - acceleration
        prevX = 0.0
        prevY = 0.0
        centerSpeed =0
        if xList.full():
            prevX = statistics.median(list(xList.queue))
            prevY = statistics.median(list(yList.queue))
            xList.get()
            yList.get()

        xList.put(elps[0][0])
        yList.put(elps[0][1])
        X = statistics.median(list(xList.queue))
        Y = statistics.median(list(yList.queue))
        
        if xList.full():
            dx = abs(prevX-X)
            dy = abs(prevY-Y)
            centerV = math.sqrt(dx**2+dy**2)
                
        # calculate probabilities for the 4 features
        pAngle = (abs(angle-90)-50)/10
        pAngle = 1 / (math.exp(pAngle)+1)
        
        pAR = 10*AR - 5
        pAR = 1 / (math.exp(pAR) + 1)
        
        ACS = centerV - 9
        ACS = 1 / (math.exp(ACS) + 1)

        # print("pAngle : ", pAngle)
        # print("pAR : ", pAR)
        # print("ACS : ", ACS)
        
        #confidence
        P_FALL = pAngle * pAR * ACS + 0.5
        # print("P_FALL1 : ", P_FALL)
        
        P_FALL = 1/ (math.exp(-(P_FALL-0.65)*10)+1)
        # print("P_FALL2: ", P_FALL)

        #status display
        cv2.putText(frame, "Status : ", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        cv2.putText(frame, "Fall Confidence: {0:.2f} ".format(P_FALL), (10,50),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 128, 255), 2)
        # cv2.putText(frame, "Angle: {0:.2f}".format(angle), (10, 220),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
        # cv2.putText(frame, "AR: {0:.2f}".format(AR), (10, 237),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
        # cv2.putText(frame, "Center Speed: {0:.2f}".format(centerV), (10, 256),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

        #fall
        if P_FALL > 0.88:
            if alert >= 8:
                print("fall")
                cv2.putText(frame, " Fall Detected", (82, 20),cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
                # cv2.imwrite("report.jpg", frame)
                # send_alert.SendMail("report.jpg")
                alert = alert + 1
            else:
                alert = alert + 1

    return alert
