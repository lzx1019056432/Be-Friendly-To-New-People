import numpy as np
import matplotlib.pyplot as plt
'''
项目介绍：
    此项目是使用numpy搭建神经网络模型，预测波士顿房价。
数据介绍：
    每一条房屋数据有14个值，前13个值是房屋属性，比如面积，长度等，最后一个是房屋价格,共506条数据。
    
此项目使用SGD随机梯度下降
'''
#数据导入以及处理
def deal_data():
    #读取文件数据，此时数据形状是(7084,)，即所有数据在一行中
    housingdata = np.fromfile('data/housing.data',sep=' ')

    #修改数据格式，将每一条房屋数据放在一行中。
    housingdata = np.array(housingdata).reshape((-1,14))#此时数据形状为(506,14)

    #对数据的前13个属性进行归一化操作，有助于提高模型精准度，这里使用max-min归一化方式。公式为(x-min)/(max-min)
    for i in range(13):
        Max =  np.max(housingdata[:,i])
        Min = np.min(housingdata[:,i])
        housingdata[:,i]=(housingdata[:,i]-Min)/(Max-Min)

    #依据2-8原则，80%的数据作为训练数据，20%数据作为测试数据。
    Splitdata = round(len(housingdata)*0.8)
    Train = housingdata[:Splitdata]#训练数据集
    Test = housingdata[Splitdata:]#测试数据集
    return Train,Test

#模型设计以及配置
#首先确定有13个权值参数w，并随机初始化
class Model_Config(object):
    def __init__(self,num):
        np.random.seed(1)
        self.w = np.random.randn(num,1)
        self.b =0
     #计算预测值
    def forward(self,x):
        y = np.dot(x,self.w)
        return y
    #设置损失函数,这里使用差平方损失函数计算方式
    def loss(self,z,y):
        error = z-y
        cost = error*error
        avg_cost = np.mean(cost)
        return avg_cost
    #计算梯度
    def back(self,x,y):
        z = self.forward(x)
        gradient_w = (z-y)*x
        gradient_w = np.mean(gradient_w,axis=0)#这里注意，axis=0必须写上，否则默认将这个数组变成一维的求平均
        gradient_w = gradient_w[:,np.newaxis]#这里注意写博客--增加一个维度
        gradient_b = (z-y)
        gradient_b = np.mean(gradient_b)
        return gradient_w,gradient_b

    #使用梯度更新权值参数w
    def update(self,gradient_w,gradient_b,learning_rate):
        self.w = self.w-learning_rate*gradient_w
        self.b = self.b-learning_rate*gradient_b

    #开始训练
    def train(self,epoch_num,train_data,learning_rate,batch_size):
        #循环迭代
        losses=[]
        for i in range(epoch_num):
            np.random.shuffle(train_data)
            mini_batches = [train_data[i:i+batch_size] for i in range(0,len(train_data),batch_size)]
            for batch_id,data in enumerate(mini_batches):
                x = data[:,:-1]
                y = data[:,-1:]
                z = self.forward(x)
                avg_loss = self.loss(z,y)
                gradient_w,gradient_b = self.back(x,y)
                self.update(gradient_w,gradient_b,learning_rate)
                losses.append(avg_loss)
                #每进行20此迭代，显示一下当前的损失值
                if(i%10==0):
                    print("epoch_num:{},batch_id:{},loss:{}".format(i,batch_id,avg_loss))

        return losses
def showpeocess(loss):
    plt.title("The Process Of Train")
    plt.plot([i for i in range(len(loss))],loss)
    plt.xlabel("epoch_num")
    plt.ylabel("loss")
    plt.show()
if __name__ == '__main__':
    Train,Test = deal_data()
    epoch_num = 200#设置迭代次数
    batch_size=50#每50个组成一个批次
    Model = Model_Config(13)
    losses = Model.train(epoch_num=epoch_num,batch_size=batch_size,train_data=Train,learning_rate=0.001)
    showpeocess(loss=losses)


