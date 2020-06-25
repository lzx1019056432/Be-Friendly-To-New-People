# -*- coding:utf-8 -*-
'''
参考《机器学习实战》
使用最小二乘法算法进行求解问题

'''

import numpy as np
import matplotlib.pyplot as plt
def LoadData(filename):
    dataMat = []
    labelMat = []
    with open(filename) as f:
        numFeat = len(f.readline().split('\t'))-1#这里会导致忽略第一个数据
        for line in f.readlines():
            lineArr = []
            curLine = line.strip().split('\t')
            for i in range(numFeat):
               lineArr.append(float(curLine[i]))
            dataMat.append(lineArr)
            labelMat.append(float(curLine[-1]))
        return dataMat,labelMat
def standRegres(xArr,yArr):
    xMat = np.mat(xArr);yMat = np.mat(yArr).T#由于原来形状是(1,199)，所以这里需要转置
    print("yMat",yMat.shape)#yMat (199, 1)
    xTx = xMat.T*xMat
    if np.linalg.det(xTx)==0.0:
        print("false")
        return
    print("xtx.shape",xTx.shape)#形状：(2,2)
    print("xTx.I",xTx.I)#矩阵的逆
    print("xMat.T",(xMat.T).shape)
    ws = xTx.I*(xMat.T*yMat)#(xMat.T*yMat)形状为(2,1)
    return ws

def showdata(xArr,yMat,ws):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    xCopy = xArr.copy()
    xCopy.sort(0)
    yHat = xCopy*ws
    ax.scatter(xArr[:,1].flatten().tolist(),yMat.T[:,0].flatten().tolist(),s=20,alpha=0.5)
    ax.plot(xCopy[:,1],yHat)
    plt.show()
def pearsoncor(yHat,yMat):
    result = np.corrcoef(yHat.T,yMat)#相关系数分析。越接近1，表示相似度越高
    print("pearson-result:",result)


if __name__ == '__main__':
    xArr,yArr = LoadData('datasets/ex0.txt')
    print(xArr)
    ws = standRegres(xArr,yArr)
    print("ws:",ws)#输出w
    xMat = np.mat(xArr)
    yMat = np.mat(yArr)
    yHat = xMat*ws#获得预测值
    showdata(xMat,yMat,ws)#图像显示
    pearsoncor(yHat,yMat)#进行相关度分析
    print("yArr[0]",yArr[0])

