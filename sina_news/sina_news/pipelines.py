# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.conf import settings
import pymongo
import logging
#from bson import ObjectId


class SinaNewsPipeline(object):
    def process_item(self, item, spider):

        return item


class SinaDatabase(object):

    def __init__(self):
        host = settings['MONGODB_HOST']
        port = settings['MONGODB_PORT']
        db_name = settings['MONGODB_DB_NAME']
        coll_name = settings['MONGODB_COLL_NAME1']
        self.client = pymongo.MongoClient(host=host, port=port)
        self.db = self.client[db_name]
        self.coll = self.db[coll_name]

    def process_item(self, item, spider):
        #update_time_result = self.coll.find({'update_time_flag': {'$exists': True}})
        update_time_result = self.coll.find({'update_time_flag': {'$type': 2}}) #string
        before_update_time=''
        if update_time_result.count()>=3:
            cc = 0
            for update in update_time_result:
                if cc==0:
                    condition = {'_id': update['_id']}
                    #collGroup.remove({"_id": ObjectId('_id的字符串')})
                    #self.coll.delete_one({'_id': update['_id']})
                    update['update_time_flag'] = None
                    delete_result = self.coll.update_one(condition, {'$set': update})
                    logging.info('matched:'+str(delete_result.matched_count))
                    logging.info('modified'+str(delete_result.modified_count))
                if cc==1:
                    before_update_time = update['update_time_flag']
                    break
                cc+=1
        elif update_time_result.count()>1:
            for update in update_time_result:
                if before_update_time=='':
                    before_update_time = update['update_time_flag']
                    break


        if (item['time_stamp']>before_update_time and before_update_time!='') or self.coll.find().count()<=30:
            time_query = {"time_stamp": item['time_stamp']}
            time_result = self.coll.find(time_query, {"news": 1})
            if time_result.count()==0:
                self.coll.insert_one(dict(item))
                logging.info('Succeed Saving')
            else:
                for x in time_result:
                    if item['news'] != x['news']:
                        self.coll.insert_one(dict(item))
                        logging.info('Succeed Saving')


        return item
