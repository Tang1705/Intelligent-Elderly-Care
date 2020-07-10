# 摄像头实时人脸识别
import threading

import dlib
import numpy as np
import cv2
import pandas as pd
import os
import time
import facenet
from PIL import Image, ImageDraw, ImageFont

from Post import post
from model import create_model

import smile_detection

start_time = 0
# 1. Dlib 正向人脸检测器
# detector = dlib.get_frontal_face_detector()

# OpenCV DNN face detector
detector = cv2.dnn.readNetFromCaffe("data/data_opencv/deploy.prototxt.txt",
                                    "data/data_opencv/res10_300x300_ssd_iter_140000.caffemodel")

# 2. Dlib 人脸 landmark 特征点检测器
# predictor = dlib.shape_predictor('data/data_dlib/shape_predictor_68_face_landmarks.dat')

# 3. Dlib Resnet 人脸识别模型，提取 128D 的特征矢量
# face_reco_model = dlib.face_recognition_model_v1("data/data_dlib/dlib_face_recognition_resnet_model_v1.dat")

nn4_small2_pretrained = create_model()
nn4_small2_pretrained.load_weights('weights/nn4.small2.v1.h5')


class Face_Recognizer:
    def __init__(self):
        # 用来存放所有录入人脸特征的数组
        self.features_known_list = []

        # 存储录入人脸名字
        self.loaded = False
        self.name_known_cnt = 0
        self.name_known_list = []

        self.metadata = []
        self.embedded = []

        # 存储当前摄像头中捕获到的所有人脸的坐标名字
        self.pos_camera_list = []
        self.name_camera_list = []
        self.type_camera_list = []
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
                self.name_known_cnt = self.metadata.shape[0]
                self.embedded = np.zeros((self.metadata.shape[0], 128))

                for i, m in enumerate(self.metadata):
                    for j, n in enumerate(m):
                        for k, p in enumerate(n):
                            img = facenet.load_image(p.image_path())
                            # img = align_image(img)
                            img = cv2.resize(img, (96, 96))
                            # scale RGB values to interval [0,1]
                            img = (img / 255.).astype(np.float32)
                            # obtain embedding vector for image
                            self.embedded[i] = nn4_small2_pretrained.predict(np.expand_dims(img, axis=0))[0]
                        # self.embedded[i] = self.embedded[i] / len(m)
                        path = p.image_path().replace("\\", "/")
                        self.name_known_list.append(path.split('/')[-2])
                        self.type_camera_list.append(path.split('/')[-3])
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

    # 计算两个128D向量间的欧式距离
    # @staticmethod
    # def return_euclidean_distance(feature_1, feature_2):
    #     feature_1 = np.array(feature_1)
    #     feature_2 = np.array(feature_2)
    #     dist = np.sqrt(np.sum((feature_1 - feature_2) ** 2))
    #     return dist

    # 更新 FPS
    def update_fps(self):
        now = time.time()
        self.frame_time = now - self.frame_start_time
        self.fps = 1.0 / self.frame_time
        self.frame_start_time = now

    def draw_note(self, img_rd):
        font = cv2.FONT_ITALIC

        cv2.putText(img_rd, "Face Recognizer", (20, 40), font, 1, (255, 255, 255), 1, cv2.LINE_AA)
        cv2.putText(img_rd, "FPS:   " + str(self.fps.__round__(2)), (20, 100), font, 0.8, (0, 255, 0), 1, cv2.LINE_AA)
        cv2.putText(img_rd, "Faces: " + str(self.faces_cnt), (20, 140), font, 0.8, (0, 255, 0), 1, cv2.LINE_AA)
        cv2.putText(img_rd, "Q: Quit", (20, 450), font, 0.8, (255, 255, 255), 1, cv2.LINE_AA)

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
        # Default known name: 1, 2, person_3
        self.name_known_list[0] = '1'.encode('utf-8').decode()
        self.name_known_list[1] = 'Tony Blair'.encode('utf-8').decode()
        # self.name_known_list[2] = '唐保生'.encode('utf-8').decode()
        # self.name_known_list[3] = '1'.encode('utf-8').decode()
        # self.name_known_list[4] ='xx'.encode('utf-8').decode()

    # 处理获取的视频流，进行人脸识别
    def process(self, stream):
        # 1. 读取存放所有人脸特征的 csv
        if self.get_face_database():
            while stream.isOpened():
                flag, img_rd = stream.read()
                img_with_name = img_rd
                kk = cv2.waitKey(1)
                # 按下 q 键退出
                if kk == ord('q'):
                    break
                else:
                    self.draw_note(img_rd)
                    self.features_camera_list = []
                    self.faces_cnt = 0
                    self.pos_camera_list = []
                    self.name_camera_list = []

                    (h, w) = img_rd.shape[:2]
                    blob = cv2.dnn.blobFromImage(cv2.resize(img_rd, (300, 300)), 1.0,
                                                 (300, 300), (104.0, 177.0, 123.0))
                    detector.setInput(blob)
                    faces = detector.forward()

                    # 2. 检测到人脸
                    if faces.shape[2] != 0:
                        # 3. 获取当前捕获到的图像的所有人脸的特征，存储到 self.features_camera_list
                        # for i in range(0, faces.shape[2]):
                        #     confidence = faces[0, 0, i, 2]
                        #
                        #     # filter out weak detections by ensuring the `confidence` is
                        #     # greater than the minimum confidence
                        #     if confidence < 0.5:
                        #         continue
                        #     box = faces[0, 0, i, 3:7] * np.array([w, h, w, h])
                        #     (startX, startY, endX, endY) = box.astype("int")
                        #     rect = dlib.rectangle(startX, startY, endX, endY)
                        #     shape = predictor(img_rd, rect)
                        #     self.features_camera_list.append(face_reco_model.compute_face_descriptor(img_rd, shape))

                        # 4. 遍历捕获到的图像中所有的人脸
                        for k in range(0, faces.shape[2]):
                            # 计算矩形框大小
                            confidence = faces[0, 0, k, 2]

                            # filter out weak detections by ensuring the `confidence` is
                            # greater than the minimum confidence
                            if confidence < 0.5:
                                continue
                            self.faces_cnt += 1
                            # print("##### camera person", k + 1, "#####")
                            # 让人名跟随在矩形框的上方
                            # 确定人名的位置坐标
                            # 先默认所有人不认识，是 unknown
                            # Set the default names of faces with "unknown"
                            self.name_camera_list.append("unknown")

                            # 每个捕获人脸的名字坐标
                            box = faces[0, 0, k, 3:7] * np.array([w, h, w, h])
                            (startX, startY, endX, endY) = box.astype("int")
                            self.pos_camera_list.append(tuple(
                                [int(startX + 5), int(startY - 30)]))

                            # height = (endY - startY)
                            # width = (endX - startX)

                            # img_blank = np.zeros((height, width, 3), np.uint8)
                            img_blank = img_rd[startY:endY, startX:endX]
                            try:
                                # for ii in range(height):
                                #     for jj in range(width):
                                #         img_blank[ii][jj] = img_rd[startY + ii][startX + jj]

                                img = cv2.resize(img_blank, (96, 96))
                                img = (img / 255.).astype(np.float32)
                                img = nn4_small2_pretrained.predict(np.expand_dims(img, axis=0))[0]

                                # 5. 对于某张人脸，遍历所有存储的人脸特征
                                e_distance_list = []
                                for i in range(0, len(self.embedded)):
                                    e_distance_list.append(facenet.distance(self.embedded[i], img))
                                # for i in range(len(self.features_known_list)):
                                #     # 如果 person_X 数据不为空
                                #     if str(self.features_known_list[i][0]) != '0.0':
                                #         # print("with person", str(i + 1), "the e distance: ", end='')
                                #         e_distance_tmp = self.return_euclidean_distance(self.features_camera_list[k],
                                #                                                         self.features_known_list[i])
                                #         # print(e_distance_tmp)
                                #         e_distance_list.append(e_distance_tmp)
                                #     else:
                                #         # 空数据 person_X
                                #         e_distance_list.append(999999999)
                                # # 6. 寻找出最小的欧式距离匹配
                                similar_person_num = e_distance_list.index(min(e_distance_list))
                                # print("Minimum e distance with person", self.name_known_list[similar_person_num])
                                # print(min(e_distance_list))
                                if min(e_distance_list) < 0.58:
                                    self.name_camera_list[k] = self.name_known_list[similar_person_num % 8]
                                    if self.type_camera_list[similar_person_num % 8] == 'elder':
                                        mode = smile_detection.smile_detect(img_blank)
                                        if mode == 'happy':
                                            cv2.imwrite('smile_detection.jpg', img_rd)
                                            cv2.rectangle(img_rd, tuple([startX, startY - 70]),
                                                          tuple([endX, startY - 35]),
                                                          (0, 215, 255), cv2.FILLED)
                                            cv2.putText(img_rd, 'happy', (startX + 5, startY - 45), cv2.FONT_ITALIC, 1,
                                                        (255, 255, 255), 1, cv2.LINE_AA)
                                            # t = threading.Thread(target=post(elder_id=self.name_camera_list[k], event=0,
                                            #                                  imagePath='smile_detection.jpg'))
                                            # t.start()
                                    # print("May be person " + str(self.name_known_list[similar_person_num]))
                                elif min(e_distance_list) > 0.75:
                                    self.name_camera_list[k] = '陌生人'
                                    cv2.imwrite('stranger_detection.jpg', img_rd)
                                    # t = threading.Thread(target=post(event=2, imagePath='stranger_detection.jpg'))
                                    # t.start()
                                else:
                                    pass
                                    # print("Unknown person")

                                # 矩形框
                                for kk, d in enumerate(faces):
                                    # 绘制矩形框
                                    if self.name_camera_list[k] == '陌生人':
                                        cv2.rectangle(img_rd, tuple([startX, startY]), tuple([endX, endY]),
                                                      (0, 0, 255), 2)
                                        cv2.rectangle(img_rd, tuple([startX, startY - 35]), tuple([endX, startY]),
                                                      (0, 0, 255), cv2.FILLED)
                                    elif self.name_camera_list[k] != 'unknown':
                                        cv2.rectangle(img_rd, tuple([startX, startY]), tuple([endX, endY]),
                                                      (0, 255, 0), 2)
                                        cv2.rectangle(img_rd, tuple([startX, startY - 35]), tuple([endX, startY]),
                                                      (0, 255, 0), cv2.FILLED)

                            except:
                                continue
                            # print('\n')
                            # self.faces_cnt = faces.shape[2]
                            # if len(self.name_camera_list) > 0:
                            # 7. 在这里更改显示的人名
                            # self.modify_name_camera_list()
                            # 8. 写名字
                            # self.draw_name(img_rd)
                            img_with_name = self.draw_name(img_rd)
                    else:
                        img_with_name = img_rd

                # print("Faces in camera now:", self.name_camera_list, "\n")

                if len(img_with_name):
                    cv2.imshow("camera", img_with_name)

                # 9. 更新 FPS / Update stream FPS
                self.update_fps()

    # OpenCV 调用摄像头并进行 process
    def run(self):
        cap = cv2.VideoCapture(0)
        cap.set(3, 480)
        self.process(cap)

        cap.release()
        cv2.destroyAllWindows()


def main():
    # Calibration_on = Calibration()
    # scale = Calibration_on.run()
    # print(scale)

    Face_Recognizer_con = Face_Recognizer()
    Face_Recognizer_con.run()


if __name__ == '__main__':
    main()
