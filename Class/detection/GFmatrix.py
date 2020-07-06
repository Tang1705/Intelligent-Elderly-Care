# plus、multi、GF三个函数用于生成伪随机矩阵
def plus(x, y):
    if x == y:
        return 0
    elif (x == 1 and y == 2) or (x == 2 and y == 1):
        return 3
    elif (x == 1 and y == 3) or (x == 3 and y == 1):
        return 2
    elif (x == 2 and y == 3) or (x == 3 and y == 2):
        return 1
    elif x == 0:
        return y
    elif y == 0:
        return x


def multi(x, y):
    if x == 0 or y == 0:
        return 0
    elif x == 1:
        return y
    elif y == 1:
        return x
    elif x == 2 and y == 2:
        return 3
    elif x == 3 and y == 3:
        return 2
    else:
        return 1


def GF(a, b, c, d, e, f):
    data = []

    for i in range(0, 4095):
        data.append(0)

    data[0] = a
    data[1] = b
    data[2] = c
    data[3] = d
    data[4] = e
    data[5] = f

    for i in range(6, 4095):
        data[i] = plus(data[i - 1], multi(data[i - 2], 3))
        data[i] = plus(data[i], multi(data[i - 3], 2))
        data[i] = plus(data[i], multi(data[i - 4], 1))
        data[i] = plus(data[i], multi(data[i - 5], 1))
        data[i] = plus(data[i], multi(data[i - 6], 3))

    res = []
    for i in range(0, 65):
        res.append([])
        for j in range(0, 63):
            res[i].append(0)
    for i in range(0, 4095):
        res[i % 65][i % 63] = data[i]

    return res