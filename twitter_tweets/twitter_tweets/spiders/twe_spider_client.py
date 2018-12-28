# -*- coding: utf-8 -*-
import json
import re
import scrapy


class TweSpiderClientSpider(scrapy.Spider):
    name = 'twe_spider_client'
    allowed_domains = ['twitter.com']
    start_urls = ['https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=juntaowang&count=10']


    oauth_token_list = [
        {"access_token":"2539062798-VrfDaXKIdSstCG8Hb44LhtzbNlI0Gbs9vWHsVjV",
         "access_token_secret":"f4RmK9FLglMR5U0StSFbcQP99a7v6cYEidVM5ltrDhAwk",
         "consumer_key":"0ZOmoVp3xuRCxftkVXCSCqfcE",
         "consumer_secret":"qrYA1kChqEMjaFox5jobcvQ6zLV4Er3VphTtk7zd62sSZakh9m"
         },
        {
        "access_token": "2581126909-ogXS3trYqraaUsjzZDnanGBemoNauiP88lCl63q",
        "access_token_secret": "B3DV78C5UHgi301b3II2K2pSOO54bYueBSrf4oAanwQcv",
        "consumer_key": "EQg2MrI2KAwF2W7EGWAr1L2PM",
        "consumer_secret": "IGWRbR38I9QShVgDpgEhrRXebtopAJFX4dDarn6djO1j5cxAXa"
        },
        {
        "access_token": "2474326578-9qWvD4oVAxGcHJ5rQqSNjlD5ilSkDjBvwc6hPtS",
        "access_token_secret": "FTPBcxgr5hxwcZ8O8J6eN2L8tvOTzvzSjMqcfrZdgj9u3",
        "consumer_key": "p0xUdkuEaTOOw2maptTWLJ2bC",
        "consumer_secret": "RBHC9dDcbtMGCs9RFIE9ZOGqpngjeCP02WOho40Wy61uLb7dts"
        }
    ]

    def parse(self, response):
        json_content = json.loads(response.text)
        for j in json_content:
            source = j["source"]
            user = j["user"]["screen_name"]
            print(user)
            print(source)

