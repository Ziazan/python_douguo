'''
@Author: your name
@Date: 2020-05-01 22:54:45
@LastEditTime: 2020-05-02 10:26:31
@LastEditors: your name
@Description: In User Settings Edit
@FilePath: /python/douguo/handle_mongo.py
'''
import pymongo

from pymongo.collection import Collection

class Connect_mongo(object):
    def __init__(self):
        self.client = pymongo.MongoClient(host="127.0.0.1",port=27017)
        self.db_data = self.client["dougou_meishi"]

    def insert_item(self,item):
        db_collection = Collection(self.db_data,'t_douguo_item')
        db_collection.insert(item)

mongo_info = Connect_mongo()