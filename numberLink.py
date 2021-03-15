import os

sizeM = 10
sizeN = 10


def v(inputPos, type=None):
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


class NumberLinkClause(object):
    """docstring for NumberLinkClause"""

    def __init__(self):
        super(NumberLinkClause, self).__init__()
        self.clauses = []

    def addClause_1(self, dy, dx):
        # each square must have only one output
        listV = []
        for d in range(1, 5):
            listV.append(v([dy, dx, d], "cell"))
        [x, y, z, t] = listV
        self.clauses.append(listV)
        for i in range(1, 5):
            for j in range(i + 1, 5):
                self.clauses.append([-listV[i - 1], -listV[j - 1]])

    def addClause_2(self, dy, dx):
        # square which doest have any number must not have cross path
        listV = []
        for d in range(1, 5):
            listV.append(v([dy, dx, d], "cell"))
        [x, y, z, t] = listV
        for i in range(1, 5):
            for j in range(i + 1, 5):
                for z in range(j + 1, 5):
                    xx = listV[i - 1]
                    yy = listV[j - 1]
                    zz = listV[z - 1]
                    self.clauses.append([xx, yy, zz])
                    self.clauses.append([-xx, -yy, -zz])

    def getAdj(self, dy, dx, d):
        if d == 1:
            return [dy, dx + 1]
        elif d == 2:
            return [dy + 1, dx]
        elif d == 3:
            return [dy, dx - 1]
        return dy - 1, dx

    def addClause_3(self, dy, dx, d):
        # square adjacent clause
        x = v([dy, dx, d], "cell")
        newY, newX = self.getAdj(dy, dx, d)
        if 1 <= newY and newY <= sizeM and 1 <= newX and newX <= sizeN:
            vAdj = v([dy, dx, newY, newY])
            self.clauses.append([-x, vAdj])
            self.clauses.append([-vAdj, x])

    def addClause_4(self, dy):
        # squares at the edges clause along the y axis
        dx1 = 1
        dx2 = sizeN
        vDx1 = v([dy, dx1, 3], "cell")
        vDx2 = v([dy, dx2, 1], "cell")
        self.clauses.append([-vDx1])
        self.clauses.append([-vDx2])

    def addClause_5(self, dx):
        # squares at the edges clause along the x axis
        dy1 = 1
        dy2 = sizeM
        vDy1 = v([dy1, dx, 4], "cell")
        vDy2 = v([dy2, dx, 2], "cell")
        self.clauses.append([-vDy1])
        self.clauses.append([-vDy2])

    def addClause_6(self, dy, dx, dk, dl, dm, dn):
        # if (dy, dx) == (dk, dl):
        #     return 
        # if (dk, dl) == (dm, dn):
        #     return 
        # if (dy, dx) == (dm, dn):
        #     return
        vCijkl = v([dy, dx, dk, dl], "connection")
        vCklmn = v([dk, dl, dm, dn], "connection")
        vCijmn = v([dy, dx, dm, dn], "connection")
        self.clauses.append([-vCijkl, -vCklmn, vCijmn])

    def getLen(self):
        return len(self.clauses)


if __name__ == '__main__':
    matrix = [[-1] * sizeM] * sizeN
    for dy in range(1, sizeM + 1):
        for dx in range(1, sizeN + 1):
            for dd in range(1, 5):
                pos = v([dy, dx, dd], "cell")

    for dy in range(1, sizeM + 1):
        for dx in range(1, sizeN + 1):
            for ddy in range(1, sizeM + 1):
                for ddx in range(1, sizeN + 1):
                    pos = v([dy, dx, ddy, ddx], "connection")

    numberCls = NumberLinkClause()
    for dy in range(1, sizeM + 1):
        for dx in range(1, sizeN + 1):
            if matrix[dy - 1][dx - 1] != -1:
                numberCls.addClause_1(dy, dx)
            else:
                numberCls.addClause_2(dy, dx)

    for dy in range(1, sizeM + 1):
        for dx in range(1, sizeN + 1):
            for dd in range(1, 5):
                numberCls.addClause_3(dy, dx, dd)

    for dy in range(1, sizeM + 1):
        numberCls.addClause_4(dy)

    for dx in range(1, sizeN + 1):
        numberCls.addClause_5(dx)

    for dy in range(1, sizeM  + 1):
        for dx in range(1, sizeN + 1):
            for dk in range(1, sizeM + 1):
                for dl in range(1, sizeN + 1):
                    for dm in range(1, sizeM + 1):
                        for dn in range(1, sizeN + 1):
                            numberCls.addClause_6(dy, dx, dk, dl, dm, dn)

    # print(numberCls.getLen())
