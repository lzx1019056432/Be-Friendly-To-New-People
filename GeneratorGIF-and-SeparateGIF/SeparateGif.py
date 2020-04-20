from PIL import Image
import numpy as np
import imageio
import argparse
import os
'''
作者：@梁先森
CSDN博客地址：https://blog.csdn.net/lzx159951
github地址：
实现功能：将gif分离成一张张图片
'''

parser = argparse.ArgumentParser()
parser.add_argument("-i",type=str,default="image",help="Please input GIF picture")
parser.add_argument("-o","-output",default="outputimage",type=str,help="the name of output image")
args = parser.parse_args()
try:
    imagelist = imageio.mimread(args.i)
    print("GIF文件已成功读取")
except:
    print("GIF文件读取失败")
num=-1
path=''
try:
    if(not os.path.exists('output')):
        os.mkdir('output')
        path = 'output/'
    for i in imagelist:
        num+=1
        im = Image.fromarray(i)
        imagearray = np.array(i)
        if(imagearray.shape[2]==4):
            if(str(args.o).lower().endswith('.jpg') or str(args.o).lower().endswith('.jpeg') or str(args.o).lower().endswith('.png')):
                output = path+str(args.o).split('.')[0]+str(num)+'.png'
            else:
                output = path+str(args.o)+str(num)+'.png'
        imageio.imwrite(output,imagearray)
    print("GIF图片分离成功")
except:
    print("GIF图片分离失败")

