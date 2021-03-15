import os

sizeM = 10
sizeN = 10


def v(inputPos, type):
    if type == "cell":
        [y, x, d] = inputPos
        rePos = sizeN * 4 * (y - 1) + 4 * (x - 1) + d
    else:
        [dy, dx, ddy, ddx] = inputPos
        rePos = (dy - 1) * sizeN * sizeN * sizeM
        rePos += (dx - 1) * sizeN * sizeM
        rePos += (ddy - 1) * sizeN
        rePos += ddx
    return rePos


def clause():
    res = []
    return res


if __name__ == '__main__':
    for dy in range(1, sizeM + 1):
        for dx in range(1, sizeN + 1):
            for dd in range(1, 5):
                pos = v([dy, dx, dd], "cell")

    for dy in range(1, sizeM + 1):
        for dx in range(1, sizeN + 1):
            for ddy in range(1, sizeM + 1):
                for ddx in range(1, sizeN + 1):
                    pos = v([dy, dx, ddy, ddx], "connection")
                    print(pos)
