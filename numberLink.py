import pycosat
import numpy as np


class Variable(object):
    """docstring for Variable"""

    def __init__(self, arg):
        super(Variable, self).__init__()
        self.sizeM = arg[0]
        self.sizeN = arg[1]
        self.cellSize = arg[0] * arg[1] * 4

    def getV(self, inputPos, type=None):
        if type == "cell":
            [y, x, d] = inputPos
            rePos = self.sizeN * 4 * (y - 1) + 4 * (x - 1) + d
        else:
            [dy, dx, ddy, ddx] = inputPos
            rePos = (dy - 1) * self.sizeN * self.sizeN * self.sizeM
            rePos += (dx - 1) * self.sizeN * self.sizeM
            rePos += (ddy - 1) * self.sizeN
            rePos += ddx
            rePos += self.cellSize
        return rePos

    def getVCell(self, x):
        counter = 0
        for dy in range(1, self.sizeM + 1):
            for dx in range(1, self.sizeN + 1):
                for dd in range(1, 5):
                    counter += 1
                    if counter == x:
                        return [dy, dx, dd]
        return -1

    def getVConnection(self, x):
        counter = 0
        for dy in range(1, self.sizeM + 1):
            for dx in range(1, self.sizeN + 1):
                for ddy in range(1, self.sizeM + 1):
                    for ddx in range(1, self.sizeN + 1):
                        counter += 1
                        if counter == x:
                            return[dy, dx, ddy, ddx]
        return -1

    def getSpecificV(self, x):
        if x <= self.cellSize:
            return self.getVCell(x)
        return self.getVConnection(x - self.cellSize)


class NumberLinkClause(object):
    """docstring for NumberLinkClause"""

    def __init__(self, arg):
        super(NumberLinkClause, self).__init__()
        self.clauses = []
        self.sizeM = arg[0]
        self.sizeN = arg[1]
        self.v = Variable([self.sizeM, self.sizeN])

    def addClause_1(self, dy, dx):
        # each square must have only one output
        listV = []
        for d in range(1, 5):
            listV.append(self.v.getV([dy, dx, d], "cell"))
        [x, y, z, t] = listV
        self.clauses.append(listV)
        for i in range(1, 5):
            for j in range(i + 1, 5):
                self.clauses.append([-listV[i - 1], -listV[j - 1]])

    def addClause_2(self, dy, dx):
        # square which doest have any number must not have cross path
        listV = []
        for d in range(1, 5):
            listV.append(self.v.getV([dy, dx, d], "cell"))
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
            return [dy, dx - 1]
        elif d == 2:
            return [dy - 1, dx]
        elif d == 3:
            return [dy, dx + 1]
        return [dy + 1, dx]

    def addClause_3(self, dy, dx, d):
        # square adjacent clause
        x = self.v.getV([dy, dx, d], "cell")
        tmp = [3, 4, 1, 2]
        newY, newX = self.getAdj(dy, dx, d)
        # print(newY, newX, dy, dx, d)
        if 1 <= newY and newY <= self.sizeM and 1 <= newX and newX <= self.sizeN:
            vAdj = self.v.getV([dy, dx, newY, newX], "connection")
            self.clauses.append([-x, vAdj])
            # self.clauses.append([-vAdj, x])
            vAdj = self.v.getV([newY, newX, tmp[d - 1]], "cell")
            self.clauses.append([-x, vAdj])
            self.clauses.append([-vAdj, x])

    def addClause_4(self, dy):
        # squares at the edges clause along the y axis
        dx1 = 1
        dx2 = self.sizeN
        vDx1 = self.v.getV([dy, dx1, 1], "cell")
        vDx2 = self.v.getV([dy, dx2, 3], "cell")
        self.clauses.append([-vDx1])
        self.clauses.append([-vDx2])

    def addClause_5(self, dx):
        # squares at the edges clause along the x axis
        dy1 = 1
        dy2 = self.sizeM
        vDy1 = self.v.getV([dy1, dx, 2], "cell")
        vDy2 = self.v.getV([dy2, dx, 4], "cell")
        self.clauses.append([-vDy1])
        self.clauses.append([-vDy2])

    def addClause_6(self, dy, dx, dk, dl, dm, dn):
        if (dy, dx) == (dk, dl):
            return
        if (dk, dl) == (dm, dn):
            return
        if (dy, dx) == (dm, dn):
            return
        vCijkl = self.v.getV([dy, dx, dk, dl], "connection")
        vCklmn = self.v.getV([dk, dl, dm, dn], "connection")
        vCijmn = self.v.getV([dy, dx, dm, dn], "connection")
        self.clauses.append([-vCijkl, -vCklmn, vCijmn])

    def addClause_7(self, dy, dx, dk, dl):
        vCijkl = self.v.getV([dy, dx, dk, dl], "connection")
        self.clauses.append([vCijkl])

    def addClause_8(self, dy, dx, dk, dl):
        vCijkl = self.v.getV([dy, dx, dk, dl], "connection")
        self.clauses.append([-vCijkl])

    def getLen(self):
        return len(self.clauses)

    def getClause(self):
        return self.clauses


