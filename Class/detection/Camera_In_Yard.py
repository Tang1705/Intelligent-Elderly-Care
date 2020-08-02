import threading
from datetime import datetime

from oldcare.track.centroidtracker import CentroidTracker
from oldcare.track.trackableobject import TrackableObject
from imutils.video import FPS
import numpy as np
from Post import post
import imutils
import argparse
import time
import dlib
import cv2

# 全局变量
# prototxt_file_path = 'data/data_opencv/MobileNetSSD_deploy.prototxt'
# # Contains the Caffe deep learning model files.
# # We’ll be using a MobileNet Single Shot Detector (SSD),
# # “Single Shot Detectors for object detection”.
# model_file_path = 'data/data_opencv/MobileNetSSD_deploy.caffemodel'


# 物体识别模型能识别的物体（21种）
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
           "bottle", "bus", "car", "cat", "chair",
           "cow", "diningtable", "dog", "horse", "motorbike",
           "person", "pottedplant", "sheep", "sofa", "train",
           "tvmonitor"]


# 加载物体识别模型
# net = cv2.dnn.readNetFromCaffe(prototxt_file_path, model_file_path)


class Intrusion_Detection():
    def __init__(self, net):
        self.net = net
        # initialize the frame dimensions (we'll set them as soon as we read
        # the first frame from the video)
        self.W = None
        self.H = None
        self.pre = datetime.now()
        # instantiate our centroid tracker, then initialize a list to store
        # each of our dlib correlation trackers, followed by a dictionary to
        # map each unique object ID to a TrackableObject
        self.ct = CentroidTracker(maxDisappeared=40, maxDistance=50)
        self.trackers = []
        self.trackableObjects = {}

        # initialize the total number of frames processed thus far, along
        # with the total number of objects that have moved either up or down
        self.totalFrames = 0
        self.totalDown = 0
        self.totalUp = 0

        # start the frames per second throughput estimator
        self.fps = FPS().start()

    # loop over frames from the video stream
    def process(self, frame):
        # grab the next frame and handle if we are reading from either
        # VideoCapture or VideoStream

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # if the frame dimensions are empty, set them
        if self.W is None or self.H is None:
            (self.H, self.W) = frame.shape[:2]

        # initialize the current status along with our list of bounding
        # box rectangles returned by either (1) our object detector or
        # (14) the correlation trackers
        status = "Waiting"
        rects = []

        # check to see if we should run a more computationally expensive
        # object detection method to aid our tracker
        if self.totalFrames % 20 == 0:
            # set the status and initialize our new set of object trackers
            status = "Detecting"
            self.trackers = []

            # convert the frame to a blob and pass the blob through the
            # network and obtain the detections
            blob = cv2.dnn.blobFromImage(frame, 0.007843, (self.W, self.H), 127.5)
            self.net.setInput(blob)
            detections = self.net.forward()
            # loop over the detections
            for i in np.arange(0, detections.shape[2]):
                # extract the confidence (i.e., probability) associated
                # with the prediction
                confidence = detections[0, 0, i, 2]

                # filter out weak detections by requiring a minimum
                # confidence
                if confidence > 0.5:

                    # extract the index of the class label from the
                    # detections list
                    idx = int(detections[0, 0, i, 1])

                    # if the class label is not a person, ignore it
                    if CLASSES[idx] != "person":
                        continue

                    # compute the (x, y)-coordinates of the bounding box
                    # for the object
                    box = detections[0, 0, i, 3:7] * np.array([self.W, self.H, self.W, self.H])
                    (startX, startY, endX, endY) = box.astype("int")

                    # construct a dlib rectangle object from the bounding
                    # box coordinates and then start the dlib correlation
                    # tracker
                    tracker = dlib.correlation_tracker()
                    rect = dlib.rectangle(startX, startY, endX, endY)
                    tracker.start_track(rgb, rect)

                    # add the tracker to our list of trackers so we can
                    # utilize it during skip frames
                    self.trackers.append(tracker)
        # otherwise, we should utilize our object *trackers* rather than
        # object *detectors* to obtain a higher frame processing throughput
        else:
            # loop over the trackers
            for tracker in self.trackers:
                # set the status of our system to be 'tracking' rather
                # than 'waiting' or 'detecting'
                status = "Tracking"

                # update the tracker and grab the updated position
                tracker.update(rgb)
                pos = tracker.get_position()

                # unpack the position object
                startX = int(pos.left())
                startY = int(pos.top())
                endX = int(pos.right())
                endY = int(pos.bottom())

                # draw a rectangle around the people
                cv2.rectangle(frame, (startX, startY), (endX, endY),
                              (0, 255, 0), 2)

                # add the bounding box coordinates to the rectangles list
                rects.append((startX, startY, endX, endY))

        # draw a horizontal line in the center of the frame -- once an
        # object crosses this line we will determine whether they were
        # moving 'up' or 'down'
        # cv2.line(frame, (0, H // 14), (W, H // 14), (0, 255, 255), 14)

        # use the centroid tracker to associate the (1) old object
        # centroids with (14) the newly computed object centroids
        objects = self.ct.update(rects)

        # loop over the tracked objects
        for (objectID, centroid) in objects.items():
            # check to see if a trackable object exists for the current
            # object ID
            to = self.trackableObjects.get(objectID, None)

            # if there is no existing trackable object, create one
            if to is None:
                to = TrackableObject(objectID, centroid)

            # otherwise, there is a trackable object so we can utilize it
            # to determine direction
            else:
                # the difference between the y-coordinate of the *current*
                # centroid and the mean of *previous* centroids will tell
                # us in which direction the object is moving (negative for
                # 'up' and positive for 'down')
                y = [c[1] for c in to.centroids]
                direction = centroid[1] - np.mean(y)
                to.centroids.append(centroid)

                # check to see if the object has been counted or not
                if not to.counted:
                    # if the direction is negative (indicating the object
                    # is moving up) AND the centroid is above the center
                    # line, count the object
                    if direction < 0 and centroid[1] < self.H // 2:
                        self.totalUp += 1
                        to.counted = True

                    # if the direction is positive (indicating the object
                    # is moving down) AND the centroid is below the
                    # center line, count the object
                    elif direction > 0 and centroid[1] > self.H // 2:
                        self.totalDown += 1
                        to.counted = True

                        current_time = time.strftime('%Y-%m-%d %H:%M:%S',
                                                     time.localtime(time.time()))
                        event_desc = '有人闯入禁止区域!!!'
                        event_location = '院子'
                        print('[EVENT] %s, 院子, 有人闯入禁止区域!!!'
                              % (current_time))
                        time_snap = datetime.now()
                        cv2.imwrite('intrusion' + str(time_snap).replace(':', '') + '.jpg', frame)
                        if (datetime.now() - self.pre).total_seconds() > 5:
                            t = threading.Thread(
                                target=post(event=4, imagePath='intrusion' + str(time_snap).replace(':', '') + '.jpg'))
                            t.setDaemon(False)
                            t.start()
                            self.pre = datetime.now()

                        # todo insert into database
                        # command = '%s inserting.py --event_desc %s--event_type4 - -event_location % s' % \
                        #           (python_path, event_desc, event_location)
                        # p = subprocess.Popen(command, shell=True)

                # store the trackable obj   ect in our dictionary
            self.trackableObjects[objectID] = to

            # draw both the ID of the object and the centroid of the
            # object on the output frame
            text = "ID {}".format(objectID)
            cv2.putText(frame, text, (centroid[0] - 10, centroid[1] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            cv2.circle(frame, (centroid[0], centroid[1]), 4,
                       (0, 255, 0), -1)

        # construct a tuple of information we will be displaying on the
        # frame
        info = [
            # ("Up", totalUp),
            # ("Down", totalDown),
            ("Status", status),
        ]

        # loop over the info tuples and draw them on our frame
        for (i, (k, v)) in enumerate(info):
            text = "{}: {}".format(k, v)
            cv2.putText(frame, text, (10, self.H - ((i * 20) + 20)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

        # show the output frame
        frame = cv2.resize(frame, (640, 480))

        # increment the total number of frames processed thus far and
        # then update the FPS counter
        self.totalFrames += 1
        return frame
