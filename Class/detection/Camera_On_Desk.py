# 摄像头实时人脸识别
import threading
from datetime import datetime

import dlib
import numpy as np
import cv2
import pandas as pd
import os
import time

import requests

import facenet
from PIL import Image, ImageDraw, ImageFont
from Post import post, post_person

start_time = 0
api_transfer = {'elder': 'old', 'employee': 'employee', 'volunteer': 'volunteer'}


class Interaction_Detection:
    def __init__(self, detector, nn4_small2):
        # 模型
        self.detector = detector
        self.nn4_small2 = nn4_small2
        self.pre = datetime.now()

        # 用来存放所有录入人脸特征的数组
        self.features_known_list = []

        # 存储录入人脸名字
        self.loaded = False
        self.name_known_cnt = 0
        self.name_known_list = []
        self.type_known_list = []
        self.id_known_list = []

        self.metadata = []
        self.embedded = []

        # 存储当前摄像头中捕获到的所有人脸的坐标名字
        self.pos_camera_list = []
        self.name_camera_list = []
        self.type_camera_list = []
        self.id_camera_list = []
        # 存储当前摄像头中捕获到的人脸数
        self.faces_cnt = 0
        # 存储当前摄像头中捕获到的人脸特征
        self.features_camera_list = []

        # Update FPS
        self.fps = 0
        self.frame_start_time = 0

    # 从 "features_all.csv" 读取录入人脸特征
    def get_face_database(self):
        if self.loaded:
            return 1
        else:
            if os.path.exists("data/data_faces_from_camera/"):
                self.metadata = facenet.load_metadata("data/data_faces_from_camera/")
                self.name_known_cnt = 0
                for i in range(0, len(self.metadata)):
                    for j in range(0, len(self.metadata[i])):
                        for k in range(0,len(self.metadata[i][j])):
                            self.name_known_cnt += 1
                print(self.name_known_cnt)
                self.embedded = np.zeros((self.name_known_cnt * 8, 128))

                for i, m in enumerate(self.metadata):
                    for j, n in enumerate(m):
                        for k, p in enumerate(n):
                            img = facenet.load_image(p.image_path().replace("\\", "/"))
                            # img = align_image(img)
                            img = cv2.resize(img, (96, 96))
                            # scale RGB values to interval [0,1]
                            img = (img / 255.).astype(np.float32)
                            # obtain embedding vector for image
                            self.embedded[i] = self.nn4_small2.predict(np.expand_dims(img, axis=0))[0]
                            # self.embedded[i] = self.embedded[i] / len(m)
                            path = p.image_path().replace("\\", "/")
                        self.name_known_list.append(path.split('/')[-2])
                        self.type_known_list.append(path.split('/')[-3])
                for i in range(len(self.name_known_list)):
                    if self.type_known_list[i] == 'elder':
                        type = 'old'
                    elif self.type_known_list[i] == 'volunteer':
                        type = 'employee'
                    self.id_known_list.append(requests.get("http://zhuooyu.cn:8000/api/person/" + str(type) + "/" + str(
                        self.name_known_list[i]) + "/").text)
                self.loaded = True
                return 1
            else:
                print('##### Warning #####', '\n')
                print("'features_all.csv' not found!")
                print(
                    "Please run 'get_faces_from_camera.py' before 'face_reco_from_camera.py'",
                    '\n')
                print('##### End Warning #####')
                return 0

    # 更新 FPS
    def update_fps(self):
        now = time.time()
        self.frame_time = now - self.frame_start_time
        self.fps = 1.0 / self.frame_time
        self.frame_start_time = now

    def draw_note(self, img_rd):
        font = cv2.FONT_ITALIC

        # cv2.putText(img_rd, "Face Recognizer", (20, 40), font, 1, (255, 255, 255), 1, cv2.LINE_AA)
        # cv2.putText(img_rd, "FPS:   " + str(self.fps.__round__(14)), (20, 100), font, 0.8, (0, 255, 0), 1, cv2.LINE_AA)
        cv2.putText(img_rd, "Faces: " + str(self.faces_cnt), (20, 40), font, 0.8, (0, 255, 0), 1, cv2.LINE_AA)
        # cv2.putText(img_rd, "Q: Quit", (20, 450), font, 0.8, (255, 255, 255), 1, cv2.LINE_AA)

    def draw_name(self, img_rd):
        # 在人脸框下面写人脸名字
        img_with_name = img_rd
        font = ImageFont.truetype("simsun.ttc", 30, index=1)
        img = Image.fromarray(cv2.cvtColor(img_rd, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(img)
        for i in range(self.faces_cnt):
            if self.name_camera_list[i] != 'unknown':
                # cv2.putText(img_rd, self.name_camera_list[i], self.pos_camera_list[i], font, 0.8, (0, 255, 255), 1, cv2.LINE_AA)
                draw.text(xy=self.pos_camera_list[i], text=self.name_camera_list[i], font=font)
                img_with_name = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        return img_with_name

    # 修改显示人名
    def modify_name_camera_list(self):
        # TODO 数据库 ID
        # Default known name: 1, 14, person_3
        self.name_known_list[0] = '1'.encode('utf-8').decode()
        self.name_known_list[1] = 'Tony Blair'.encode('utf-8').decode()
        # self.name_known_list[14] = '唐保生'.encode('utf-8').decode()
        # self.name_known_list[3] = '1'.encode('utf-8').decode()
        # self.name_known_list[4] ='xx'.encode('utf-8').decode()

    # 进行人脸识别
    def process(self, img_rd, scale):
        img_with_name = img_rd
        data_type_three = {
            'old': 0,
            'employee': 0,
            'volunteer': 0,
            'stranger': 0
        }
        # 读取所有人脸
        if self.get_face_database():
            self.draw_note(img_rd)
            self.features_camera_list = []
            self.faces_cnt = 0
            self.pos_camera_list = []
            self.name_camera_list = []
            self.type_camera_list = []

            (h, w) = img_rd.shape[:2]
            blob = cv2.dnn.blobFromImage(cv2.resize(img_rd, (300, 300)), 1.0,
                                         (300, 300), (104.0, 177.0, 123.0))
            self.detector.setInput(blob)
            faces = self.detector.forward()

            # 检测到人脸
            if faces.shape[2] != 0:
                # 遍历捕获到的图像中所有的人脸
                for k in range(0, faces.shape[2]):
                    # 计算矩形框大小
                    confidence = faces[0, 0, k, 2]

                    # filter out weak detections by ensuring the `confidence` is
                    # greater than the minimum confidence
                    if confidence < 0.5:
                        continue
                    self.faces_cnt += 1

                    # 让人名跟随在矩形框的上方
                    # 确定人名的位置坐标
                    # 先默认所有人不认识，是 unknown
                    self.name_camera_list.append("unknown")
                    self.type_camera_list.append("unknown")

                    # 每个捕获人脸的名字坐标
                    box = faces[0, 0, k, 3:7] * np.array([w, h, w, h])
                    (startX, startY, endX, endY) = box.astype("int")
                    self.pos_camera_list.append(tuple(
                        [int(startX + 5), int(startY - 30)]))

                    img_blank = img_rd[startY:endY, startX:endX]
                    img_blank = img_blank[..., ::-1]
                    try:
                        # for ii in range(height):
                        #     for jj in range(width):
                        #         img_blank[ii][jj] = img_rd[startY + ii][startX + jj]

                        img = cv2.resize(img_blank, (96, 96))
                        img = (img / 255.).astype(np.float32)
                        img = self.nn4_small2.predict(np.expand_dims(img, axis=0))[0]

                        # 对于某张人脸，遍历所有存储的人脸
                        e_distance_list = []
                        for i in range(0, len(self.embedded)):
                            e_distance_list.append(facenet.distance(self.embedded[i], img))

                        similar_person_num = e_distance_list.index(min(e_distance_list))

                        # print(min(e_distance_list))
                        if min(e_distance_list) < 0.58:
                            self.name_camera_list[k] = self.name_known_list[similar_person_num % 8]
                            self.type_camera_list[k] = self.type_known_list[similar_person_num % 8]
                            data_type_three[api_transfer[self.type_camera_list[k]]] += 1

                        # 绘制矩形框
                        if self.name_camera_list[k] != 'unknown':
                            cv2.rectangle(img_rd, tuple([startX, startY]), tuple([endX, endY]),
                                          (0, 255, 0), 2)
                            cv2.rectangle(img_rd, tuple([startX, startY - 35]), tuple([endX, startY]),
                                          (0, 255, 0), cv2.FILLED)

                    except:
                        continue
                    print(self.type_camera_list)
                    img_with_name = self.draw_name(img_rd)
                    if 'unknown' in self.type_camera_list and len(self.type_camera_list) > 1:
                        index = self.type_camera_list.index('unknown')
                        pos_vol = np.array(self.pos_camera_list[index])
                        for i in range(0, len(self.type_camera_list)):
                            if self.type_camera_list[i] == "elder":
                                d = scale * np.sqrt(facenet.distance(pos_vol, np.array(self.pos_camera_list[i])))
                                if d < 50:
                                    if (datetime.now() - self.pre).total_seconds() > 5:
                                        time_snap = datetime.now()
                                        cv2.imwrite("interaction"+str(time_snap).replace(':','')+".jpg", img_with_name)
                                        t = threading.Thread(target=post(event=1, imagePath='interaction'+str(time_snap).replace(':','')+'.jpg'))
                                        t.setDaemon(False)
                                        t.start()
                                        self.pre = datetime.now()
            else:
                img_with_name = img_rd

            # if 'volunteer' in self.type_camera_list:

            # 更新 FPS / Update stream FPS
            self.update_fps()
            # 距离检测
        if (datetime.now() - self.pre).total_seconds() > 5:
            post_person(data_type_three)
            self.pre = datetime.now()
        return img_with_name

    # OpenCV 调用摄像头并进行 process
    def run(self, frame, scale):
        # cap = cv2.VideoCapture(0)
        # cap.set(3, 480)
        self.process(frame, scale)

        # cap.release()
        # cv2.destroyAllWindows()
