# -*- coding:utf-8 -*-
'''
打算做一款自动答题辅助软件，主要是针对微信读书
思路：
1. 截屏含有题目和答案的图片(范围可以自己指定)
2. 使用百度的图片识别技术将图片转化为文字，并进行一系列处理，分别将题目和答案进行存储
3. 调动百度知道搜索接口，将题目作为搜索关键字进行答案搜索
4. 将搜索出来的内容使用BeautifulSoup4进行答案提取，这里可以设置答案提取数量
5. 将搜索结果进行输出显示

剩余问题：
1. 遇到填空题的时候，很容易会出现搜索失败的情况
------------
作者：梁先森
CSDN主页:https://blog.csdn.net/lzx159951
Github主页：https://github.com/lzx1019056432
-----------
'''
import requests
import re
import base64
from bs4 import  BeautifulSoup
from urllib import parse
import time
from PIL import ImageGrab
class autogetanswer():
    def __init__(self,StartAutoRecomment=True,answernumber=5):
        self.StartAutoRecomment=StartAutoRecomment
        self.APIKEY=['BICrjnoCjzFmdTWyzpzDUNNI','CrHGnuyl2L9ZZGOgS5ore03C']
        self.SECRETKEY=['BgL4j21oCS1XOIa4a9Kvf7c80qZMNGj9','1xo0j99UMkLu8NRATg75Bjj814uf90cx']
        self.accesstoken=[]
        self.baiduzhidao='http://zhidao.baidu.com/search?'
        self.question=''
        self.answer=[]
        self.answernumber=answernumber
        self.searchanswer=[]
        self.answerscore=[]
        self.reanswerindex=0
        self.imageurl='answer.jpg'
        self.position=(35,155,355,680)
        self.titleregular1=r'(10题|共10|12题|共12|翻倍)'
        self.titleregular2=r'(\?|\？)'
        self.answerregular1=r'(这题|问题|跳题|换题|题卡|换卡|跳卡|这有)'
    def GetAccseetoken(self):
        for i in range(len(self.APIKEY)):
            host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={}&client_secret={}'.format(self.APIKEY[i],self.SECRETKEY[i])
            response = requests.get(host)
            jsondata = response.json()
            self.accesstoken.append(jsondata['access_token'])
    def OCR(self,filename):
        request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"
        # 二进制方式打开图片文件
        f = open(filename, 'rb')
        img = base64.b64encode(f.read())
        params = {"image":img}
        access_token = self.accesstoken[0]
        request_url = request_url + "?access_token=" + access_token
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        response = requests.post(request_url, data=params, headers=headers)
        if response:
            result = response.json()
            questionstart=0
            answerstart=0
            self.question=''
            self.answer=[]
            for i in range(result['words_result_num']):
                if(re.search(self.titleregular1,result['words_result'][i]['words'])!=None):
                    questionstart=i+1
                if(re.search(self.titleregular2,result['words_result'][i]['words'])!=None):
                    answerstart=i+1
            if(answerstart!=0):
                for title in result['words_result'][questionstart:answerstart]:
                    if(re.search(self.answerregular1,title['words'])!=None):
                        pass
                    else:
                        self.question+=title['words']
                for answer in result['words_result'][answerstart:]:
                    if(re.search(self.answerregular1,answer['words'])!=None):
                        pass
                    else:
                        if(str(answer['words']).find('.')>0):
                            answer2 = str(answer['words']).split('.')[-1]
                        else:
                            answer2=answer['words']
                        self.answer.append(answer2)
            else:
                for title in result['words_result'][questionstart:]:
                    if(re.search(self.answerregular1,title['words'])!=None):
                        pass
                    else:
                        self.question+=title['words']
            print("本题问题：",self.question)
            print("本题答案：",self.answer)
        return response.json()

    def BaiduAnswer(self):
        request = requests.session()
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'}
        data = {"word":self.question}
        url=self.baiduzhidao+'lm=0&rn=10&pn=0&fr=search&ie=gbk&'+parse.urlencode(data,encoding='GB2312')
        ress = request.get(url,headers=headers)
        ress.encoding='gbk'
        if ress:
            soup = BeautifulSoup(ress.text,'lxml')
            result = soup.find_all("dd",class_="dd answer")
            if(len(result)!=0 and len(result)>self.answernumber):
                length=self.answernumber
            else:
               length=len(result)
            for i in range(length):
                self.searchanswer.append(result[i].text)

    def CalculateSimilarity(self,text1,text2):
        access_token = self.accesstoken[1]
        request_url="https://aip.baidubce.com/rpc/2.0/nlp/v2/simnet"
        request_url = request_url + "?access_token=" + access_token
        headers = {'Content-Type': 'application/json'}
        data={"text_1":text1,"text_2":text2,"model":"GRNN"}
        response = requests.post(request_url, json=data, headers=headers)
        response.encoding='gbk'
        if response:
            try:
                result = response.json()
                return result['score']
            except:
                return 0
    def AutoRecomment(self):
        if(len(self.answer)==0):
            return
        for i in range(len(self.answer)):
            scores=[]
            flag=0
            for j in range(len(self.searchanswer)):
                if(j!=0and (j%2==0)):
                    time.sleep(0.1)
                score = tools.CalculateSimilarity(tools.answer[i],tools.searchanswer[j])
                if(tools.answer[i] in tools.searchanswer[j]):
                    score=1
                scores.append(score)
                if(score>0.8):
                    flag=1
                    self.answerscore.append(score)
                    break
            if(flag==0):
                self.answerscore.append(max(scores))
        self.reanswerindex = self.answerscore.index(max(self.answerscore))
    def IniParam(self):
        self.accesstoken=[]
        self.question=''
        self.answer=[]
        self.searchanswer=[]
        self.answerscore=[]
        self.reanswerindex=0
    def MainMethod(self):
        while(True):
            try:
                order = input('请输入指令（1=开始，2=结束):')
                if(int(order)==1):
                    start = time.time()
                    self.GetAccseetoken()
                    img = ImageGrab.grab(self.position)#左、上、右、下
                    img.save(self.imageurl)
                    self.OCR(self.imageurl)
                    self.BaiduAnswer()
                    if(self.StartAutoRecomment):
                        self.AutoRecomment()
                    print("======================答案区======================\n")
                    for i in range(len(self.searchanswer)):
                        print("{}.{}".format(i,self.searchanswer[i]))
                    end = time.time()
                    print(self.answerscore)
                    if(self.StartAutoRecomment and len(self.answer)>0):
                        print("\n推荐答案:",self.answer[self.reanswerindex])
                    print("\n======================答案区======================")
                    print("总用时：",end-start,end="\n\n")
                    self.IniParam()
                else:
                    break
            except:
                print("识别失败，请重新尝试")
                self.IniParam()
                pass

if __name__ == '__main__':
    tools = autogetanswer(StartAutoRecomment=False)
    tools.MainMethod()

