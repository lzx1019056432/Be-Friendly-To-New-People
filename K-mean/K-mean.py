import numpy as np
import matplotlib.pyplot as plt
def CreatData():
    x1 = np.random.rand(50)*3#0-3
    y1 = [i+np.random.rand()*2-1 for i in x1]
    with open('data.txt','w') as f:
        for i in range(len(x1)):
            f.write(str(x1[i])+'\t'+str(y1[i])+'\n')
def loadDateSet(fileName):
    dataMat=[]
    fr = open(fileName)
    for line in fr.readlines():
        curline = line.strip().split('\t')
        #map函数 对指定的序列做映射，第一个参数是function 第二个是序列
        #此方法可以理解为进行字符串格式转换.这个函数可以深究
        #print(curline)
        #fltLine = float(curline)
        fltLine = map(float,curline)
        dataMat.append(list(fltLine))
    return dataMat

def distEclud(vecA,vecB):
    return np.sqrt(np.sum(np.power((vecA-vecB),2)))
def showProcess(clusterAssment,centroids):
    #显示过程
    Index1 = np.nonzero(clusterAssment[:,0]==0)[0]
    Index2 = []
    for i in range(len(clusterAssment)):
        if i not in Index1:
            Index2.append(i)
    plt.plot(datamat[Index1,0],datamat[Index1,1],'ro')
    plt.plot(datamat[Index2,0],datamat[Index2,1],'go')
    plt.scatter([centroids[0,0]],[centroids[0,1]],color='',marker='o',edgecolors='red',linewidths=3)
    plt.scatter([centroids[1,0]],[centroids[1,1]],color='',marker='o',edgecolors='green',linewidths=3)
    plt.show()
def randCent(dataSet,k):
    n = np.shape(dataSet)[1]#获取维度数
    centroids = np.mat(np.zeros((k,n)))#创建一个k*n的矩阵，初始值为0
    for j in range(n):
        minJ = np.min(dataSet[:,j])#获取每一维度的最小值
        rangeJ = float(np.max(dataSet[:,j])-minJ)#获得最大间隔，最大值➖最小值
        centroids[:,j] = minJ+rangeJ*np.random.rand(k,1)#最小值加上间隔*[0,1]范围的数
        #每进行一次循环，给每一整列赋值。
    return centroids

def kMeans(dataSet,k,distMeans=distEclud,createCent = randCent):
    m = np.shape(dataSet)[0]#获取数据的个数
    clusterAssment = np.mat(np.zeros((m,2)))#创建一个m行2列的矩阵用于存储索引值和距离
    centroids = createCent(dataSet,k)#随机选取两个点
    plt.scatter([centroids[0,0]],[centroids[0,1]],color='',marker='o',edgecolors='red',linewidths=3)
    plt.scatter([centroids[1,0]],[centroids[1,1]],color='',marker='o',edgecolors='green',linewidths=3)
    plt.plot(dataSet[:,0],dataSet[:,1],'o',color='yellow')
    plt.show()
    clusterChanged = True#标志符，判定数据点的所属关系有没有发生变化
    flag=1
    while clusterChanged:
        print("当前迭代次数为：{}".format(flag))
        flag+=1
        clusterChanged=False
        for i in range(m):#m为数据量的个数
            minDist = 10000#设置一个最大值
            minIndex = -1#初始化索引
            for j in range(k):#k为划分的种类数 此for循环给数据点分配所属关系
                distJI = distMeans(centroids[j,:],dataSet[i,:])#距离值
                if distJI<minDist:
                    minDist = distJI
                    minIndex = j
            if clusterAssment[i,0]!=minIndex:#判断所属关系是否发生改变
                clusterChanged=True
            clusterAssment[i,:] = minIndex,minDist**2#这里面存储的是所属关系和序列号
        #print(centroids)
        for cent in range(k):#这个for循环是用来移动分类点的位置，将其移动到所属点的平均值位置
            # print("输出1：",clusterAssment[:,0])
            # print("输出2：",np.nonzero(clusterAssment[:,0].A==cent))
            #.A 是将矩阵转化为数组
            ptsInClust = dataSet[np.nonzero(clusterAssment[:,0].A==cent)[0]]#取出相同簇的点进行取平均，这里[0]是因为参数的形状为(n,1)
            #np.nonzero 取值不为0的索引值
            centroids[cent,:] = np.mean(ptsInClust,axis=0)#取平均
        showProcess(clusterAssment,centroids)
    return centroids,clusterAssment

if __name__ == '__main__':
    datamat = np.mat(loadDateSet('data.txt'))
    centroids,clusterAssment = kMeans(datamat,2)