class NumberLink(object):
    """docstring for NumberLink"""

    def __init__(self, arg):
        super(NumberLink, self).__init__()
        self.arg = arg
        self.sizeM = arg.shape[0]
        self.sizeN = arg.shape[1]
        self.v = Variable([self.sizeM, self.sizeN])
        matrix = arg
        for dy in range(1, self.sizeM + 1):
            for dx in range(1, self.sizeN + 1):
                for dd in range(1, 5):
                    pos = self.v.getV([dy, dx, dd], "cell")
                    print(pos, dy, dx, dd)
        print("break")
        for dy in range(1, self.sizeM + 1):
            for dx in range(1, self.sizeN + 1):
                for ddy in range(1, self.sizeM + 1):
                    for ddx in range(1, self.sizeN + 1):
                        pos = self.v.getV([dy, dx, ddy, ddx], "connection")
                        print(pos, dy, dx, ddy, ddx)
        print("break")
        numberCls = NumberLinkClause([self.sizeM, self.sizeN])
        for dy in range(1, self.sizeM + 1):
            for dx in range(1, self.sizeN + 1):
                if matrix[dy - 1][dx - 1] != -1:
                    numberCls.addClause_1(dy, dx)

        for dy in range(1, self.sizeM + 1):
            for dx in range(1, self.sizeN + 1):
                if matrix[dy - 1][dx - 1] == -1:
                    numberCls.addClause_2(dy, dx)

        for dy in range(1, self.sizeM + 1):
            for dx in range(1, self.sizeN + 1):
                for dd in range(1, 5):
                    numberCls.addClause_3(dy, dx, dd)

        for dy in range(1, self.sizeM + 1):
            numberCls.addClause_4(dy)

        for dx in range(1, self.sizeN + 1):
            numberCls.addClause_5(dx)

        for dy in range(1, self.sizeM + 1):
            for dx in range(1, self.sizeN + 1):
                for dk in range(1, self.sizeM + 1):
                    for dl in range(1, self.sizeN + 1):
                        for dm in range(1, self.sizeM + 1):
                            for dn in range(1, self.sizeN + 1):
                                numberCls.addClause_6(dy, dx, dk, dl, dm, dn)

        for dy in range(1, self.sizeM + 1):
            for dx in range(1, self.sizeN + 1):
                for dk in range(1, self.sizeM + 1):
                    for dl in range(1, self.sizeN + 1):
                        posY = dy - 1
                        posX = dx - 1
                        posK = dk - 1
                        posL = dl - 1
                        if ((dy, dx) != (dk, dl)) and (matrix[posY][posX] == matrix[posK][posL]):
                            if (matrix[posY][posX] != -1):
                                numberCls.addClause_7(dy, dx, dk, dl)
                        # if (matrix[posY][posX] != matrix[posK][posL]) and (matrix[posY][posX] != -1) and (matrix[posK][posL] != -1):
                        #     numberCls.addClause_8(dy, dx, dk, dl)
        self.clauses = numberCls.getClause()
        for obj in self.clauses:
            print(obj)

    def getClause(self):
        return self.clauses

    def getVariable(self, x):
        return self.v.getSpecificV(x)

    def getListEdge(self):
        print("solving...")
        result = pycosat.solve(self.clauses)
        if result == "UNSAT":
            return []
        listEdge = []
        for x in result:
            if x > 0:
                abc = self.getVariable(x)
                if len(abc) <= 3:
                    listEdge.append(abc)
        return listEdge


if __name__ == '__main__':
    matrix = [[0, -1], [-1, 0]]
    res = NumberLink(np.asarray(matrix))
    print("loaded Clauses")
    result = pycosat.solve(res.getClause())
    print(len(res.getClause()))
    print(result)
    # for sol in pycosat.itersolve(res.getClause()):
    #     print(sol)
    a = [-1 for x in range(1000)]
    tmp = [4, 8, 10, 11, 13, 14, 18, 19, 20, 25, 24, 30, 28, 31]
    for x in tmp:
        a[x] = 1
    # for x in result:
    #     if x > 0:
    #         a[x] = 1
    print("debug")
    for x in res.getClause():
        listT = []
        for xi in x:
            if xi < 0:
                listT.append(-a[-xi])
            else:
                listT.append(a[xi])
        tmpRes = 0
        for xi in listT:
            if xi == 1:
                tmpRes = 1
        print(x, "=====================> ", tmpRes)
    # from pysat.solvers import Minisat22
    # with Minisat22(res.getClause()) as m:
    #     print(m.solve())
    for x in result:
        if x > 0:
            print(x, res.getVariable(x))
    # abc = res.getListEdge()
    # print(abc)
