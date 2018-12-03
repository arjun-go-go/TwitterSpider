# -*- coding: utf-8 -*-
import re
import scrapy
import json
from scrapy.selector import Selector
from ..items import Tweet,Profile
from ..loaders import ItemLoader,TweetsLoader,strip
from copy import deepcopy
from scrapy_redis.spiders import RedisSpider



class TweSpider6Spider(RedisSpider):
    name = 'twe_spider_6'
    allowed_domains = ['twitter.com']
    # start_urls = ['http://twitter.com/']
    redis_key = "twitter"

    # def start_requests(self):
    #     # name_list = ["guoyong_says","zhuangdaohe1","kiddjoneke"]
    #     name_list = Search().search_sql()
    #     for name in name_list:
    #         url = "https://twitter.com/@" + name
    #         yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        re_name = re.match(r"https://twitter.com/@(.*)", response.url)
        if re_name:
            name = re_name.group(1)
        try:
            max_position = response.xpath('//div[@data-max-position]/@data-max-position').extract_first()

            user_item = Profile()
            """头像图片"""
            user_item["image"] = response.xpath('//*[contains(@class, "ProfileAvatar-image")]/@src').extract_first()

            """推特名称"""
            user_item["name"] = response.xpath('//a[contains(@class, "ProfileNameTruncated-link")]/text()').extract_first()
            user_item["name"] = strip(user_item["name"])

            """@推特名称"""
            user_item["user_name"] = response.xpath('//div[@class="ProfileCardMini-screenname"]//b/text()').extract_first()

            """推特用户id"""
            user_item["user_id"] = response.xpath('//div[@class="ProfileNav"][@data-user-id]/@data-user-id').extract_first()

            """总共发的推文量"""
            user_item["tweets"] = response.xpath(
                '//li[contains(@class, "ProfileNav-item--tweets")]//span[@class="ProfileNav-value"]/@data-count').extract_first()

            """"他关注的人数"""
            user_item["following"] = response.xpath(
                '//li[contains(@class, "ProfileNav-item--following")]//span[@class="ProfileNav-value"]/@data-count').extract_first()

            """关注他的人数"""
            user_item["followers"] = response.xpath(
                '//li[contains(@class, "ProfileNav-item--followers")]//span[@class="ProfileNav-value"]/@data-count').extract_first()

            """喜欢的人数"""
            user_item["favorites"] = response.xpath(
                '//li[contains(@class, "ProfileNav-item--favorites")]//span[@class="ProfileNav-value"]/@data-count').extract_first()

            """位置信息，国家"""
            user_item["location"] = response.xpath(
                '//div[contains(@class, "ProfileHeaderCard-location")]//text()').extract()
            user_item["location"] = "".join("".join(user_item["location"]).split())

            """加入twitter时间"""
            user_item["join_date"] = response.xpath(
                '//div[@class="ProfileHeaderCard-joinDate"]//span[@title]/@title').extract_first()
            user_item["join_date"] = "".join("".join(user_item["join_date"]).split())

            """与他有关的公司资料,简介"""
            user_item["introduction"] = response.xpath(
                '//p[contains(@class, "ProfileHeaderCard-bio")]//text()').extract()
            user_item["introduction"] = "".join("".join(user_item["introduction"]).split())

            user_item["table"] = "users"

            if max_position:
                # next_url = "https://twitter.com/@{0}?max_position={1}".format(user_item["user_name"],max_position)
                next_url = "https://twitter.com/@{0}".format(user_item["user_name"])
                yield scrapy.Request(next_url,
                                     callback=self.parse_tweets,
                                     dont_filter=True,
                                     meta={"item":deepcopy(user_item)})

            yield user_item

        except Exception as e:
            print(e)


    def parse_tweets(self, response):
        user_item = deepcopy(response.meta["item"])
        position = response.xpath('//div[@data-max-position]/@data-min-position').extract_first()

        li_list = response.xpath('//ol[@id="stream-items-id"]/li')
        for selector in li_list:
            tweet_item = Tweet()
            tweet_item["name"] = user_item["user_name"]
            """推文中被@的人"""
            user_list = selector.xpath('.//a[@data-mentioned-user-id]/@href').extract()
            tweet_item["tweet_list"] = ",".join(user_list)

            """单个推文id"""
            tweet_item["data_id"] = selector.xpath('.//li[@data-item-id]/@data-item-id').extract_first()

            """原始推文"""
            tweet_item["tweet_id"] = selector.xpath('.//div[@data-user-id]/@data-user-id').extract_first()

            """原始推文发文名称"""
            tweet_name = selector.xpath('.//div[@class="stream-item-header"]/a/@href').extract_first()
            if tweet_name:
                tweet_item["tweet_name"] = re.match(r"\/(.*)", tweet_name).group(1)

            """发推的时间"""
            tweet_item["tweet_time"] = selector.xpath('.//small[@class="time"]/a/@title').extract_first()
            tweet_item["tweet_time"] = "".join(tweet_item["tweet_time"].split())

            """发推时间戳"""
            tweet_item["data_time"] = selector.xpath('.//small[@class="time"]/a/span/@data-time').extract_first()
            tweet_item["data_time"] = int(tweet_item["data_time"])

            """发推的链接"""
            tweet_item["url"] = selector.xpath('.//small[@class="time"]/a/@href').extract_first()
            if tweet_item["url"] is not None:
                tweet_item["url"] = "https://twitter.com" + tweet_item["url"]

            """推文内容"""
            tweet_item["tweet_text"] = selector.xpath('.//p[contains(@class, "TweetTextSize")]//text()').extract()
            tweet_item["tweet_text"] = "".join("".join(tweet_item["tweet_text"]).split())

            """推文回复数"""
            tweet_item["replies"] = selector.xpath(
                './/span[contains(@class, "ProfileTweet-action--reply")]//span[@class="ProfileTweet-actionCount"]/@data-tweet-stat-count').extract_first()

            """每条推文转推数"""
            tweet_item["retweets"] = selector.xpath(
                './/span[contains(@class, "ProfileTweet-action--retweet")]//span[@class="ProfileTweet-actionCount"]/@data-tweet-stat-count').extract_first()

            """每条推文点赞的数量"""
            tweet_item["favorites"] = selector.xpath(
                './/span[contains(@class, "ProfileTweet-action--favorite")]//span[@class="ProfileTweet-actionCount"]/@data-tweet-stat-count').extract_first()

            """推文图片链接"""
            tweet_item['media_images'] = selector.xpath('.//div[contains(@class, "AdaptiveMedia-photoContainer")]/@data-image-url').extract_first()

            tweet_item['media_videos'] = selector.xpath('.//video/@src').extract_first()

            tweet_item["table"] ='tweets'


            yield tweet_item

            # position = response.xpath('//div[@data-max-position]/@data-min-position').extract_first()
            if position:
                yield scrapy.Request(
                    "https://twitter.com/@{0}?max_position={1}".format(tweet_item["name"],position),
                    callback=self.parse_tweets,
                meta={"item":deepcopy(user_item)})


