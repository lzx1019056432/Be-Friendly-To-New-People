# -*- coding:utf-8 -*-
'''
《机器学习实战》之KNN算法源码
原理：
通过计算数据之间的欧几里得距离，来判定新数据的所属关系。
步骤：
1.计算新的数据与各个原数据的欧几里得距离
2. 按照升序排列，选择前K个数据
3. 统计K个数据所属于的类，计算概率值
4. 概率最大的即为新数据所属的类。

数据集：
这里使用了书中提供的数据集，共包含4列，前三列对应着三个属性，分别是飞行里程数、玩游戏时间占比、消耗冰淇淋公升数

最后一列是数据所属分类1、2、3
'''
import numpy as np
import operator
#加载数据
def loaddatasets(dataseturl,datatype='train'):
    datasetLabel = []
    datasetClass = []
    with open(dataseturl) as f:
        datas = f.readlines()
    for data in datas:
        dataline = data.strip().split('\t')
        datasetLabel.append(dataline[:-1])
        datasetClass.append(dataline[-1])
    if(type=='train'):
        datasetLabel = datasetLabel[:900]
        datasetClass = datasetClass[:900]
    else:
        datasetLabel = datasetLabel[900:]
        datasetClass = datasetClass[900:]
    return datasetLabel,datasetClass
## 数据归一化
def normalized_dataset(dataset):
    dataset = np.array(dataset,dtype='float')
    max = np.max(dataset,axis=0)
    min = np.min(dataset,axis=0)
    result = (dataset-min)/(max-min)
    return result,max,min
## 计算欧几里得距离
def calculate_distance(dataset,x):
    #此时算出了新数据x与原来每个数据之间的距离
    result = np.sqrt(np.sum(np.power((dataset-x),2),axis=1))
    #返回值是形状为(length,1)的数组
    return result
## 进行分类
def KnnClassify(k,inputdata,datasetLabel,datasetClass):
    # print(result)
    distance = calculate_distance(datasetLabel,inputdata)
    sortdistanceindex = np.argsort(distance)
    #print("sortdistanceindex",sortdistanceindex)
    classcount={ }
    for i in range(k):
        klist=datasetClass[sortdistanceindex[i]]
        classcount[klist] = classcount.get(klist,0)+1
    #这里需要记录一下，如何对字典中某一属性进行排序
    sortedClassCount = sorted(classcount.items(),key=operator.itemgetter(1),reverse=True)
    #print("sortedClassCount:",sortedClassCount)
    return sortedClassCount[0][0]
# 检测模型精度，使用百分之10的数据
def TestModelPrecision():
    dataseturl = 'datasets/datingTestSet2.txt'
    datatestLabel,datatestClass = loaddatasets(dataseturl,datatype='test')
    datamodelLabel,datamodelClass = loaddatasets(dataseturl,datatype='train')
    datatestLabel,_ ,_ = normalized_dataset(datatestLabel)
    datamodelLabel,_,_ = normalized_dataset(datamodelLabel)
    #print("normalize:",datasetLabel)
    num=0
    for i in range(len(datatestClass)):
        DataClass = KnnClassify(k=3,inputdata=datatestLabel[i],datasetLabel=datamodelLabel,datasetClass=datamodelClass)
        print("当前预测所属类为{},实际所属类为{}".format(DataClass,datatestClass[i]))
        if(int(DataClass)==int(datatestClass[i])):
            num+=1
    return 100*num/len(datatestClass)
# 输入数据进行分类
def ClassifyResult():
    data1 = input("请输入飞行里程数:")
    data2 = input("请输入玩游戏时间占比:")
    data3 = input("请输入消耗得冰淇淋公升数:")
    dataseturl = 'datasets/datingTestSet2.txt'
    datamodelLabel,datamodelClass = loaddatasets(dataseturl,datatype='train')
    datamodelLabel,max,min = normalized_dataset(datamodelLabel)
    inputdata = np.array([data1,data2,data3],dtype='float')
    inputdata = (inputdata-min)/(max-min)#处理输入的数据
    DataClass = KnnClassify(k=3,inputdata=inputdata,datasetLabel=datamodelLabel,datasetClass=datamodelClass)
    print("输出结果是:",DataClass)
if __name__ == '__main__':
    accuracy = TestModelPrecision()
    print("模型精准度为:{}%".format(accuracy))
    ClassifyResult()