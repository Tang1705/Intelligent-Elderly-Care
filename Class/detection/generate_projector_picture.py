import cv2
import numpy as np
from PIL import Image
from GFmatrix import GF


# 生成一个菱形的填色像素坐标
def set_matrix(dimension):
    color = []

    for i in range(0, dimension):
        color.append([])
        for j in range(0, dimension):
            color[i].append(0)
    demission_temp = dimension - 1
    for i in range(0, dimension):
        for j in range(0, dimension):
            if i < demission_temp // 2:
                if j >= demission_temp // 2 - i and j <= demission_temp // 2 + i or j == demission_temp // 2:
                    color[i][j] = 1
            elif i > demission_temp // 2:
                temp = (demission_temp) - i
                if j >= demission_temp // 2 - temp and j <= demission_temp // 2 + temp or j == demission_temp // 2:
                    color[i][j] = 1
            else:
                color[i][j] = 1
    return color


if __name__ == '__main__':
    # data = fileload()
    data = GF(1, 1, 1, 1, 1, 1)
    dimension = int(input("Please enter the length of the diagonal of the  rhombus:"))
    color = set_matrix(dimension)

    x = 912
    y = 1140
    bgcolor = 0xffffff  # 投影图案是白色背景

    c = Image.new("RGB", (x, y), bgcolor)

    start_row = end_row = 0
    start_column = end_column = 0

    if 63 * dimension > 912:
        start_row = 0
        end_row = 912
    else:
        start_row = (912 - (63 * dimension)) // 2
        end_row = start_row + 63 * dimension

    if 65 * dimension > 1140:
        start_column = 0
        end_column = 1140
    else:
        start_column = (1140 - (65 * dimension)) // 2
        end_column = start_column + 65 * dimension
    # 以13*13的菱形为例，暂时没有修改菱形超过图片大小的情况
    i = start_row
    while i < end_row:
        if i > end_row - dimension or i == end_row - dimension:
            break
        else:
            t = (i - start_row) // dimension
        j = start_column
        while j < end_column:
            if j > end_column - dimension or j == end_column - dimension:
                break
            else:
                q = (j - start_column) // dimension
            if data[q][t] == 0:
                for k in range(0, dimension):
                    for m in range(0, dimension):
                        if color[k][m] == 1:
                            c.putpixel([i + k, j + m], (0, 0, 255))  # 蓝色
            elif data[q][t] == 1:
                for k in range(0, dimension):
                    for m in range(0, dimension):
                        if color[k][m] == 1:
                            c.putpixel([i + k, j + m], (255, 0, 0))  # 红色
            elif data[q][t] == 2:
                for k in range(0, dimension):
                    for m in range(0, dimension):
                        if color[k][m] == 1:
                            c.putpixel([i + k, j + m], (0, 255, 0))  # 绿色
            else:
                for k in range(0, dimension):
                    for m in range(0, dimension):
                        if color[k][m] == 1:
                            c.putpixel([i + k, j + m], (0, 0, 0))
            j = j + dimension
        i = i + dimension
    c.show()
    c.save("projector.png")
