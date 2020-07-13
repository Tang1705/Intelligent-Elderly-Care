import math
import sys
import threading
import time
import cv2
import os
from sys import platform
import argparse
import numpy as np
from Post import post

from PIL import ImageDraw, ImageFont
from PIL import Image

import queue
import frame_process
import algorithm_fall

# Import Openpose (Windows/Ubuntu/OSX)
# dir_path = os.path.dirname(os.path.realpath(__file__))
dir_path = 'D:\\BJTU\\Python\\openpose-master\\build-2017'
try:
    # Windows Import
    if platform == "win32":
        # Change these variables to point to the correct folder (Release/x64 etc.)
        sys.path.append(dir_path + '\\python\\openpose\\Release')
        os.environ['PATH'] = os.environ['PATH'] + ';' + dir_path + '\\x64\\Release;' + dir_path + '\\bin;'
        import pyopenpose as op
    else:
        # Change these variables to point to the correct folder (Release/x64 etc.)
        sys.path.append('../../python')
        # If you run `make install` (default path is `/usr/local/python` for Ubuntu), you can also access the OpenPose/python module from there. This will install OpenPose and the python library at your desired installation path. Ensure that this is in your python path in order to use it.
        # sys.path.append('/usr/local/python')
        from openpose import pyopenpose as op
except ImportError as e:
    print(
        'Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?')
    raise e


class Fall_Detection:
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.args = self.parser.parse_known_args()
        self.params = dict()
        self.params["model_folder"] = "D:\\BJTU\\Python\\openpose-master\\models\\"
        self.params['net_resolution'] = "-1x160"

        for i in range(0, len(self.args[1])):
            curr_item = self.args[1][i]
            if i != len(self.args[1]) - 1:
                next_item = self.args[1][i + 1]
            else:
                next_item = "1"
            if "--" in curr_item and "--" in next_item:
                key = curr_item.replace('-', '')
                if key not in self.params:  self.params[key] = "1"
            elif "--" in curr_item and "--" not in next_item:
                key = curr_item.replace('-', '')
                if key not in self.params: self.params[key] = next_item

        # Starting OpenPose
        self.opWrapper = op.WrapperPython()
        self.opWrapper.configure(self.params)
        self.opWrapper.start()

        # init variables
        self.frame_start_time = 0
        self.v0 = 0
        self.width0 = []
        self.height0 = []
        self.center0 = []
        self.couter = 0
        self.error = 0

        self.xList = queue.Queue(maxsize=10)
        self.yList = queue.Queue(maxsize=10)
        self.prevX = 0.0
        self.prevY = 0.0
        self.centerV = 0
        self.centerSpeed = 0
        self.alert = 0
        self.firstFrame = None

    def re_init(self):
        self.frame_start_time = 0
        self.v0 = 0
        self.width0 = []
        self.height0 = []
        self.center0 = []
        self.couter = 0
        self.error = 0

        self.xList = queue.Queue(maxsize=10)
        self.yList = queue.Queue(maxsize=10)
        self.prevX = 0.0
        self.prevY = 0.0
        self.centerV = 0
        self.centerSpeed = 0
        self.alert = 0
        self.firstFrame = None

    def run(self, frame):
        height = []
        width = []
        center = []

        # Process Image
        datum = op.Datum()
        datum.cvInputData = frame
        self.opWrapper.emplaceAndPop([datum])
        img_rd = datum.cvOutputData

        # fall judge
        try:
            # key points have been identified
            x = datum.poseKeypoints[0][:, 0]
            y = datum.poseKeypoints[0][:, 1]

            width.append(np.max(x[np.nonzero(x)]) - np.min(x[np.nonzero(x)]))
            height.append(np.max(y[np.nonzero(y)]) - np.min(y[np.nonzero(y)]))

            center.append(np.mean(x[np.nonzero(x)]))
            center.append(np.mean(y[np.nonzero(y)]))

            if self.frame_start_time == 0:
                self.center0 = center.copy()
                self.width0 = width.copy()
                self.height0 = height.copy()
                self.frame_start_time = time.time()
            else:
                diff = np.array([center[0] - self.center0[0], center[1] - self.center0[1]])
                dist = math.sqrt(np.sum((diff * 10 ** (-4)) ** 2))
                now = time.time()
                v = dist / (now - self.frame_start_time)
                a = (v ** 2 - self.v0 ** 2) / (2 * dist)

                # print(v, abs(a))
                if (abs(a) > 0.2) and \
                        (np.subtract(np.array(width), np.array(height)) > np.subtract(np.array(self.width0), np.array(
                            self.height0)) and np.subtract(np.array(width), np.array(height)) > 0):
                    self.couter += 1
                    # print("alarm by v and a")
                elif (width > height and (x[8] != 0 or x[9] != 0 or x[12] != 0) and v < 1):
                    self.couter += 1
                    # print("alarm by w and h")
                else:
                    if self.error == 0:
                        self.error += 1
                    else:
                        self.couter = 0
                        self.error = 0

                if self.couter > 3:
                    font = ImageFont.truetype("simsun.ttc", 30, index=1)
                    img_rd = Image.fromarray(cv2.cvtColor(datum.cvOutputData, cv2.COLOR_BGR2RGB))
                    draw = ImageDraw.Draw(img_rd)
                    draw.text((10, 10), text="Fall Detected", font=font,
                              fill=(255, 0, 0))
                    img_rd = cv2.cvtColor(np.array(img_rd), cv2.COLOR_RGB2BGR)
                    cv2.imwrite('fall_detection.jpg', frame)
                    t = threading.Thread(target=post(event=3, imagePath='fall_detection.jpg'))
                    t.setDaemon(False)
                    t.start()
                    # status = post(event=3, imagePath='fall_detection.jpg')
                    # print("fall")

                # update variables
                self.frame_start_time = now
                self.v0 = v
                self.width0 = width.copy()
                self.height0 = height.copy()
            # if width > height:
            #     print("alarm")
            self.firstFrame = None
        except Exception as e:
            gray = frame_process.preprocess_frame(frame)

            if self.firstFrame is None:
                self.firstFrame = gray
                pass

            frameDelta = cv2.absdiff(self.firstFrame, gray)

            cnts = frame_process.get_contours(self.firstFrame, gray)

            defined_min_area = 3000
            frame, self.alert = algorithm_fall.fall_detect(cnts, defined_min_area, frame, self.prevX, self.prevY,
                                                           self.xList, self.yList, self.centerV, self.alert)

            img_rd = frame
            # cv2.imshow("OpenPose 1.6.0 - Tutorial Python API", frame)

        frame = cv2.resize(img_rd, (640, 480))
        # cv2.imshow("OpenPose 1.6.0 - Tutorial Python API", img_rd)
        return frame
# http://zhuooyu.cn:8000/api/person/old/10