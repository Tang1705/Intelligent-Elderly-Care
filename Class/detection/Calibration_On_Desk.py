import math
import time

import cv2
import numpy as np

from auto_whiteBalance import aug

from GFmatrix import GF

np.seterr(invalid='ignore')


# config = {'morning': [80, 220, 125, 125]}


class Calibration:
    def __init__(self):
        self.font = cv2.FONT_ITALIC

        self.flag = np.zeros((1024, 1280))
        self.nx = [-1, -1, -1, 0, 0, 1, 1, 1]
        self.ny = [1, 0, -1, 1, -1, 1, 0, -1]

        self.frame_time = 0
        self.frame_start_time = 0
        self.fps = 0

        self.scale = 1

    # 获取处理之后 stream 的帧数
    def update_fps(self):
        now = time.time()
        self.frame_time = now - self.frame_start_time
        if self.frame_time != 0:
            self.fps = 1.0 / self.frame_time
            self.frame_start_time = now

    # 生成的 cv2 window 上面添加说明文字
    def draw_note(self, img_rd):
        # 添加说明
        cv2.putText(img_rd, "Calibration", (20, 40), self.font, 1, (255, 255, 255), 1, cv2.LINE_AA)
        cv2.putText(img_rd, "FPS:   " + str(self.fps.__round__(2)), (20, 100), self.font, 0.8, (0, 255, 0), 1,
                    cv2.LINE_AA)

        cv2.putText(img_rd, "S: Calibrate Current Frame", (20, 400), self.font, 0.8, (255, 255, 255), 1, cv2.LINE_AA)
        cv2.putText(img_rd, "Q: Quit", (20, 450), self.font, 0.8, (255, 255, 255), 1, cv2.LINE_AA)

    """
    get_candidate_points:
    将RGB图像转为单通道
    计算每一个像素点横向和纵向的单通道色彩强度差，选择值最大的通道为该像素点的差值，将差值大于选定阈值的点视为候选点
    在选定的窗口大小中进行计算，减少处理数据的数量
    返回存有候选点数据的矩阵
    -1为候选点
    -3为非候选点
    """

    def get_candidate_points(self, frame):
        candidate = np.zeros((frame.shape[0], frame.shape[1]))  # 初始化图像点位置矩阵为0
        b, g, r = cv2.split(frame)
        i = int(frame.shape[0] / 2)
        while i < int(7 * frame.shape[0] / 8):
            j = 0
            while j < int(frame.shape[1] / 2):
                sum = [0, 0, 0]  # 存储r,g,b三个通道的差值结果
                tempxy = [0, 0, 0, 0, 0, 0]  # 存储三个通道纵向和横向的临时求和结果
                k = -6
                while k < 7:  # 十字掩码长度选择为菱形对角线长度的一半
                    tempxy[0] = tempxy[0] + b[i + k][j]  # b通道水平方向
                    tempxy[1] = tempxy[1] + b[i][j + k]  # b通道铅直方向
                    tempxy[2] = tempxy[2] + g[i + k][j]  # g通道水平方向
                    tempxy[3] = tempxy[3] + g[i][j + k]  # g通道铅直方向
                    tempxy[4] = tempxy[4] + r[i + k][j]  # r通道水平方向
                    tempxy[5] = tempxy[5] + r[i][j + k]  # r通道铅直方向
                    k = k + 1
                sum[0] = sum[0] + abs(tempxy[0] - tempxy[1])  # r通道差值
                sum[1] = sum[1] + abs(tempxy[2] - tempxy[3])  # g通道差值
                sum[2] = sum[2] + abs(tempxy[4] - tempxy[5])  # b通道差值
                d = max(sum[0], sum[1], sum[2])  # 选择差值最大的通道
                # print(d)
                if d > 1300:  # tq和zyy人工学习调参选阈值，阈值增大，候选点集中于球体中央
                    candidate[i][j] = -1  # -1标记为候选点
                    # point_size = 1
                    # point_color = (0, 0, 255)
                    # thickness = 0  # 可以为 0 、4、8
                    #
                    # cv2.circle(frame, (j,i), point_size, point_color, thickness)
                else:
                    candidate[i][j] = -3  # -3标记为非候选点
                j = j + 1
            i = i + 1
        # cv2.imshow('1', frame)
        # cv2.waitKey(0)  # 按0退出
        return candidate

    """
    get_grid_points:
    将RGB图像转为灰度图像
    根据真正的角点具有严格的中心对称性，将相关系数大于选定阈值的点选做特征点
    并根据P1和P2类型点的特征（左右或上下为模式元素）将特征点分类为两类特征点
    白色背景的灰度值高于颜色元素的灰度值
    圆邻域采用SUSAN角点检测法的圆邻域，直径为7
    1为角点
    2为非角点
    """

    def get_grid_points(self, frame, candidate):
        GrayImage = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        gridpoints = np.zeros((frame.shape[0], frame.shape[1]))
        size = 7
        counter = 0
        circle_neighborhood = np.zeros((size, size))
        for i in range(0, size):
            for j in range(0, size):
                if i < (size - 1) / 2:
                    if j >= (size - 1) / 2 - i - (size - 3) / 4 and j <= (size - 1) / 2 + i + + (size - 3) / 4:
                        counter += 1
                        circle_neighborhood[i][j] = 1
                elif i >= (size + 5) / 4 and i <= (3 * size - 5) / 4:
                    counter += 1
                    circle_neighborhood[i][j] = 1
                else:
                    if j >= (size - 1) / 2 - (size - 1 - i) - (size - 3) / 4 and j <= (size - 1) / 2 + (
                            size - 1 - i) + (
                            size - 3) / 4:
                        counter += 1
                        circle_neighborhood[i][j] = 1

        i = int(frame.shape[0] / 2)
        while i < int(7 * frame.shape[0] / 8):
            j = 0
            while j < int(frame.shape[1] / 2):
                """
                element元素说明
                便于计算圆形邻域的相关系数，引入变量element
                第一个元素：M_{Ci} * M_{Ci}'之和
                第二个元素：M_{Ci}之和
                第三个元素：M_{Ci}'之和
                第四个元素：M_{Ci}^2之和
                第五个元素：(M_{Ci}')^2之和
                """
                element = [0, 0, 0, 0, 0]
                if candidate[i][j] == -1:
                    # 计算直径为7的圆邻域的色彩强度，与数据结构中数组和矩阵的关系相似
                    p = -3
                    while p < 4:
                        q = -3
                        while q < 4:
                            if circle_neighborhood[p][q] == 1:
                                # 以圆心像素点为（0,0）
                                # 计算其余点的坐标和旋转180度后的坐标
                                # 原坐标
                                imgx = i + p
                                imgy = j + q
                                # 旋转180度后的坐标
                                imgxp = i - p
                                imgyp = j - q
                                element[0] = element[0] + int(GrayImage[imgx][imgy]) * int(GrayImage[imgxp][imgyp])
                                element[1] = element[1] + int(GrayImage[imgx][imgy])
                                element[2] = element[2] + int(GrayImage[imgxp][imgyp])
                                element[3] = element[3] + int(GrayImage[imgx][imgy] ** 2)
                                element[4] = element[4] + int(GrayImage[imgxp][imgyp] ** 2)
                            q = q + 1
                        p = p + 1

                    pc = (counter * element[0] - element[1] * element[2]) / (
                            np.sqrt(counter * element[3] - element[1] ** 2) * np.sqrt(
                        counter * element[4] - element[2] ** 2))
                    if pc > 0.5:  # 相关系数足够大的点被判断为特征点(对称系数为0的为特征点——A Twofold...)
                        gridpoints[i][j] = 1
                        # point_size = 1
                        # point_color = (0, 0, 255)
                        # thickness = 0  # 可以为 0 、4、8
                        #
                        # cv2.circle(frame, (j, i), point_size, point_color, thickness)

                else:
                    gridpoints[i][j] = 0
                j = j + 1
            i = i + 1
        # cv2.imshow('14', frame)
        # cv2.waitKey(0)  # 按0退出
        return gridpoints

    """
    bfs8:
    8邻域广度优先搜索
    确定唯一特征点位置
    """

    def bfs8(self, frame, g, x, y):
        counter = 1
        queue = [[x, y]]
        ans = [0, 0]
        self.flag[x][y] = 1
        ans[0] = 1.0 * x
        ans[1] = 1.0 * y
        while len(queue) > 0:
            current = queue.pop(0)
            self.flag[current[0]][current[1]] = 1
            i = 0
            while i < 8:
                temp = [0, 0]
                temp[0] = current[0] + self.nx[i]
                temp[1] = current[1] + self.ny[i]
                if temp[0] < 0 or temp[0] > frame.shape[0] or temp[1] < 0 or temp[1] > frame.shape[1]:
                    i = i + 1
                    continue
                if self.flag[int(temp[0])][int(temp[1])] or g[int(temp[0])][int(temp[1])] == 0:
                    i = i + 1
                    continue
                self.flag[int(temp[0])][int(temp[1])] = 1
                queue.append(temp)
                ans[0] = ans[0] + 1.0 * temp[0]
                ans[1] = ans[1] + 1.0 * temp[1]
                counter = counter + 1
                i = i + 1
        ans[0] = ans[0] / counter
        ans[1] = ans[1] / counter
        return ans

    """
    get_feature_point:
    调用8邻域深度优先搜索
    确定单一特征点位置
    """

    def get_feature_point(self, frame, gps):
        q = []
        i = int(frame.shape[0] / 2)
        while i < int(7 * frame.shape[0] / 8):
            j = 0
            while j < int(frame.shape[1] / 2):
                if self.flag[i][j] == 1 or gps[i][j] == 0:
                    j = j + 1
                    continue
                temp = self.bfs8(frame, gps, i, j)
                q.append(temp)
                j = j + 1
            i = i + 1
        return q

    """
    decode:
    根据颜色解码
    确定特征点在矩阵的位置
    """

    def decode(self, frame, feature_point):
        points = []
        position = []
        frame = aug(frame)
        color_map = np.zeros((frame.shape[0], frame.shape[1]))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(frame)
        for i in range(0, frame.shape[0]):
            for j in range(0, frame.shape[1]):
                if l[i][j] < 100:
                    color_map[i][j] = 3
                    frame[i][j] = np.array([0, 0, 0])
                elif l[i][j] > 200:
                    frame[i][j] = np.array([255, 255, 255])
                    color_map[i][j] = 255
                else:
                    if b[i][j] < 120:
                        color_map[i][j] = 0
                        frame[i][j] = np.array([255, 0, 0])
                    else:
                        if a[i][j] > 125:
                            color_map[i][j] = 1
                            frame[i][j] = np.array([0, 0, 255])
                        else:
                            color_map[i][j] = 2
                            frame[i][j] = np.array([0, 255, 0])

        # cv2.imshow('lab', frame)
        # cv2.waitKey(0)  # 按0退出
        data = GF(1, 1, 1, 1, 1, 1)
        # map = np.zeros((4, 4, 4, 4, 4, 4, 14))

        map = np.zeros((4096, 2))

        i = 0
        while i < 64:
            j = 1
            while j < 62:
                index = data[i][j - 1] * 4 ** 5 + data[i][j] * 4 ** 4 + data[i][j + 1] * 4 ** 3 + data[i + 1][
                    j - 1] * 4 ** 2 + data[i + 1][j] * 4 + data[i + 1][j + 1]
                map[index] = [i, j]
                j = j + 1
            i = i + 1

        for point in feature_point:
            if color_map[int(point[0])][int(point[1]) + 9] != 255 and color_map[int(point[0])][
                int(point[1]) - 9] != 255:
                pass
            else:
                i = int(point[0])
                j = int(point[1])
                index = int(color_map[i - 9][j - 18]) * 4 ** 5 + int(color_map[i - 9][j]) * 4 ** 4 + int(
                    color_map[i - 9][j + 18]) * 4 ** 3 + int(color_map[i + 9][j - 18]) * 4 ** 2 + int(
                    color_map[i + 9][j]) * 4 + int(color_map[i + 9][j + 18])
                # point_size = 1
                # point_color = (255, 255, 255)
                # thickness = 0  # 可以为 0 、4、8
                # print(color_map[i - 9][j - 18], color_map[i - 9][j], color_map[i - 9][j + 18], color_map[i + 9][j - 18],
                #       color_map[i + 9][j], color_map[i + 9][j + 18])
                # print(index)
                #
                # cv2.circle(frame, (int(j - 18), int(i - 9)), point_size, point_color, thickness)
                # cv2.circle(frame, (int(j), int(i - 9)), point_size, point_color, thickness)
                # cv2.circle(frame, (int(j + 18), int(i - 9)), point_size, point_color, thickness)
                # cv2.circle(frame, (int(j - 18), int(i + 9)), point_size, point_color, thickness)
                # cv2.circle(frame, (int(j), int(i + 9)), point_size, point_color, thickness)
                # cv2.circle(frame, (int(j + 18), int(i + 9)), point_size, point_color, thickness)
                try:
                    if map[index][0] < 10 and map[index][1] < 8:
                        points.append(list(map[int(index)]))
                        position.append([i, j])
                except:
                    pass
        cv2.imwrite('testt3.png', frame)
        # cv2.imshow('lab', frame)
        # cv2.waitKey(0)  # 按0退出
        return points, position

    def process(self, img_rd):
        self.flag = np.zeros((img_rd.shape[0], img_rd.shape[1]))
        # 1024*1280 -1候选点，-3非候选点
        candidate = self.get_candidate_points(frame=img_rd)
        # 1024*1280 1角点，0非角点
        gridpoints = self.get_grid_points(frame=img_rd, candidate=candidate)
        # 存有特征点的列表 -1特征点
        featurepoints_position = self.get_feature_point(frame=img_rd, gps=gridpoints)

        feature_points, position = self.decode(frame=img_rd, feature_point=featurepoints_position)

        index = len(feature_points) // 2
        try:
            pixel_distance = math.sqrt((position[index + 1][0] - position[index][0]) ** 2 +
                                       (position[index + 1][1] - position[index][1]) ** 2)
            world_distance = math.sqrt((feature_points[index + 1][0] * 2 - feature_points[index][0] * 2) ** 2 +
                                       (feature_points[index + 1][1] * 2 - feature_points[index][1] * 2) ** 2)
            self.scale = world_distance / pixel_distance

        except:
            self.scale = 0.11

        # 绘制特征点
        # point_size = 1
        # point_color = (0, 0, 255)
        # thickness = 0  # 可以为 0 、4、8
        #
        # for point in featurepoints_position:
        #     cv2.circle(img_rd, (int(point[1]), int(point[0])), point_size, point_color, thickness)
        # cv2.imwrite('testt2.png', img_rd)

        self.draw_note(img_rd)
        self.update_fps()

    def run(self, frame):
        # cap = cv2.VideoCapture(0)
        self.process(frame)

        return self.scale
