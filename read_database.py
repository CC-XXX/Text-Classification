# -*- coding: utf-8 -*-

import pymongo

def get_news():
    client = pymongo.MongoClient(host='localhost', port=27017)
    db = client['n']

    MONGO_TABLE = 'sina_news'
    collection = db[MONGO_TABLE]
    m = collection.find().sort([('_id', -1)])
    count = 1
    for i in m:
        news_list.append(i['news'])
    return news_list
