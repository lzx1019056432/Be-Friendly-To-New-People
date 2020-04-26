## GeneratorGIF-and-SeparateGIF
此项目是GIF图片的生成和GIF图片的分离。

![img](https://img-blog.csdnimg.cn/20200426104251951.gif)

​																生成样例图

### 依赖环境

python 3.7

### python 库

numpy--图片格式操作

pillow--图片操作

imageio--图片相关操作

os-- 文件路径操作

argparse--命令行参数处理

### 下载安装

```
git clone https://github.com/lzx1019056432/Be-Friendly-To-New-People.git
```

### 安装依赖包

```
pip install -r requirements.txt
```

### 使用方式

在当前目录下输入：

```
cd GeneratorGIF-and-SeparateGIF
```

第一次在GitHub上整理资源，有哪些做的不恰当的地方，还希望各位大佬多提提意见。做这个的初心就是想收集一些比较好的机器学习和人工智能入门案例，带有详细文档解释。这样也大大降低入门门槛，同时减少了新手各种找资料的实践。如果有愿意一起完善这个项目的，可以邮箱联系我 1019056432 @qq.com  期待与大佬一起做一件有意义的事。

* 生成GIF图片

```
python GeneratorGif.py -i image -o outputimage -d 0.5
```

-i  后面需跟上图片所在的文件夹

-o  输出的图片名称

-d  GIF图片播放速度，即每张图片转换延迟

* 分解GIF图片

```
python SeparateGif.py -i image.gif -o outputimage
```

-i  后面添加需要分解的GIF图片

-o  输出图片的名称，多图片后面使用递增数字区分

### 注释

1. 建议将需要合成的图片放到一个文件夹中，然后将文件放入GeneratorGIF-and-SeparateGIF目录下
2. 也可以将项目目录添加到系统环境变量中，这样就可以随时随地使用这个工具了。
3. 如果有任何疑问，欢迎大家CSDN私信我吗，我会第一时间给大家回答的。