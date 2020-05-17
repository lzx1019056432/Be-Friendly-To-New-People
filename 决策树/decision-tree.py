# -*- coding:utf-8 -*-
'''
决策树
原理：
模拟我们人类判断问题使用决策的方式，通过树状图形进行做出分类

'''
import numpy as np
import ML.treePlotter as treePlotter
import pickle
import operator

#加载数据
def loadData(dataseturl):
    dataset = []
    with open(dataseturl) as f:
        dataall = f.readlines()
    for data in dataall:
        dataline = data.strip().split('\t')
        dataset.append(dataline)
    #age（年龄）、prescript（症状）、astigmatic（是否散光）、tearRate（流泪程度）
    labels=['age','prescript','astigmatic','tearRate']#四个属性
    return dataset,labels
#计算给定数据集的香农熵
def calShannonEnt(dataset):
    numEntries = len(dataset)
    labelCounts={}
    for data in dataset:
        classlabel = data[-1]
        if(classlabel not in labelCounts.keys()):
            labelCounts[classlabel]=0
        labelCounts[classlabel]+=1
    shannonEnt=0.0
    #print("labelCounts",labelCounts)
    for key in labelCounts:
        p = float(labelCounts[key])/numEntries
        shannonEnt-= p*np.log2(p)
    #print("shannoEnt:",shannonEnt)
    return shannonEnt

#根据某一特征，划分数据集
def splitDataset(dataset,axis,value):#axis 属性的位置 value 返回数据属性值为value
    retDataSet = []
    for featVec in dataset:
        if featVec[axis]==value:
            reducedFeatVec = featVec[:axis]
            reducedFeatVec.extend(featVec[axis+1:])
            retDataSet.append(reducedFeatVec)
   # print("划分数据集:",retDataSet)
    return retDataSet

#选择做好的数据集进行划分，返回值是特征位置
def chooseBestFeatureToSplit(dataset):
    numFeatures = len(dataset[0])-1 #计算特征数
    baseEntropy = calShannonEnt(dataset)#计算信息熵
    bestFeature = -1
    bestInfoGain = 0
    for i in range(numFeatures):#不断循环属性
        featList = [example[i] for example in dataset]#获取数据集的第i个特征
        uniqueVals = set(featList)#属性i的属性值有哪些
        #print("uniqueVals",uniqueVals)
        newEntropy = 0.0
        for value in uniqueVals:#
            subDataSet = splitDataset(dataset,i,value)#按照属性i和属性i的值value进行数据划分
            #print("subDataSet",subDataSet)
            prob = len(subDataSet)/float(len(dataset))
            #print("calShannonEnt(subDataSet):",calShannonEnt(subDataSet))
            newEntropy +=prob*calShannonEnt(subDataSet) #计算划分过数据集的信息熵
        infoGain = baseEntropy-newEntropy#计算信息增益，也就是信息熵的变换量
        #print("infogain",infoGain)
        if(infoGain>bestInfoGain):
            bestInfoGain = infoGain
            bestFeature=i
   # print("输出最好的属性",bestFeature)
    return bestFeature

# 若所有属性使用完毕后，类标签还无法统一，使用投票的方式进行统一
def majorityCnt(classList):
    classCount={ }
    #这个是个非常常用得手段，用于统计各个值得个数
    for vote in classList:
        if vote not in classCount.keys():
            classCount[vote]=0
        else:
            classCount[vote]+=1
    sortedClassCount = sorted(classCount.items(),key=operator.itemgetter(1),reverse=True)
    return sortedClassCount[0][0]

#创建树，通过递归函数进行构建
def createTree(dataset,labels):#数据集和标签列表
    classList =[example[-1] for example in dataset]#数据所属类得值
    if classList.count(classList[0])==len(classList):#条件1：classList只剩下一种值
        return classList[0]
    if len(dataset[0])==1:#条件2：数据dataset中属性已使用完毕，但没有分配完毕
        return majorityCnt(classList)#取数量多的作为分类
    bestFeat = chooseBestFeatureToSplit(dataset)#选择最好的分类点，即香农熵值最小的
    #print("bestFeat:",bestFeat)
    labels2 = labels.copy()#复制一分labels值，防止原数据被修改。
    bestFeatLabel = labels2[bestFeat]
    myTree = {bestFeatLabel:{}}#选取获取的最好的属性作为
    print("bestFeat:",bestFeat)
    # labels.pop(bestFeat)
    del(labels2[bestFeat])#这里写博客的时候，需要说一下关于list值得变化
    print("labels-id2:",id(labels2))
    featValues = [example[bestFeat] for example in dataset]#获取该属性下的几类值
    uniqueVals = set(featValues)
    for value in uniqueVals:
        subLabels = labels2[:]#剩余属性列表
        myTree[bestFeatLabel][value] = createTree(splitDataset(dataset,bestFeat,value),subLabels)
    return myTree
# 进行分类---通过递归方式对这颗树进行遍历，有点类似树的后序遍历
def classify(inputTree,featLabels,testVec):
    firstStr = list(inputTree.keys())[0]
    # print("firststr",firstStr)
    # print("featLabels",featLabels)
    secondDic = inputTree[firstStr]#获取最外层字典里的值
    featIndex = featLabels.index(firstStr)#获取最外层属性值在属性列表中的位置
    for key in secondDic.keys():
        if testVec[featIndex]==key:
            if isinstance(secondDic[key],dict):
                classLabel = classify(secondDic[key],featLabels,testVec)
            else:
                classLabel = secondDic[key]

    return classLabel

#存储树---以二进制序列化进行存储
def storeTree(inputTree,filename):
    fw = open(filename,'wb')
    #这里pickle可以稍微详细说一下
    pickle.dump(inputTree,fw)
    fw.close()

#加载存储的树  以二进制返回加载的序列化值
def grabTree(filename):
    fr = open(filename,'rb')
    return pickle.load(fr)

if __name__ == '__main__':
    mydat,labels = loadData('datasets/lenses.txt')
    print("labels-id1:",id(labels))
    print("output:",labels)
    mytree = createTree(mydat,labels)
    print("输出mytree:",mytree)
    # filename = 'testdata.txt'
    # storeTree(mytree,filename)
    # tree = grabTree(filename)
    # print("加载过来的tree:",tree)
    # print("输出mytree的key:",list(mytree.keys())[0])
    treePlotter.createPlot(mytree)#绘画决策树
    # print("pre-ouput:",labels)
    classlabel = classify(mytree,labels,['young','hyper','yes','reduced'])#验证分类
    print(classlabel)