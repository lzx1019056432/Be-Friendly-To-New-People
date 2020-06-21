# -*- coding:utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
def loadSimpData():
    dataMat = []
    labelMat = []
    data = open('datasets/testSet.txt')
    for dataline in data.readlines():
        linedata = dataline.split('\t')
        dataMat.append([float(linedata[0]),float(linedata[1])])
        labelMat.append(float(linedata[2].replace('\n','')))
    return dataMat,labelMat

def plotROC(predStrengths,classLabels):
    #predStrengths = np.fabs(predStrengths)
    # print("predStrengths:",predStrengths[0])
    # print("sorted(predStrengths):",sorted(list(predStrengths[0])))
    cur = (0.0,0.0)
    ySum = 0.0
    numPosClas = np.sum(np.array(classLabels)==1.0)
    yStep = 1/float(numPosClas)
    xStep = 1/float(len(classLabels)-numPosClas)
    sortedIndicies = list(predStrengths.argsort())
    sortedIndicies.sort(reverse=True)
    fig = plt.figure()
    fig.clf()
    ax = fig.add_subplot(111)
    for index in sortedIndicies:
        if classLabels[index]==1:
            addX = 0
            addY = yStep
        else:
            addX = xStep
            addY=0
            ySum+=cur[1]
        # print("[cur[0],cur[0]-delX]:",[cur[0],cur[0]-delX])
        # print("[cur[1],cur[1]-delY]:",[cur[1],cur[1]-delY])
        ax.plot([cur[0],cur[0]+addX],[cur[1],cur[1]+addY],c='r')#[1,1],[1,]
        print("ystep,xstep",yStep,xStep)
        cur = (cur[0]+addX,cur[1]+addY)
    ax.plot([0,1],[0,1],'b--')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Roc curve for AdaBoost Horse Colic Detection System')
    #ax.axis([0,1,0,1])
    plt.show()
    print('the Area Under the Curve is :',ySum*xStep)

if __name__ == '__main__':
    dataMat,classLabels = loadSimpData()
    traindata = np.mat(dataMat[:80]);trainclasslabels = np.array(classLabels[:80])
    predStrengths = np.array([i/10 for i in range(1,80)])
    plotROC(predStrengths,trainclasslabels)

