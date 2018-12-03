# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TwitterTweetsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class Item(scrapy.Item):
    table = scrapy.Field()


class Profile(Item):
    cover_image = scrapy.Field()
    image = scrapy.Field()
    name = scrapy.Field()
    user_name = scrapy.Field()
    user_id = scrapy.Field()
    tweets = scrapy.Field()
    following = scrapy.Field()
    followers = scrapy.Field()
    favorites = scrapy.Field()
    location = scrapy.Field()
    location_page = scrapy.Field()
    location_id = scrapy.Field()
    website = scrapy.Field()
    join_date = scrapy.Field()
    introduction = scrapy.Field()
    media = scrapy.Field()
    media_url = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
               insert into tw_user_copy(name,user_name,user_id,tweets,following,followers,favorites,location,join_date,introduction
                 ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                 ON DUPLICATE KEY UPDATE tweets=VALUES(tweets),following=VALUES(following),followers=VALUES(followers),favorites=VALUES(favorites)
           """
        params = (
            self["name"],self["user_name"],self["user_id"],self["tweets"],
            self["following"],self["followers"],self["favorites"],
            self["location"],self["join_date"],self["introduction"],

        )
        return insert_sql, params


class Tweet(scrapy.Item):
    name = scrapy.Field()
    user_id = scrapy.Field()
    tweet_time = scrapy.Field()
    user_name = scrapy.Field()
    tweet_list = scrapy.Field()
    tweet_name = scrapy.Field()
    tweet_id = scrapy.Field()
    tweet_text = scrapy.Field()
    replies = scrapy.Field()
    retweets = scrapy.Field()
    favorites = scrapy.Field()
    data_time = scrapy.Field()
    data_id = scrapy.Field()
    media_images = scrapy.Field()
    url = scrapy.Field()
    media_videos = scrapy.Field()
    table = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
               insert into tw_tweets_copy(name,tweet_time,tweet_list,tweet_name,
               tweet_id,tweet_text,replies,retweets,favorites,data_time,data_id,url
                 ) VALUES (%s, %s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s)
           """
        params = (
            self["name"],self["tweet_time"],
            self["tweet_list"],self["tweet_name"],self["tweet_id"],
            self["tweet_text"],self["replies"],self["retweets"],self["favorites"],
            self["data_time"],self["data_id"],self["url"]
        )
        return insert_sql, params

