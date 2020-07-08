# -*- coding:utf-8 -*-
'''
岭回归算法改进线性回归
'''
import numpy as np
import matplotlib.pyplot as plt

#加载数据
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

## 主函数，计算模型参数
def ridgeRegres(xMat,yMat,lam=0.2):
    xTx = xMat.T*xMat
    denom = xTx+np.eye(np.shape(xMat)[1])*lam
    if np.linalg.det(denom)==0.0:
        print("This matrix is singular ,cannot do inverse")
        return
    ws = denom.I*(xMat.T*yMat)
    return ws
## 使用不同的λ进行测试
def ridgeTest(xArr,yArr):
    xMat = np.mat(xArr);yMat = np.mat(yArr).T
    numTestPts = 9
    print(np.shape(xMat)[1])
    lamudas=[]
    wMat = np.zeros((numTestPts,np.shape(xMat)[1]))
    for i in range(numTestPts):
        lamudas.append(np.exp(i-3))
        print("np.exp({})={}".format((i-3),np.exp(i-3)))
        ws = ridgeRegres(xMat,yMat,np.exp(i-3))
        wMat[i,:] = ws.T
    return wMat,lamudas
## 不同的λ进行比较
def showcompare(abx,ridgeWeights,yvalue,lamudas):
    fig = plt.figure()
    plt.rcParams['font.sans-serif']=['SimHei']#这两句作用为防止中文乱码
    plt.rcParams['axes.unicode_minus']=False
    fig.subplots_adjust(hspace=0.4, wspace=0.4)
    axs = [fig.add_subplot(3,3,i) for i in range(1,10)]
    xCopy = np.array(abx.copy())
    srtInd = xCopy[:,1].argsort(0)
    for i in range(9):
        yHat = abx*np.mat(ridgeWeights[i]).T
        yHat = np.array(yHat).flatten()
        print("yHat,yHat.shape",yHat,np.shape(yHat))
        axs[i].plot(xCopy[srtInd][:,1],yHat[srtInd])
        axs[i].scatter(xCopy[srtInd][:,1],yvalue[srtInd],s=5,alpha=0.7,color='red')
        axs[i].set_title("λ={:.3f}(e的{}次方)".format(lamudas[i],i-3))
    plt.show()
## 交叉验证
def Cross_validation(xMat,yMat,ridgeWeights,lamudas):
    yMat = np.array(yMat).reshape((len(yMat),1))
    lossvalue = []
    for i in range(9):
        yHat = xMat*np.mat(ridgeWeights[i]).T
        lossvalue.append(np.sum(np.abs(yHat-yMat)))
    lossvalue = np.array(lossvalue)
    result = lossvalue.argmin()
    return lamudas[result]


if __name__ == '__main__':
    xvalue,yvalue = LoadData('datasets/ex0.txt')
    print(len(xvalue))
    abx = xvalue[:180];aby =yvalue[:180]#实验数据
    testx = xvalue[180:];testy = yvalue[180:]#测试数据
    yvalue = np.array(aby)
    ridgeWeights,lamudas = ridgeTest(abx,aby)
    showcompare(abx,ridgeWeights,yvalue,lamudas)
    aplamuda = Cross_validation(testx,testy,ridgeWeights,lamudas)
    print("最合适的λ是：",aplamuda)
