# -*- coding:utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
'''
作者：梁先森
CSDN主页：https://blog.csdn.net/lzx159951
Github主页：https://github.com/lzx1019056432

'''
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
    spotstyle=['ro','go','yo','bo','po']
    scattercolor=['red','green','yellow','blue','pink']
    for i in range(len(clusterAssment)):
        if i not in Index1:
            Index2.append(i)
    for i in range(len(centroids)):
        Index1 = np.nonzero(clusterAssment[:,0]==i)[0]
        plt.plot(datamat[Index1,0],datamat[Index1,1],spotstyle[i])
        plt.scatter([centroids[i][0]],[centroids[i][1]],color='',marker='o',edgecolors=scattercolor[i],linewidths=3)
    plt.show()
def randCent(dataSet,k):
    n = np.shape(dataSet)[1]#获取维度数
    centroids = np.array(np.zeros((n,2)))#创建一个k*n的矩阵，初始值为0
    print(centroids)
    for j in range(n):
        minJ = np.min(dataSet[:,j])#获取每一维度的最小值
        rangeJ = float(np.max(dataSet[:,j])-minJ)#获得最大间隔，最大值➖最小值
        #print("test2:",centroids[:,j])
        centroids[:,j] = np.array(minJ+rangeJ*np.random.rand(k,1)).reshape(2)#最小值加上间隔*[0,1]范围的数
        #print("test3:",centroids[:,j])
        #每进行一次循环，给每一整列赋值。
    return centroids

def kMeans(dataSet,k,distMeans=distEclud,createCent = randCent):
    m = np.shape(dataSet)[0]#获取数据的个数
    clusterAssment = np.array(np.zeros((m,2)))#创建一个m行2列的数组用于存储索引值和距离
    centroids = createCent(dataSet,k)#随机选取两个点
    print("初始化的矩阵",centroids)
    # plt.scatter([centroids[0][0]],[centroids[0][1]],color='',marker='o',edgecolors='red',linewidths=3)
    # plt.scatter([centroids[1][0]],[centroids[1][1]],color='',marker='o',edgecolors='green',linewidths=3)
    # plt.plot(dataSet[:,0],dataSet[:,1],'o',color='yellow')
    # plt.show()
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
            ptsInClust = dataSet[np.nonzero(clusterAssment[:,0]==cent)[0]]#取出相同簇的点进行取平均，这里[0]是因为参数的形状为(n,1)
            #np.nonzero 取值不为0的索引值
            centroids[cent,:] = np.mean(ptsInClust,axis=0)#取平均
        #showProcess(clusterAssment,centroids)
    return centroids,clusterAssment

def biKmeans(dataSet,k,distMeans=distEclud):
    m = np.shape(dataSet)[0]
    clusterAssment =np.array(np.zeros((m,2)))#初始化一个形状为m*2的数组
    centroid0 = np.mean(dataSet,axis=0).tolist()[0]#这里获取已求平均的x、y值
    # print(np.mean(dataSet,axis=0))输出形状为：[[1.51081424 1.55366839]]
    centList = [centroid0]#这里放置的是划分簇的中心点
    #print("cenlist:",np.shape(centList))
    for j in range(m):#m次循环，计算每个数据与中心点的距离。这里多了个平方，目的是增加对距离远的数据的敏感度
        clusterAssment[j,1] = distMeans(np.mat(centroid0),dataSet[j,:])**2
    while(len(centList)<k):#结束循环条件，满足条件的中心点数等于K值
        lowestSSE = 100000#初始化一个最大值
        for i in range(len(centList)):#循环每一个中心点
            #这里是取出属于第i类的点数据
            ptsInCurrCluster = dataSet[np.nonzero(clusterAssment[:,0]==i)[0],:]
            #通过k-mean  将当前类的数据集进行2分类
            centroidMat,splitClustAss = kMeans(ptsInCurrCluster,2,distMeans)
            #计算分类后所有数据的距离值（误差值）
            sseSplit = np.sum(splitClustAss[:,1])
            #计算除了该类剩余数据的误差值
            sseNotSplit = np.sum(clusterAssment[np.nonzero(clusterAssment[:,0]!=i)[0],1])
            print("sseSplit,and notSplit:",sseSplit,sseNotSplit)
            #进行比较，若分类之后损失值小于lowestSSE，则可分
            if(sseSplit+sseNotSplit)<lowestSSE:
                bestCentToSplit = i
                bestNewCents = centroidMat#经过k-mean计算出的两个簇点
                bestClustAss = splitClustAss.copy()#拷贝一份经过k-mean计算的数据所属关系
                lowestSSE = sseSplit+sseNotSplit#总的损失值大小
                #对当前已经经过k-mean计算的数据进行重新分类
                #将类型==1的分给最大长度，因为是从0开始计算的，所以不用＋1.
                bestClustAss[np.nonzero(bestClustAss[:,0]==1)[0],0]=len(centList)
                #等于0的还是分配原来的。
                bestClustAss[np.nonzero(bestClustAss[:,0]==0)[0],0]=bestCentToSplit
                #此时bestClustAss 数组中存储的是经过2分之后的数据标签归属和误差值
                print("the bestCentTopSplit is:",bestCentToSplit)
                print("the len of bestClustAss is :",len(bestClustAss))
        #簇点进行替换
        centList[bestCentToSplit] = bestNewCents[0,:]
        print("step1:",np.shape(centList))
        #产生的新的簇点加在列表后面
        centList.append(bestNewCents[1,:])
        print("step2:",np.shape(centList))
        #直接将上面分好的数据标签归属进行替换
        #print("ttest---:",clusterAssment[[1,2,3,4,5],:])允许这样的数据访问形式。
        clusterAssment[np.nonzero(clusterAssment[:,0]==bestCentToSplit)[0],:] = bestClustAss
    return centList,clusterAssment
if __name__ == '__main__':
    datamat = np.array(loadDateSet('data.txt'))
    centList,clusterAssment =  biKmeans(datamat,3)
    showProcess(clusterAssment,centList)