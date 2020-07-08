# -*- coding:utf-8 -*-
'''
前向逐步线性回归


'''
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif']=['SimHei']#这两句作用为防止中文乱码
plt.rcParams['axes.unicode_minus']=False
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

## 损失值计算
def rssError(yMat,yTest):
    result = np.sum(np.power((yMat-yTest),2),0)
    return result

def stageWise(xArr,yArr,eps=0.01,numIt=300):
    xMat = np.mat(xArr);yMat = np.mat(yArr).T
    yMean = np.mean(yMat,0)
    # 数据标准化
    xMean = np.mean(xMat,0)
    yMat = yMat-yMean
    xVar = np.var(xMat,0)
    xMat = (xMat-xMean)/xVar
    #
    m,n = np.shape(xMat)
    returnMat = np.zeros((numIt,n))
    ws = np.zeros((n,1));wsTest = ws.copy();wsMax = ws.copy()
    for i in range(numIt):
        lowestError = np.power(10,5)#初始化一个最大值
        for j in range(n):
            for sign in [-1,1]:
                wsTest = ws.copy()
                wsTest[j]+=eps*sign
                yTest = xMat*wsTest
                rssE = rssError(yMat.A,yTest.A)
                #print("rssE:",rssE)
                if  rssE<lowestError:
                    lowestError=rssE
                    wsMax = wsTest
        ws = wsMax.copy()
        returnMat[i,:] = ws.T
        print("第{}次优化，ws.T={}".format(i+1,ws.T))
    return returnMat
## 将权值的变化显示在图像上
def showchange(returnMat,n):
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    colors = ['red','green','block','blue','yellow','pink']
    print(np.shape(returnMat[:,1]))
    for i in range(n):
        ax.plot(range(300),returnMat[:,i],label='属性{}'.format(i+1))
    ax.legend(loc='lower left',framealpha=0.2)
    plt.show()
if __name__ == '__main__':
    xvalue,yvalue = LoadData('datasets/abalone.txt')
    m,n = np.shape(xvalue)
    print(n)
    returnMat = stageWise(xvalue,yvalue,0.01,300)
    showchange(returnMat,n)

