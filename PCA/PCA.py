# -*- coding:utf-8 -*-
'''
PCA 主成分分析
步骤：
1.将原始数据按列组成n行m列矩阵X
2. 将X的每一行进行零均值化，即减去这一行的值
3.求出协方差矩阵C=1/mXXT
4. 求出协方差矩阵的特征值及对应的特征向量
5. 将特征向量按对应特征值大小从上到下按行排成矩阵，取前K行组成矩阵P
6. Y=PX即为降维到K维后的数据

注：
这里的数据格式为  行代表数据，列代表属性。这个与之前看的资料正好相反，不过影响不大。
'''
import numpy as np
import matplotlib.pyplot as plt
#加载数据，输出为矩阵形式
def loadDateSet(filename,delim='\t'):
    with open(filename,'r')as f:
        stringarr = [line.strip().split(delim) for line in f.readlines()]
        datarr = [list(map(float,line)) for line in stringarr]
    return np.mat(datarr)

def pca(dataMat,topNfeat=999):
    meanVals = np.mean(dataMat,axis=0)#计算每一个属性的均值
    meanRemoved = dataMat-meanVals#将数据进行零均值化
    covMat = np.cov(meanRemoved,rowvar=False)#计算协方差矩阵，rowvar=False 表示属性在列，数据在行
    eigVals,eigVects = np.linalg.eig(np.mat(covMat))#计算矩阵的特征值和特征向量
    #print("特征值：",eigVals)
    #print("特征向量：",eigVects)
    eigValInd = np.argsort(eigVals)#将特征值进行排序,按照从小到大的顺序，返回索引值
    #print("排序后的特征值：",eigValInd)
    #这里就是取前K个最大值
    eigValInd = eigValInd[:-(topNfeat+1):-1] #这里使用了切片，只取前K个最大的索引，这里我们K=1
    #print("eigValInd:",eigValInd)
    redEigVects = eigVects[:,eigValInd] #取特征值对应的特征向量
    #print("redEigVects",redEigVects)
    #Y=XP
    lowDDataMat = meanRemoved*redEigVects #零均值的数据与 特征向量做相乘 结果为Y,降维后的数据
    #redEigVects.T  为对redEigVects 进行转置
    #这里为何能还原呢，是因为P是特征向量，特征向量P*其转置=E so XP*PT=X
    reconMat = (lowDDataMat*redEigVects.T)+meanVals #数据还原
    return lowDDataMat,reconMat

if __name__ == '__main__':
    datamat = loadDateSet('data.txt')
    lowDDataMat,reconmat = pca(datamat,1)
    print("原数据：\n",reconmat)
    print("降维后的数据：\n",lowDDataMat)