# -*- coding:utf-8 -*-

'''
局部加权线性回归算法

'''
import numpy as np
import matplotlib.pyplot as plt
def LoadData(filename):
    dataMat = []
    labelMat = []
    with open(filename) as f:
        numFeat = len(f.readline().split('\t'))-1#这里会导致忽略第一个数据
        f.seek(0)
        for line in f.readlines():
            lineArr = []
            curLine = line.strip().split('\t')
            for i in range(numFeat):
                lineArr.append(float(curLine[i]))
            dataMat.append(lineArr)
            labelMat.append(float(curLine[-1]))
        return dataMat,labelMat

#局部加权线性回归
def lwlr(testPoint,xArr,yArr,k=0.1):
    xMat = np.mat(xArr);yMat = np.mat(yArr).T#
    m = np.shape(xMat)[0]#数据个数
    #为什么创建方阵，是为了实现给每个数据增添不同的权值
    weights = np.mat(np.eye(m))#初始化一个阶数等于m的方阵，其对角线的值为1，其余值均为0
    for j in range(m):
        diffMat = testPoint-xMat[j,:]
        weights[j,j] = np.exp(diffMat*diffMat.T/(-2.0*k**2)) #e的指数形式
    xTx = xMat.T*(weights*xMat)
    #print("weights",weights)
    if np.linalg.det(xTx)==0.0:#通过计算行列式的值来判是否可逆
        print("this matrix is singular,cannot do inverse")
        return
    ws = xTx.I*(xMat.T*(weights*yMat))
    return testPoint*ws
def lwlrTest(testArr,xArr,yArr,k=1.0):
    m = np.shape(testArr)[0]
    yHat = np.zeros(m)
    for i in range(m):
        yHat[i] = lwlr(testArr[i],xArr,yArr,k)
    return yHat
#图像显示
def lwlshow(xArr,yMat,yHat,k):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    xCopy = np.array(xArr.copy())
    srtInd = xCopy[:,1].argsort(0)
    print("xSort",xCopy[srtInd])
    ax.plot(xCopy[srtInd][:,1],yHat[srtInd])
    yMat = np.array(yMat)
    ax.scatter(xCopy[srtInd][:,1].tolist(),yMat[srtInd],s=10,alpha=0.7)
    ax.set_title("k={}".format(str(k)))
    plt.show()
if __name__ == '__main__':
    xArr,yArr = LoadData('datasets/ex0.txt')
    ytest = lwlr(xArr[0],xArr,yArr,1.0)
    print("xArr[0],ytest",xArr[0],ytest)
    k=0.01
    yHat = lwlrTest(xArr,xArr,yArr,k)
    lwlshow(xArr,yArr,yHat,k)