# -*- coding:utf-8 -*-
import requests
import json
import time
def test1(destination):
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
             'Cookie':'_abtest_userid=d778cf10-b380-4da2-977a-b3fd72a9934d; _RF1=120.216.170.214; _RSG=xQKVBUHW1u6FBqc9suTio8; _RDG=28014134c27fb82c9e1cd0973a907c8ce8; _RGUID=6e018117-8b7d-46bb-8cac-778d899b42cf; Session=smartlinkcode=U130026&smartlinklanguage=zh&SmartLinkKeyWord=&SmartLinkQuary=&SmartLinkHost=; Union=AllianceID=4897&SID=130026&OUID=&createtime=1590973579&Expires=1591578378915; MKT_CKID=1590973578972.3e60b.vtue; MKT_CKID_LMT=1590973578973; MKT_Pagesource=PC; _ga=GA1.2.776587014.1590973579; _gid=GA1.2.428582162.1590973579; StartCity_Pkg=PkgStartCity=2; GUID=09031160411534832517; appFloatCnt=1; manualclose=1; _jzqco=%7C%7C%7C%7C%7C1.1607786070.1590973578966.1590975682555.1590976896014.1590975682555.1590976896014.0.0.0.8.8; __zpspc=9.1.1590973578.1590976896.8%232%7Cwww.baidu.com%7C%7C%7C%7C%23; _bfa=1.1590973576257.dfu8z.1.1590973576257.1590973576257.1.31; _bfs=1.31; _bfi=p1%3D104317%26p2%3D104317%26v1%3D31%26v2%3D30; _gat=1',
             'origin':'https://vacations.ctrip.com',
             'x-req-src':'{"appId":"100020727","from":"vacations.ctrip.com/list/whole/d-chongqing-158.html","version":"8300.103","os":"PC","platform":"Online"}',
             'content-type':'application/json'}
    data={"contentType":"json","head":{"cid":"09031160411534832517","ctok":"","cver":"1.0","lang":"01","sid":"8888","syscode":"09","auth":"","extension":[]},"version":"80400","client":{"trace":"none","device":"PC","source":"NVacationSearchV2","variables":[{"key":"SHXVERSION","value":"B"}],"cid":"1590973576257.dfu8z"},"poiType":{"poid":158,"type":"D","keyword":destination},"filtered":{"sort":2,"channel":"Online","tab":"A126","saleCity":2,"startCity":2,"pageSize":30,"pageIndex":1,"items":[]},"returnType":{"type":"all","filters":"ProductNewLine,ProductLine,HotDestination,HotScenicSpot,SaleDepartureStat,TravelDays,DepartureDate,Month,ProductPattern,ProductLevel,ADSuitPersons,ProductDistrict,ProviderBrand,PriceRange,Promotion,OnSale","recommendProduct":True}}
    url="https://vacations.ctrip.com/list/restapi/gateway/13561/search?fxpcqlniredt=09031160411534832517"
    data = json.dumps(data)
    re = requests.post(url,headers=headers,data=data)
    jsondata = re.json()
    listdata=[]
    for i in range(4):
        listdata.append([jsondata['products'][i]['name'],jsondata['products'][i]['id']])
        #print(jsondata['products'][i]['name'],jsondata['products'][i]['id'],)
    return listdata
def test2(id):
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
             'Cookie':'_abtest_userid=d778cf10-b380-4da2-977a-b3fd72a9934d; _RF1=120.216.170.214; _RSG=xQKVBUHW1u6FBqc9suTio8; _RDG=28014134c27fb82c9e1cd0973a907c8ce8; _RGUID=6e018117-8b7d-46bb-8cac-778d899b42cf; Session=smartlinkcode=U130026&smartlinklanguage=zh&SmartLinkKeyWord=&SmartLinkQuary=&SmartLinkHost=; Union=AllianceID=4897&SID=130026&OUID=&createtime=1590973579&Expires=1591578378915; MKT_CKID=1590973578972.3e60b.vtue; MKT_CKID_LMT=1590973578973; MKT_Pagesource=PC; _ga=GA1.2.776587014.1590973579; _gid=GA1.2.428582162.1590973579; StartCity_Pkg=PkgStartCity=2; GUID=09031160411534832517; appFloatCnt=1; manualclose=1; _jzqco=%7C%7C%7C%7C%7C1.1607786070.1590973578966.1590975682555.1590976896014.1590975682555.1590976896014.0.0.0.8.8; __zpspc=9.1.1590973578.1590976896.8%232%7Cwww.baidu.com%7C%7C%7C%7C%23; _bfa=1.1590973576257.dfu8z.1.1590973576257.1590973576257.1.31; _bfs=1.31; _bfi=p1%3D104317%26p2%3D104317%26v1%3D31%26v2%3D30; _gat=1',
             'origin':'https://vacations.ctrip.com',
             'x-req-src':'{"appId":"100007656","from":"vacations.ctrip.com/tour/detail/p1020423035s2.html","version":"8300.103","os":"PC","platform":"Online"}',
             'content-type':'application/json'}
    for i in range(1,10):
        try:
            pagenum = i
            data={"ChannelCode":0,"Version":"810000","Locale":"zh-CN","head":{"cid":"09031160411534832517","ctok":"","cver":"1.0","lang":"01","sid":"8888","syscode":"09","auth":"","extension":[]},"productId":id,"paging":{"pageSize":5,"pageNo":pagenum},"sortType":2,"tagTerms":[],"PlatformId":4,"contentType":"json"}
            url="https://vacations.ctrip.com/tour/restapi/online/15656/listProductComments.json?_fxpcqlniredt=09031160411534832517"
            data = json.dumps(data)
            re = requests.post(url,headers=headers,data=data)
            jsondata = re.json()
            for i in range(5):
                print("\n-----------------------")
                print("评论内容：",jsondata['comments'][i]['content'])#获取评论数据
                print("评分：",jsondata['comments'][i]['score'])#获取评分
                datatime = str(jsondata['comments'][i]['commentTime'])[:-3]
                times = time.localtime(int(datatime))
                datatime = time.strftime("%Y-%m-%d %H:%M:%S",times)
                print("日期：",datatime)#获取日期
                print("-----------------------\n")
            time.sleep(2)
        except:
            break
def  mainfun():
    traveldestination = ['重庆','广州','郑州','三亚','上海','杭州','北京','成都']#这里是添加旅游地点
    for i in range(len(traveldestination)):
        listdata = test1(traveldestination[i])
        print("地点:",traveldestination[i],end='\n')
        for data in listdata:
            print(data[0])
            test2(data[1])
if __name__ == '__main__':
    mainfun()