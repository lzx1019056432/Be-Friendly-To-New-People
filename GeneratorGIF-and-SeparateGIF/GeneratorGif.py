from PIL import Image
import numpy as np
import imageio
import argparse
import os
'''
作者：@梁先森
CSDN博客地址：https://blog.csdn.net/lzx159951
实现功能：实现图片转换成gif、分离gif为图片

'''
parser = argparse.ArgumentParser()
parser.add_argument("-i",type=str,default="image",help="Please input the file folder path of the picture")
parser.add_argument("-o","-output",default="outputimage",type=str,help="the name of output image")
parser.add_argument("-d",default="0.5",type=float,help="Picture playback interval")

args = parser.parse_args()
listimage=[]#存储图片
listname=[]#存储图片地址
try:
    if(not os.path.exists(args.i)):
        print("您输入的文件夹地址或者图片地址不存在！")
    else:
        for imagename in os.listdir('image'):
            if(imagename.lower().endswith('jpg') or imagename.lower().endswith('png')):
                listname.append(imagename)
        print("读取图片完成")
        for imagename in listname:
            if imagename.find('.'):
                im = Image.open(args.i+'/'+imagename)
                im = np.array(im)
                listimage.append(im)
        #创建文件夹
        if(not os.path.exists(args.i+'/output')):
            os.mkdir(args.i+'/output')
        if(str(args.o).lower().endswith('.gif')):
            filename=args.i+'/output/'+args.o
        else:
            filename = args.i+'/output/'+args.o+'.gif'
        print("正在生成gif......")
        imageio.mimsave(filename,listimage,'GIF',duration=args.d)
        print("gif输出完毕,感谢使用")
except:
    print("图片转换失败")