## 决策树代码


### 依赖环境

python3.7

### python库

numpy 

matplotlib

### 下载安装

```
git clone https://github.com/lzx1019056432/Be-Friendly-To-New-People.git
```

### 安装依赖包

```
cd 决策树
pip install -r requirements.txt
```
### 文件介绍
* datasets 为数据文件
* decision-tree.py 为决策树主函数文件
* treePlotter.py 使用matplotlib绘画决策树

### 使用方法

在当前目录下输入

```
cd 决策树
```

运行决策树算法

```
python decision-tree.py
```

## 决策树格式

决策树产生字典的字典形式为：

```
{'tearRate': {'reduced': 'no lenses', 'normal': {'astigmatic': {'no': {'age': {'presbyopic': {'prescript': {'hyper': 'soft', 'myope': 'no lenses'}}, 'young': 'soft', 'pre': 'soft'}}, 'yes': {'prescript': {'hyper': {'age': {'presbyopic': 'no lenses', 'young': 'hard', 'pre': 'no lenses'}}, 'myope': 'hard'}}}}}}
```

决策树图形表示：

![20200517121438425.png](https://img-blog.csdnimg.cn/20200517121438425.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2x6eDE1OTk1MQ==,size_16,color_FFFFFF,t_70#pic_center)

### 技术博客地址

* [决策树代码实战](https://blog.csdn.net/lzx159951/article/details/106172243)

