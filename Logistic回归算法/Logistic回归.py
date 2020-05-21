# -*- coding:utf-8 -*-
'''
逻辑回归算法解决分类问题
使用的是数据集共有三列数据，前两列是属性，最后一列是所属类
数据总数一共有100条
这里我们使用梯度下降的方法进行优化参数
由于数据集不多，这里采用一般的梯度下降方法

这里共设置3个参数 w0是常数项，w1中对应着两个属性的参数
'''
import numpy as np
import random
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif']=['SimHei']#这两句作用为防止中文乱码
plt.rcParams['axes.unicode_minus']=False
def loaddata(filename):
    data = np.loadtxt(filename)
    dataset = []
    for i in range(len(data)):
        dataset.append([1,data[i,0],data[i,1],data[i,2]])
    return np.array(dataset)
#创建逻辑回归类
def Sigmoid(x):
    return (1/(1+np.exp(-x)))
class Logistic:
    def __init__(self):
        self.w = np.ones(shape=(3,))#初始化 表示一维数组，共有三个元素


    def train(self,dataset,epoch=50,a=0.001):
        y = dataset[:,-1]#(80,1)
        print("shape(y)",np.shape(y))
        data = dataset[:,:-1]#(80,3)
        print("shape(data)",np.shape(data))
        print("shape(self.w)",np.shape(self.w),self.w)
        for i in range(epoch):
            h = Sigmoid(np.matmul(data,self.w))
            error = h-y#(80,1)
            self.w = self.w-a*np.matmul(data.T,error)
            # if(i!=0 and i%50==0):
            #     self.showimg(dataset,i)
        self.showimg(dataset,i+1)
    def test(self,dataset):
        y = dataset[:,-1]
        data = dataset[:,:-1]
        h = Sigmoid(np.matmul(data,self.w))
        h[h>0.5]=1
        h[h<0.5]=0
        result = h
        error=0
        for i in range(len(result)):
            if(result[i]!=y[i]):
                error+=1
        print(" the error is {}%:".format(100*error/float(len(result))))

    def showimg(self,dataset,i):
        x = np.arange(-3.0,3.0,0.1)
        x2 = (-self.w[0]-x*self.w[1])/self.w[2]
        plt.scatter([dataset[dataset[:,-1]==0][:,1]],[dataset[dataset[:,-1]==0][:,2]],color='',marker='o',edgecolors='green',linewidths=3)
        plt.scatter([dataset[dataset[:,-1]==1][:,1]],[dataset[dataset[:,-1]==1][:,2]],color='',marker='o',edgecolors='red',linewidths=3)
        plt.plot(x,x2)
        plt.title("迭代第{}次".format(i))
        # plt.savefig('datasets/img{}.png'.format(i))
        plt.show()

if __name__ == '__main__':
    filename="datasets/logisticdata.txt"
    dataset = loaddata(filename)
    print(np.shape(dataset))
    traindata = dataset[:80]
    testdata = dataset[80:]
    print(len(traindata))
    logistic = Logistic()
    logistic.train(dataset,epoch=500)
    logistic.test(testdata)
    # logistic.showimg(dataset)
