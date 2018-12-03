# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TwitterFollowingItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class Followers(scrapy.Item):
    id = scrapy.Field()
    username = scrapy.Field()
    name = scrapy.Field()
    followers_name = scrapy.Field()
    followers_url = scrapy.Field()
    following = scrapy.Field()
    followers_Introduction = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
               insert into following_3(username,followers
                 ) VALUES (%s, %s)
           """
        params = (
            self["username"],self["following"]
        )
        return insert_sql, params




class Following(scrapy.Item):
    id = scrapy.Field()
    username = scrapy.Field()
    name = scrapy.Field()
    followers_name = scrapy.Field()
    followers_url = scrapy.Field()
    following = scrapy.Field()
    followers_Introduction = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
               insert into following_3(username,followers
                 ) VALUES (%s, %s)
           """
        params = (
            self["following"],self["username"]
        )
        return insert_sql, params