from sklearn.externals import joblib

import ML_ways_sklearn

import dlib
import numpy as np
import cv2


detector = dlib.get_frontal_face_detector()
# OpenCV DNN face detector
# detector = cv2.dnn.readNetFromCaffe("data/data_opencv/deploy.prototxt.txt",
#                                     "data/data_opencv/res10_300x300_ssd_iter_140000.caffemodel")
predictor = dlib.shape_predictor('data/data_dlib_model/shape_predictor_68_face_landmarks.dat')

# OpenCV 调用摄像头
cap = cv2.VideoCapture(0)

# 设置视频参数
cap.set(3, 480)


def get_features(img_rd):

    # 输入:  img_rd:      图像文件
    # 输出:  positions_lip_arr:  feature point 49 to feature point 68, 20 feature points / 40D in all

    # 取灰度
    img_gray = cv2.cvtColor(img_rd, cv2.COLOR_RGB2GRAY)

    # 计算68点坐标
    positions_68_arr = []
    faces = detector(img_gray, 0)
    landmarks = np.matrix([[p.x, p.y] for p in predictor(img_rd, faces[0]).parts()])

    for idx, point in enumerate(landmarks):
        # 68点的坐标
        pos = (point[0, 0], point[0, 1])
        positions_68_arr.append(pos)

    positions_lip_arr = []
    # 将点 49-68 写入 CSV
    # 即 positions_68_arr[48]-positions_68_arr[67]
    for i in range(48, 68):
        positions_lip_arr.append(positions_68_arr[i][0])
        positions_lip_arr.append(positions_68_arr[i][1])

    return positions_lip_arr


while cap.isOpened():
    # 480 height * 640 width
    flag, img_rd = cap.read()
    kk = cv2.waitKey(1)

    img_gray = cv2.cvtColor(img_rd, cv2.COLOR_RGB2GRAY)

    # 人脸数 faces
    faces = detector(img_gray, 0)
    # 检测到人脸
    if len(faces) != 0:
        # 提取单张40维度特征
        positions_lip_test = get_features(img_rd)

        # path of models
        path_models = "data/data_models/"

        # #########  LR  ###########
        LR = joblib.load(path_models+"model_LR.m")
        ss_LR = ML_ways_sklearn.model_LR()
        X_test_LR = ss_LR.transform([positions_lip_test])
        y_predict_LR = str(LR.predict(X_test_LR)[0]).replace('0', "no smile").replace('1', "with smile")
        print("LR:", y_predict_LR)

        # #########  LSVC  ###########
        LSVC = joblib.load(path_models+"model_LSVC.m")
        ss_LSVC = ML_ways_sklearn.model_LSVC()
        X_test_LSVC = ss_LSVC.transform([positions_lip_test])
        y_predict_LSVC = str(LSVC.predict(X_test_LSVC)[0]).replace('0', "no smile").replace('1', "with smile")
        print("LSVC:", y_predict_LSVC)

        # #########  MLPC  ###########
        MLPC = joblib.load(path_models+"model_MLPC.m")
        ss_MLPC = ML_ways_sklearn.model_MLPC()
        X_test_MLPC = ss_MLPC.transform([positions_lip_test])
        y_predict_MLPC = str(MLPC.predict(X_test_MLPC)[0]).replace('0', "no smile").replace('1', "with smile")
        print("MLPC:", y_predict_MLPC)

        # #########  SGDC  ###########
        SGDC = joblib.load(path_models+"model_SGDC.m")
        ss_SGDC = ML_ways_sklearn.model_SGDC()
        X_test_SGDC = ss_SGDC.transform([positions_lip_test])
        y_predict_SGDC = str(SGDC.predict(X_test_SGDC)[0]).replace('0', "no smile").replace('1', "with smile")
        print("SGDC:", y_predict_SGDC)

        print('\n')

        # 按下 'q' 键退出
        if kk == ord('q'):
            break

    # 窗口显示
    # cv2.namedWindow("camera", 0) # 如果需要摄像头窗口大小可调
    cv2.imshow("camera", img_rd)

# 释放摄像头
cap.release()

# 删除建立的窗口
cv2.destroyAllWindows()