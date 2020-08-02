import os
import queue
import threading
import time
from numba import cuda
import cv2
import sys
import platform
import subprocess as sp
from sys import platform
from datetime import datetime
from model import create_model
from websocket import create_connection
from Camera_Beside_Com import Face_Register
from Camera_In_Room import Face_Recognizer
from Calibration_On_Desk import Calibration
from Camera_In_Hall import Fall_Detection
from Camera_On_Desk import Interaction_Detection
from Camera_In_Yard import Intrusion_Detection


class Live(object):
    def __init__(self):
        self.cap = cv2.VideoCapture(0)

        # opencv dnn 人脸检测器
        self.detector = cv2.dnn.readNetFromCaffe("data/data_opencv/deploy.prototxt.txt",
                                                 "data/data_opencv/res10_300x300_ssd_iter_140000.caffemodel")

        # facenet model
        self.nn4_small2 = create_model()
        self.nn4_small2.load_weights('weights/nn4.small2.v1.h5')

        # websocket 连接服务器
        self.ws = create_connection("ws://192.144.229.49:8000/api/websocket/cameraLink")

        self.frame_queue = queue.Queue()

        self.rtmpUrl = "rtmp://39.97.124.237:1984/wodelive"
        self.camera_path = "test4.mp4"

        # 人脸搜集
        self.Face_Register_on = Face_Register(people_type=1, id='3')

        # 微笑检测
        self.Face_Recognizer_on = Face_Recognizer(self.detector, self.nn4_small2)

        # 与义工交互 距离标定和颜色标定
        self.scale = -1
        self.Calibration_on = Calibration()
        self.Interaction_on = Interaction_Detection(detector=self.detector, nn4_small2=self.nn4_small2)

        # 摔倒检测
        self.transfer_flag = False
        self.trigger = False
        self.Fall_Detection_on = None

        # 入侵检测
        self.net = cv2.dnn.readNetFromCaffe('data/data_opencv/MobileNetSSD_deploy.prototxt',
                                            'data/data_opencv/MobileNetSSD_deploy.caffemodel')
        self.Intrusion_Detection_on = Intrusion_Detection(self.net)

        # 视频记录
        self.fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
        self.out = cv2.VideoWriter('output.avi', self.fourcc, 20, (640, 480))

        # Get video information
        self.fps = 30  # 设置帧速率
        width = 640  # 宽
        height = 480  # 高

        # ffmpeg command
        self.command = ['ffmpeg',
                        '-y',
                        '-f', 'rawvideo',
                        '-vcodec', 'rawvideo',
                        '-pix_fmt', 'bgr24',
                        '-s', "{}x{}".format(width, height),
                        '-r', str(self.fps),
                        '-i', '-',
                        '-c:v', 'libx264',
                        '-pix_fmt', 'yuv420p',
                        '-preset', 'slow',
                        '-f', 'flv',
                        self.rtmpUrl]
        self.recieve = {"todo": "reboot"}
        # self.recieve = {"todo": "change", 'data': {'fuc': '1'}}

        self.transfer_flag = False
        self.take = False

        # if trigger:
        #     cuda.select_device(0)  # 选择GPU设备
        #     cuda.close()  # 释放GPU资源

    def read_frame(self):
        # 根据不同的操作系统，设定读取哪个摄像头
        if platform == 'Linux':  # 如果是Linux系统
            cap = cv2.VideoCapture(10)  # 绑定编号为10的摄像头
            cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
            cap.set(3, 640)  # 设置摄像头画面的宽
            cap.set(4, 480)  # 设置摄像头画面的高
        elif platform == 'Darwin':  # 如果是苹果的OS X系统
            cap = cv2.VideoCapture(0)  # 绑定编号为0的摄像头
            cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
            cap.set(3, 640)
            cap.set(4, 480)
        else:  # windows系统
            cap = cv2.VideoCapture(0)  # 绑定编号为0的摄像头
            cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
            # cap.set(3, 640)
            # cap.set(4, 480)

        # read webcamera
        counter = 0
        pre = datetime.now()
        while cap.isOpened():
            counter += 1
            if counter <= 10:
                continue
            ret, frame = cap.read()
            if not ret:
                self.cap = cv2.VideoCapture(0)
                ret, frame = self.cap.read()
                self.transfer_flag = False
            # put frame into queue
            now = datetime.now()
            self.frame_queue.put(frame)
            # if self.recieve["todo"] == "change":
            #     if self.recieve["data"]["fuc"] == "1":
            #         # Get video information
            #         self.fps = 5  # 设置帧速率
            #         width = 640  # 宽
            #         height = 480  # 高
            #
            #         # ffmpeg command
            #         self.command = ['ffmpeg',
            #                         '-y',
            #                         '-f', 'rawvideo',
            #                         '-vcodec', 'rawvideo',
            #                         '-pix_fmt', 'bgr24',
            #                         '-s', "{}x{}".format(width, height),
            #                         '-r', str(self.fps),
            #                         '-i', '-',
            #                         '-c:v', 'libx264',
            #                         '-pix_fmt', 'yuv420p',
            #                         '-preset', 'slow',
            #                         '-f', 'flv',
            #                         self.rtmpUrl]
            #
            #         if (now - pre).total_seconds() > 0.14:
            #             self.frame_queue.put(frame)
            #             pre = now
            #     else:
            #         # Get video information
            #         self.fps = 20  # 设置帧速率
            #         width = 640  # 宽
            #         height = 480  # 高
            #
            #         # ffmpeg command
            #         self.command = ['ffmpeg',
            #                         '-y',
            #                         '-f', 'rawvideo',
            #                         '-vcodec', 'rawvideo',
            #                         '-pix_fmt', 'bgr24',
            #                         '-s', "{}x{}".format(width, height),
            #                         '-r', str(self.fps),
            #                         '-i', '-',
            #                         '-c:v', 'libx264',
            #                         '-pix_fmt', 'yuv420p',
            #                         '-preset', 'slow',
            #                         '-f', 'flv',
            #                         self.rtmpUrl]
            #
            #         self.frame_queue.put(frame)
            #         pre = now
            # else:
            #     self.frame_queue.put(frame)
            #     pre = now

    def push_frame(self):
        # 防止多线程时 command 未被设置
        while True:
            if len(self.command) > 0:
                # 管道配置
                p = sp.Popen(self.command, stdin=sp.PIPE)
                break

        while True:
            if not self.frame_queue.empty():
                if self.frame_queue.qsize() > 100:
                    self.frame_queue.queue.clear()
                    continue
                frame = self.frame_queue.get()
                if self.recieve["todo"] == 'reboot':
                    pass
                elif self.recieve["todo"] == 'entering':
                    people_type = self.recieve["data"]["type"]  # 0代表老人,1代表员工,2代表义工
                    id = self.recieve["data"]["id"]
                    self.pretodo = 'entering'
                    if not self.take:
                        self.Face_Register_on = Face_Register(people_type, id)
                        self.take = True
                    frame = self.Face_Register_on.process(frame)
                elif self.recieve["todo"] == 'takePhoto':
                    if self.recieve["data"]["fuc"] == 'shutter':
                        if self.take:
                            frame = self.Face_Register_on.take_photo(frame)
                            self.take = False
                        else:
                            frame = self.Face_Register_on.process(frame)
                    elif self.recieve["data"]["fuc"] == 'standard':
                        self.scale = self.Calibration_on.run(frame)
                        self.recieve = {"todo": "change", 'data': {'fuc': '2'}}
                elif self.recieve["todo"] == 'change':
                    fuc = self.recieve["data"]["fuc"]  # 更改的功能 0:无 1微笑检测 2交互检测 3摔倒检测 4禁区入侵
                    if fuc == '0':
                        self.out.write(frame)
                    elif fuc == '1':
                        frame = self.Face_Recognizer_on.process(frame)
                    elif fuc == '14':
                        if self.scale == -1:
                            pass
                        else:
                            frame = self.Interaction_on.process(frame, self.scale)
                    elif fuc == '3' and self.trigger:
                        if not self.transfer_flag:
                            self.cap = cv2.VideoCapture("test4.mp4")
                            ret, frame = self.cap.read()
                            self.transfer_flag = True
                            self.Fall_Detection_on = Fall_Detection()
                            # self.Fall_Detection_on.re_init()
                        frame = self.Fall_Detection_on.run(frame)
                    elif fuc == '4':
                        frame = self.Intrusion_Detection_on.process(frame)
                p.stdin.write(frame.tobytes())

    def get_result(self):
        self.ws.send("Hello, World")
        while True:
            recieve = self.ws.recv()
            print(eval(recieve))
            self.recieve = eval(recieve)
            if self.recieve['todo'] == 'takePhoto' and self.recieve['data']['fuc'] == 'shutter':
                self.take = True

    def release_gpu(self):
        cuda.select_device(0)  # 选择GPU设备
        cuda.close()  # 释放GPU资源

    def run(self):
        threads = [
            threading.Thread(target=Live.read_frame, args=(self,)),
            threading.Thread(target=Live.push_frame, args=(self,)),
            threading.Thread(target=Live.get_result, args=(self,))
        ]
        [thread.setDaemon(False) for thread in threads]
        [thread.start() for thread in threads]


if __name__ == "__main__":
    live = Live()
    live.run()