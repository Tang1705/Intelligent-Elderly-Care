# # From Python
# # It requires OpenCV installed for Python
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

from imutils.video import VideoStream
import datetime
import imutils
import queue
import frame_process
import algorithm_fall

pre = datetime.datetime.now()
try:
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

    # cap = cv2.VideoCapture(0)
    cap = cv2.VideoCapture("test4.mp4")

    _, frame = cap.read()
    # frame = cv2.resize(frame, (640, 480))
    # cv2.imwrite('fall_detection.jpg', frame)

    # Flags
    parser = argparse.ArgumentParser()
    # parser.add_argument("--image_path",
    #                     default="fall_detection.jpg",
    #                     help="Process an image. Read all standard formats (jpg, png, bmp, etc.).")
    args = parser.parse_known_args()

    # Custom Params (refer to include/openpose/flags.hpp for more parameters)
    params = dict()
    params["model_folder"] = "D:\\BJTU\\Python\\openpose-master\\models\\"
    params['net_resolution'] = "-1x160"

    # Add others in path?
    for i in range(0, len(args[1])):
        curr_item = args[1][i]
        if i != len(args[1]) - 1:
            next_item = args[1][i + 1]
        else:
            next_item = "1"
        if "--" in curr_item and "--" in next_item:
            key = curr_item.replace('-', '')
            if key not in params:  params[key] = "1"
        elif "--" in curr_item and "--" not in next_item:
            key = curr_item.replace('-', '')
            if key not in params: params[key] = next_item

    # Starting OpenPose
    opWrapper = op.WrapperPython()
    opWrapper.configure(params)
    opWrapper.start()

    # init variables
    frame_start_time = 0
    v0 = 0
    width0 = []
    height0 = []
    center0 = []
    couter = 0
    error = 0

    xList = queue.Queue(maxsize=10)
    yList = queue.Queue(maxsize=10)
    prevX = 0.0
    prevY = 0.0
    centerV = 0
    centerSpeed = 0
    alert = 0
    firstFrame = None

    # Construct it from system arguments
    # op.init_argv(args[1])
    # oppython = op.OpenposePython()
    while cap.isOpened():
        flag, frame = cap.read()
        kk = cv2.waitKey(1)
        # 按下 q 键退出
        if kk == ord('q'):
            break
        else:
            # cv2.imwrite('fall_detection.jpg', frame)
            height = []
            width = []
            center = []

            # Process Image
            datum = op.Datum()
            # imageToProcess = cv2.imread(args[0].image_path)
            datum.cvInputData = frame
            # datum.cvInputData = imageToProcess
            opWrapper.emplaceAndPop([datum])
            img_rd = datum.cvOutputData

            # Display Image
            # print("Body keypoints: \n" + str(datum.poseKeypoints))

            # fall judge
            try:
                # key points have been identified
                x = datum.poseKeypoints[0][:, 0]
                y = datum.poseKeypoints[0][:, 1]

                width.append(np.max(x[np.nonzero(x)]) - np.min(x[np.nonzero(x)]))
                height.append(np.max(y[np.nonzero(y)]) - np.min(y[np.nonzero(y)]))

                center.append(np.mean(x[np.nonzero(x)]))
                center.append(np.mean(y[np.nonzero(y)]))

                if frame_start_time == 0:
                    center0 = center.copy()
                    width0 = width.copy()
                    height0 = height.copy()
                    frame_start_time = time.time()
                else:
                    diff = np.array([center[0] - center0[0], center[1] - center0[1]])
                    dist = math.sqrt(np.sum((diff * 10 ** (-4)) ** 2))
                    now = time.time()
                    v = dist / (now - frame_start_time)
                    a = (v ** 2 - v0 ** 2) / (2 * dist)

                    # print(v, abs(a))
                    if (abs(a) > 0.2) and \
                            (np.subtract(np.array(width), np.array(height)) > np.subtract(np.array(width0),
                                                                                          np.array(
                                                                                              height0)) and np.subtract(
                                np.array(width), np.array(height)) > 0):
                        couter += 1
                        # print(np.subtract(np.array(width), np.array(height)))
                        # print("alarm by v and a")
                    elif (width > height and (x[8] != 0 or x[9] != 0 or x[12] != 0) and v < 1):
                        couter += 1
                        # print("alarm by w and h")
                    else:
                        if error == 0:
                            error += 1
                        else:
                            couter = 0
                            error = 0

                    if couter > 3:
                        font = ImageFont.truetype("simsun.ttc", 30, index=1)
                        img_rd = Image.fromarray(cv2.cvtColor(datum.cvOutputData, cv2.COLOR_BGR2RGB))
                        draw = ImageDraw.Draw(img_rd)
                        draw.text((10, 10), text="Fall Detected", font=font,
                                  fill=(255, 0, 0))
                        img_rd = cv2.cvtColor(np.array(img_rd), cv2.COLOR_RGB2BGR)
                        time_snap = datetime.datetime.now()
                        cv2.imwrite('fall_detection' + str(time_snap).replace(':','') + '.jpg', frame)
                        if (datetime.datetime.now() - pre).total_seconds() > 5:
                            t = threading.Thread(
                                target=post(event=3, imagePath='fall_detection' + str(time_snap).replace(':','') + '.jpg'))
                            t.start()
                            # status = post(event=3, imagePath='fall_detection.jpg')
                            # print("fall")
                            pre = datetime.datetime.now()
                            # print(pre)

                    # update variables
                    frame_start_time = now
                    v0 = v
                    width0 = width.copy()
                    height0 = height.copy()
                # if width > height:
                #     print("alarm")
                firstFrame = None
            except Exception as e:

                text = ""

                gray = frame_process.preprocess_frame(frame)

                if firstFrame is None:
                    firstFrame = gray
                    continue

                frameDelta = cv2.absdiff(firstFrame, gray)

                cnts = frame_process.get_contours(firstFrame, gray)

                defined_min_area = 3000
                frame, alert, pre = algorithm_fall.fall_detect(cnts, defined_min_area, frame, prevX, prevY, xList,
                                                               yList,
                                                               centerV, alert, pre)

                # cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                #             (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (255, 255, 255), 1)
                # cv2.imshow("Frame Delta", frameDelta)
                img_rd = cv2.resize(frame, (640, 480))
                cv2.imshow("OpenPose 1.6.0 - Tutorial Python API", img_rd)
                continue
            img_rd = cv2.resize(img_rd, (640, 480))
            # cv2.resizeWindow("OpenPose 1.6.0 - Tutorial Python API", 640, 480)
            cv2.imshow("OpenPose 1.6.0 - Tutorial Python API", img_rd)
    cap.release()
    cv2.destroyAllWindows()
except Exception as e:
    print(e)
