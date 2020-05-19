# -*- coding:utf-8 -*-
'''
此项目参考与《机器学习实战》---朴素贝叶斯分类器区分垃圾邮件
步骤：
1. 处理邮件，将单词分割放入到列表中
2. 统计不同单词个数
3. 分割训练集和测试集数据，并转化为词向量
4. 对训练集数据，计算单词出现概率
5. 对测试集的词向量数据进行贝叶斯公式计算
6. 比较两个贝叶斯公式计算结果，较大的为数据所属类

'''
import re
import numpy as np
import random
#使用正则表达式，按照除数字、字母、下划线之外的字符进行单词划分
def textParse(text):
    text1 = re.split(r'\W+',text)
    text2 = [textfilter.lower() for textfilter in text1 if len(textfilter)>2]#返回字符长度大于2的字符
    # to do -这里可以添加自定义过滤字符串的规则
    return text2

#加载数据
def loadDataSet():
    fileurl1 = 'datasets/email/ham'
    fileurl2 = 'datasets/email/spam'#垃圾邮件
    postingList=[]
    classVec = []
    fulltext=[]
    for i in range(1,26):
        f1 = open(fileurl1+'/{}.txt'.format(i),errors='ignore')
        text1 = textParse(f1.read())
        postingList.append(text1)
        fulltext.extend(text1)
        classVec.append(1)
        f2 = open(fileurl2+'/{}.txt'.format(i),'r')
        text2 = textParse(f2.read())
        postingList.append(text2)
        fulltext.extend(text2)
        classVec.append(0)
    return postingList,classVec,fulltext


#创建词向量
def setOfWords2Vec(vocabList,inputSet):
    returnVec = [0]*len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)]+=1
        else:
            print("the word is not in my vocabulary:",word)
    return returnVec

#训练函数
def trainNB0(trainMatrix,trainCategory):
    #print("trainMatrix",trainMatrix)
    numTrainDocs = len(trainMatrix)#共有几个文本
    numWords = len(trainMatrix[0])#共有多少单词
    pAbusive = sum(trainCategory)/float(numTrainDocs)#文本中有多少是侮辱性文档
    p0Num = np.ones(numWords)#
    p1Num = np.ones(numWords)
    p0Denom = 1.0*numWords
    p1Denom = 1.0*numWords
    for i in range(numTrainDocs):
        print("trainCategory[i]",trainCategory[i])
        if trainCategory[i]==1:#文档的分类
            p1Num+=trainMatrix[i]#计算每个单词出现的次数
            p1Denom+=sum(trainMatrix[i])#统计文档类型属于1的所有文档单词个数
        else:
            p0Num+=trainMatrix[i]
            p0Denom+=sum(trainMatrix[i])
    #print("p1Denom:{},p0Denom:{}".format(p1Denom,p0Denom))
    #print("p1Num:{},p0Num:{}".format(p1Num,p0Num))
    p1Vect = np.log(p1Num/p1Denom)
    p0Vect = np.log(p0Num/p0Denom)
    return p0Vect,p1Vect,pAbusive

#分类函数
def classifyNB(vec2Classify,p0Vec,p1Vec,pClass1):
    p0 = np.sum(vec2Classify*p0Vec)+np.log(pClass1)
    p1 = np.sum(vec2Classify*p1Vec)+np.log(1.0-pClass1)
    if p1>p0:
        return 1
    else:
        return 0

#测试函数
def testingNB():
    listOPosts,listClasses,fulltext = loadDataSet()
    # myVocabList = createVocabList(listOPosts)
    myVocabList = list(set(fulltext))
    #print("单词列表:",myVocabList)
    #随机取10个邮件作为测试使用
    #print("listOPosts.length:",len(listOPosts))
    trainsetnum = list(range(50))
    testset = []
    for i in range(10):
        index = int(random.uniform(0,len(trainsetnum)))
        testset.append(trainsetnum[index])
        del(trainsetnum[index])
    print("testset:",testset)
    #重新组装训练数据和测试数据
    traindata = []
    trainclass=[]
    for j in trainsetnum:
        traindata.append(setOfWords2Vec(myVocabList,listOPosts[j]))#这里直接转化为词向量
        trainclass.append(listClasses[j])
    testdata=[]
    testclass=[]
    for k in testset:
        testdata.append(setOfWords2Vec(myVocabList,listOPosts[k]))
        testclass.append(listClasses[k])
    p0V,p1V,pSpam = trainNB0(traindata,trainclass)
    errorcount=0
    for i in range(len(testdata)):
        wordVector = testdata[i]
        print("输出最终分类结果:",classifyNB(wordVector,p0V,p1V,pSpam))
        print("输出原本结果-:",testclass[i])
        if testclass[i]!=classifyNB(wordVector,p0V,p1V,pSpam):
            errorcount+=1
    print(" the error rate is:{}".format(errorcount))


if __name__ == '__main__':
    testingNB()