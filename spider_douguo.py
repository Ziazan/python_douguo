'''
@Author: your name
@Date: 2020-05-01 17:14:08
@LastEditTime: 2020-05-02 14:05:05
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: /python/douguo/spider_douguo.py
'''
import requests
import json
from multiprocessing import Queue
from handle_mongo import mongo_info
from concurrent.futures import ThreadPoolExecutor # 线程池

#创建队列
queue_list = Queue()

# 处理数据请求
def handle_request(url, data):
    header = {
        "client":"4",
        "version":"6962.2",
        "device":"SM-G955N",
        "sdk":"25,7.1.2",
        "channel":"baidu",
        # "resolution":"1600*900",
        # "display-resolution":"1600*900",
        # "dpi":"2.0",
        # "android-id":"784F438E43A20000",
        # "pseudo-id":"864394010787945",
        "brand":"samsung",
        "scale":"2.0",
        "timezone":"28800",
        "language":"zh",
        "cns":"2",
        "carrier":"CMCC",
        "User-Agent":"Mozilla/5.0 (Linux; Android 7.1.2; SM-G955N Build/N2G48H; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/75.0.3770.143 Mobile Safari/537.36",
        "imei":"864394010787945",
        "terms-accepted":"1",
        "newbie":"1",
        "reach":"10000",
        "Content-Type":"application/x-www-form-urlencoded; charset=utf-8",
        "Accept-Encoding":"gzip",
        "Connection":"Keep-Alive",
        "Host":"api.douguo.net",
        "Content-Length":"147",
    }

    response = requests.post(url=url,headers=header,data=data)
    return response

# 抓取品类列表
def handle_cat():
    url = 'http://api.douguo.net/recipe/flatcatalogs'
    data = {
        "client":"4",
        "_vs":"2305",
    }
    response = handle_request(url,data)
    index_dict = json.loads(response.text)
    for index_item in index_dict["result"]["cs"]:
        for index_item_1 in index_item["cs"]:
            for index_item_2 in index_item_1["cs"]:
                queue_list.put(index_item_2["name"])


# 关键词搜索
def handle_search(keyword):
    print("当前处理的食材是:",keyword,end="\n")
    url = 'http://api.douguo.net/search/universalnew/0/10'
    data = {
        "client":"4",
        "keyword":keyword,
        "_vs":"400",
    }
    response = handle_request(url,data)
    caipu_list_dict =  json.loads(response.text)
    for item in caipu_list_dict["result"]["recipe"]["recipes"]:
        caipu_info = {}
        caipu_info["shicai"] = keyword
        caipu_info['caipu_name'] = item["n"]
        caipu_info["author_name"] = item["an"]
        caipu_info["caipu_id"] = item["id"]
        caipu_info["cookstory"] = item["cookstory"]
        caipu_info["img"] = item["img"]
        caipu_info["major"] = item["major"]
        caipu_info["detail_url"] = item["au"]
        detail_info_dict = json.loads(handle_detail(caipu_info))
        caipu_info["tips"] = detail_info_dict["result"]["recipe"]["tips"]
        caipu_info["cookstep"] = detail_info_dict["result"]["recipe"]["cookstep"]
        print("当前入库的菜谱是：",caipu_info['caipu_name'])
        mongo_info.insert_item(caipu_info)
    
#菜谱详情
def handle_detail(item):
    url = "http://api.douguo.net/recipe/detail/" + str(item["caipu_id"])
    data = {
        "client":"4",
        "_vs":"11101",
        "_ext":	'{"query":{ "kw":' + str(item["shicai"]) + ',"src":"11101","idx":"1", "type":"13", "id":' + str(item["caipu_id"]) + ' }',
    }
    response = handle_request(url,data)
    return response.text

handle_cat()

pool = ThreadPoolExecutor(max_workers=20) #创建线程池
# while queue_list.qsize() > 0: 报错
while not queue_list.empty():
    pool.submit(handle_search,queue_list.get()) # 函数名和 参数

    
