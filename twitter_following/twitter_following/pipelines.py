# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


import pymongo
import pymysql
from py2neo import Graph,Node,Relationship
from twisted.enterprise import adbapi



class TwitterFollowingPipeline(object):
    def process_item(self, item, spider):
        return item


class MysqlTwistedPipline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host=settings["MYSQL_HOST"],
            db=settings["MYSQL_DBNAME"],
            user=settings["MYSQL_USER"],
            passwd=settings["MYSQL_PASSWORD"],
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool("pymysql", **dbparms)

        return cls(dbpool)

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider)

    def handle_error(self, failure, item, spider):
        print(failure)

    def do_insert(self, cursor, item):
        insert_sql, params = item.get_insert_sql()
        cursor.execute(insert_sql, params)


class Neo4jPipline(object):

    def __init__(self):
        self.graph = Graph("http://xxx.xx.xx.xxx:7474",username="neo4j",password="123456")

    def process_item(self, item, spider):
        tx = self.graph.begin()
        worker_list = [{"name":item["username"]},{"name":item["following"]}]
        for worker in worker_list:
            node = Node("Person",**worker)
            tx.merge(node)
        node_1 = Node(name=item["username"])
        node_2 = Node(name=item["following"])
        rel = Relationship(node_1,"following",node_2)
        try:
            tx.merge(rel)
            print("successful")
            tx.commit()
        except Exception as e:
            print(e)
            print("Failed")


class MongoPipeline(object):

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI', 'mongodb://xxx.xx.xx.xxx:27017'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'twitter')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[item['table']].insert_one(dict(item))
        return item