# -*- coding:utf-8 -*-
'''
此模块为决策树图的绘画


'''
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif']=['SimHei']#这两句作用为防止中文乱码
plt.rcParams['axes.unicode_minus']=False

decisionNode = dict(boxstyle="sawtooth",fc="0.8")#定义结点形状
leafNode = dict(boxstyle="round4",fc="0.8")#显示叶子的形状
arrow_args = dict(arrowstyle="<-")#定义箭头属性

#这里有涉及万物皆对象
#使用注释工具进行绘制
#参数分别是 注释文字、箭头位置、源位置、注释的文字外框形状属性
def plotNode(nodeTxt,centerPt,parentPt,nodeType):
    createPlot.ax1.annotate(nodeTxt,xy=parentPt,xycoords='axes fraction',\
                            xytext=centerPt,textcoords='axes fraction',\
                            va="center",ha="center",bbox=nodeType,arrowprops=arrow_args)


#获得树的叶子数
def getNumLeafs(myTree):
    numLeafs=0
    firstStr = list(myTree.keys())[0]
    secondDict = myTree[firstStr]
    for key in secondDict.keys():
        if isinstance(secondDict[key],dict):
            numLeafs+=getNumLeafs(secondDict[key])
        else:
            numLeafs+=1
    return numLeafs

#获得树的深度
def getTreeDepth(myTree):
    maxDepth = 0
    firstStr = list(myTree.keys())[0]
    secondDict = myTree[firstStr]
    for key in secondDict.keys():
        if isinstance(secondDict[key],dict):
            thisDepth = 1+getTreeDepth(secondDict[key])
        else:
            thisDepth=1
        if thisDepth>maxDepth:maxDepth=thisDepth
    return maxDepth

# 在父子结点之间填充文本信息
def plotMidText(cntrPt,parentPt,txtString):#参数分别是当前
    xMid = (parentPt[0]-cntrPt[0])/2.0+cntrPt[0]
    yMid = (parentPt[1]-cntrPt[1])/2.0+cntrPt[1]
    createPlot.ax1.text(xMid,yMid,txtString)

# 绘制树
def plotTree(myTree,parentPt,nodeTxt):
    numLeafs = getNumLeafs(myTree)
    depth = getTreeDepth(myTree)
    fitstStr = list(myTree.keys())[0]
    cntrPt = (plotTree.x0ff+(1.0+float(numLeafs))/2.0/plotTree.totalW,plotTree.y0ff)
    plotMidText(cntrPt,parentPt,nodeTxt)
    plotNode(fitstStr,cntrPt,parentPt,decisionNode)
    secondDict = myTree[fitstStr]
    plotTree.y0ff = plotTree.y0ff-1.0/plotTree.totalD
    for key in secondDict.keys():
        if isinstance(secondDict[key],dict):
            plotTree(secondDict[key],cntrPt,str(key))
        else:
            plotTree.x0ff = plotTree.x0ff+1.0/plotTree.totalW
            plotNode(secondDict[key],(plotTree.x0ff,plotTree.y0ff),cntrPt,leafNode)
            plotMidText((plotTree.x0ff,plotTree.y0ff),cntrPt,str(key))
    plotTree.y0ff = plotTree.y0ff+1.0/plotTree.totalD

def createPlot(inTree):
    fig = plt.figure(1,facecolor='white')
    fig.clf()
    axprops = dict(xticks=[],yticks=[])#定义一个参数字典
    createPlot.ax1 = plt.subplot(111,frameon=False,**axprops)
    plotTree.totalW = float(getNumLeafs(inTree))
    plotTree.totalD = float(getTreeDepth(inTree))
    plotTree.x0ff = -0.5/plotTree.totalW
    plotTree.y0ff=1.0
    plotTree(inTree,(0.5,1.0),' ')
    plt.show()
