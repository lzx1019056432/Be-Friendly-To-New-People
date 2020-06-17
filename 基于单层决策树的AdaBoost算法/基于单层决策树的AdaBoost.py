# -*- coding:utf-8 -*-
'''
@author:梁先森
@blog：
@item：基于单层决策树的AdaBoost/
@detail:
单层决策树 也就是使用一个属性对数据进行分类
'''
import numpy as np
def loadSimpData():
    dataMat = []
    labelMat = []
    data = open('datasets/testSet.txt')
    for dataline in data.readlines():
        linedata = dataline.split('\t')
        dataMat.append([float(linedata[0]),float(linedata[1])])
        labelMat.append(float(linedata[2].replace('\n','')))
    return dataMat,labelMat
#单层决策树生成函数
#参数分别为数据、属性个数、
#通过阈值比较对数据进行分类，所有在一边的将会被分类到类别1
def stumpClassify(dataMatrix,dimen,threshVal,threshIneq):
    retArray = np.ones((np.shape(dataMatrix)[0],1))#创建一个初始值为1的大小为（m，1）的数组
    if(threshIneq=='lt'):#lt表示小于的意思
        retArray[dataMatrix[:,dimen]<=threshVal]=-1.0
    else:
        retArray[dataMatrix[:,dimen]>threshVal]=-1.0
    return retArray
#参数分别是 数据、数据分类、数据权重
#此方法用来获取分类效果最好的分类方式，包括分类阈值、属性值等
def buildStump(dataArr,classLabels,D):
    dataMatrix=np.mat(dataArr)#转化为二维矩阵，而且只适应于二维
    labelMat = np.mat(classLabels).T#矩阵的转置
    m,n = np.shape(dataMatrix)
    numSteps = 10.0#总步数
    bestStump={}#存储给定权重向量D时所得到的最佳单层决策树
    bestClasEst = np.mat(np.zeros((m,1)))
    minError = float('inf')#正无穷大
    for i in range(n):#第一层循环，进行两次循环，每次针对一个属性值
        #获取当前属性值的最大最小值
        rangeMin = dataMatrix[:,i].min();rangeMax = dataMatrix[:,i].max()
        stepSize = (rangeMax-rangeMin)/numSteps# 获取步长
        for j in range(-1,int(numSteps)+1):#从-1开始，
            #目的是解决小值标签为-1 还是大值标签为-1的问题
            for inequal in ['lt','gt']:#为什么要有这么一个循环？
                threshVal = (rangeMin+float(j)*stepSize)#从-1步开始，每走一步的值
                predictedVals = stumpClassify(dataMatrix,i,threshVal,inequal)#根据这个值进行数据分类
                errArr = np.mat(np.ones((m,1)))#创建错误向量，初始值为1
                errArr[predictedVals==labelMat]=0#若预测的值和真实值相同，则赋值为0
                weightedError = D.T*errArr#权重与错误向量相乘求和
               # print("split:dim %d, thresh %.2f,thresh inequal: %s,the weighted error is %.3f" %(i,threshVal,inequal,weightedError))
                if weightedError<minError:#此if语句在于获取最小的 错误权值
                    minError = weightedError
                    bestClasEst = predictedVals.copy()
                    bestStump['dim']=i
                    bestStump['thresh']=threshVal
                    bestStump['ineq'] = inequal
    return bestStump,minError,bestClasEst

#参数分别是 数据、数据分类标签、循环次数
def adaBoostTrainDS(dataArr,classLabels,numIt=40):
    weakClassArr = []
    m = np.shape(dataArr)[0]#获取数据个数
    D = np.mat(np.ones((m,1))/m)#初始化数据权值
    aggClassEst = np.mat(np.zeros((m,1)))#
    for i in range(numIt):#循环
        bestStump,error,classEst = buildStump(dataArr,classLabels,D)#寻找最优单层决策树
        print('D:',D.T)
        #该值是说明总分类器单层决策树输出结果的权重？
        #le-16 作用是保证没有除0溢出错误发生
        alpha = float(0.5*np.log((1.0-error)/max(error,1e-16)))#eN表示10的N次方
        print("alpha:",alpha)
        bestStump['alpha'] = alpha
        weakClassArr.append(bestStump)
        print("classEst:",classEst.T)
        expon = np.multiply(-1*alpha*np.mat(classLabels).T,classEst)
        D = np.multiply(D,np.exp(expon))
        D = D/D.sum()#用于计算下一次迭代中的新权重向量D
        aggClassEst +=alpha*classEst#类别估计值
        #sign 函数就是二值分类函数，大于0为1 小于0 为-1
        aggErrors = np.array((np.sign(aggClassEst)!=np.mat(classLabels).T)*1.0)
        # print("result:",result.sum()/m)
        # aggErrors = np.multiply(np.sign(aggClassEst)!=np.mat(classLabels).T,np.ones((m,1)))
        errorRate = aggErrors.sum()/m#计算错误率
        print("total error:",errorRate)
        if errorRate ==0.0:
            break
    return weakClassArr

    #数据的测试
def modeltest(testdata,testclasslabels,classifierArray):
    m = np.shape(testdata)[0]
    aggClassEst = np.mat(np.zeros((m,1)))
    for i in range(len(classifierArray)):
        classEst = stumpClassify(testdata,classifierArray[i]['dim'],classifierArray[i]['thresh'],
                                 classifierArray[i]['ineq'])
        aggClassEst+=classifierArray[i]['alpha']*classEst
        print(aggClassEst)
    result = np.sign(aggClassEst)
    accuracy = sum(((np.array(result).reshape(20,)==testclasslabels)*1.0))/len(testclasslabels)
    return accuracy
if __name__ == '__main__':
    dataMat,classLabels = loadSimpData()
    traindata = np.mat(dataMat[:80]);trainclasslabels = np.array(classLabels[:80])
    testdata = np.mat(dataMat[80:]);testclasslabels = np.array(classLabels[80:])
    classifierArray = adaBoostTrainDS(traindata,trainclasslabels,9)
    print("classifierArray:",classifierArray)
    accuracy = modeltest(testdata,testclasslabels,classifierArray)
    print("accuracy:",accuracy)