# 摄像头实时人脸识别

import dlib
import numpy as np
import cv2
import pandas as pd
import os
import time
from PIL import Image, ImageDraw, ImageFont

# 1. Dlib 正向人脸检测器
# detector = dlib.get_frontal_face_detector()

# OpenCV DNN face detector
detector = cv2.dnn.readNetFromCaffe("data/data_opencv/deploy.prototxt.txt",
                                    "data/data_opencv/res10_300x300_ssd_iter_140000.caffemodel")

# 2. Dlib 人脸 landmark 特征点检测器
predictor = dlib.shape_predictor('data/data_dlib/shape_predictor_68_face_landmarks.dat')

# 3. Dlib Resnet 人脸识别模型，提取 128D 的特征矢量
face_reco_model = dlib.face_recognition_model_v1("data/data_dlib/dlib_face_recognition_resnet_model_v1.dat")


class Face_Recognizer:
    def __init__(self):
        # 用来存放所有录入人脸特征的数组
        self.features_known_list = []

        # 存储录入人脸名字
        self.name_known_cnt = 0
        self.name_known_list = []

        # 存储当前摄像头中捕获到的所有人脸的坐标名字
        self.pos_camera_list = []
        self.name_camera_list = []
        # 存储当前摄像头中捕获到的人脸数
        self.faces_cnt = 0
        # 存储当前摄像头中捕获到的人脸特征
        self.features_camera_list = []

        # Update FPS
        self.fps = 0
        self.frame_start_time = 0

    # 从 "features_all.csv" 读取录入人脸特征
    def get_face_database(self):
        if os.path.exists("data/features_all.csv"):
            path_features_known_csv = "data/features_all.csv"
            csv_rd = pd.read_csv(path_features_known_csv, header=None)
            # 2. 读取已知人脸数据
            for i in range(csv_rd.shape[0]):
                features_someone_arr = []
                for j in range(0, 128):
                    if csv_rd.iloc[i][j] == '':
                        features_someone_arr.append('0')
                    else:
                        features_someone_arr.append(csv_rd.iloc[i][j])
                self.features_known_list.append(features_someone_arr)
                self.name_known_list.append("Person_" + str(i + 1))
            self.name_known_cnt = len(self.name_known_list)
            print("Faces in Database：", len(self.features_known_list))
            return 1
        else:
            print('##### Warning #####', '\n')
            print("'features_all.csv' not found!")
            print(
                "Please run 'get_faces_from_camera.py' and 'features_extraction_to_csv.py' before 'face_reco_from_camera.py'",
                '\n')
            print('##### End Warning #####')
            return 0

    # 计算两个128D向量间的欧式距离
    @staticmethod
    def return_euclidean_distance(feature_1, feature_2):
        feature_1 = np.array(feature_1)
        feature_2 = np.array(feature_2)
        dist = np.sqrt(np.sum(np.square(feature_1 - feature_2)))
        return dist

    # TODO th

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
        font = ImageFont.truetype("simsun.ttc", 30, index=1)
        img = Image.fromarray(cv2.cvtColor(img_rd, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(img)
        for i in range(self.faces_cnt):
            # cv2.putText(img_rd, self.name_camera_list[i], self.pos_camera_list[i], font, 0.8, (0, 255, 255), 1, cv2.LINE_AA)
            draw.text(xy=self.pos_camera_list[i], text=self.name_camera_list[i], font=font)
            img_with_name = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        return img_with_name

    # 修改显示人名
    def modify_name_camera_list(self):
        # TODO 数据库 ID
        # Default known name: person_1, person_2, person_3
        self.name_known_list[0] = '唐麒'.encode('utf-8').decode()
        # self.name_known_list[1] ='李四'.encode('utf-8').decode()
        # self.name_known_list[2] ='xx'.encode('utf-8').decode()
        # self.name_known_list[3] ='xx'.encode('utf-8').decode()
        # self.name_known_list[4] ='xx'.encode('utf-8').decode()

    # 处理获取的视频流，进行人脸识别
    def process(self, stream):
        # 1. 读取存放所有人脸特征的 csv
        if self.get_face_database():
            while stream.isOpened():
                flag, img_rd = stream.read()
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
                        for i in range(0, faces.shape[2]):
                            confidence = faces[0, 0, i, 2]

                            # filter out weak detections by ensuring the `confidence` is
                            # greater than the minimum confidence
                            if confidence < 0.5:
                                continue
                            box = faces[0, 0, i, 3:7] * np.array([w, h, w, h])
                            (startX, startY, endX, endY) = box.astype("int")
                            rect = dlib.rectangle(startX, startY, endX, endY)
                            shape = predictor(img_rd, rect)
                            self.features_camera_list.append(face_reco_model.compute_face_descriptor(img_rd, shape))

                        # 4. 遍历捕获到的图像中所有的人脸
                        for k in range(0, faces.shape[2]):
                            # 计算矩形框大小
                            confidence = faces[0, 0, k, 2]

                            # filter out weak detections by ensuring the `confidence` is
                            # greater than the minimum confidence
                            if confidence < 0.5:
                                continue
                            print("##### camera person", k + 1, "#####")
                            # 让人名跟随在矩形框的上方
                            # 确定人名的位置坐标
                            # 先默认所有人不认识，是 unknown
                            # Set the default names of faces with "unknown"
                            self.name_camera_list.append("unknown")

                            # 每个捕获人脸的名字坐标
                            box = faces[0, 0, k, 3:7] * np.array([w, h, w, h])
                            (startX, startY, endX, endY) = box.astype("int")
                            self.pos_camera_list.append(tuple(
                                [int(startX+5), int(startY - 30)]))

                            # 5. 对于某张人脸，遍历所有存储的人脸特征
                            e_distance_list = []
                            for i in range(len(self.features_known_list)):
                                # 如果 person_X 数据不为空
                                if str(self.features_known_list[i][0]) != '0.0':
                                    print("with person", str(i + 1), "the e distance: ", end='')
                                    e_distance_tmp = self.return_euclidean_distance(self.features_camera_list[k],
                                                                                    self.features_known_list[i])
                                    print(e_distance_tmp)
                                    e_distance_list.append(e_distance_tmp)
                                else:
                                    # 空数据 person_X
                                    e_distance_list.append(999999999)
                            # 6. 寻找出最小的欧式距离匹配
                            similar_person_num = e_distance_list.index(min(e_distance_list))
                            print("Minimum e distance with person", self.name_known_list[similar_person_num])

                            if min(e_distance_list) < 0.4:
                                self.name_camera_list[k] = self.name_known_list[similar_person_num]
                                print("May be person " + str(self.name_known_list[similar_person_num]))
                            else:
                                print("Unknown person")

                            # 矩形框
                            for kk, d in enumerate(faces):
                                # 绘制矩形框
                                cv2.rectangle(img_rd, tuple([startX, startY]), tuple([endX, endY]),
                                              (0, 255, 0), 2)
                                cv2.rectangle(img_rd, tuple([startX, startY - 35]), tuple([endX, startY]),
                                              (0, 255, 0), cv2.FILLED)
                            print('\n')

                        self.faces_cnt = len(faces)
                        # 7. 在这里更改显示的人名
                        self.modify_name_camera_list()
                        # 8. 写名字
                        # self.draw_name(img_rd)
                        img_with_name = self.draw_name(img_rd)
                    else:
                        img_with_name = img_rd

                print("Faces in camera now:", self.name_camera_list, "\n")

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
    Face_Recognizer_con = Face_Recognizer()
    Face_Recognizer_con.run()


if __name__ == '__main__':
    main()
