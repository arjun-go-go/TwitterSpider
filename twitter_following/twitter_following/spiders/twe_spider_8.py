# -*- coding: utf-8 -*-
import re
import scrapy
from copy import deepcopy
from ..items import Followers,Following
from scrapy_redis.spiders import RedisSpider


class TweSpider8Spider(RedisSpider):
    name = 'twe_spider_8'
    allowed_domains = ['twitter.com']
    start_urls = ['https://twitter.com/988aa2d2f04249c/followers']

    redis_key = "following"

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        "accept-encoding": "gzip, deflate, br",
        "Referer": "https://twitter.com",
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36",
    }

    # cookie = {'personalization_id': '"v1_+QGSfcMSxkV8kyMur2APmw', 'guest_id': 'v1%3A154164429028797999', '_ga': 'GA1.2.641061644.1541644294', '_gid': 'GA1.2.1383659725.1541644294', 'ads_prefs': '"HBERAAA', 'kdt': 'JHQUK70hpovtIzAxmdkbCDudg9bdrGYnWF3WgjnE', 'remember_checked_on': '1', 'twid': '"u', 'auth_token': '022026822a67658b4583e1c7495e861cece9a83c', 'csrf_same_site_set': '1', 'csrf_same_site': '1', 'ct0': '28910ee476cc9be43fdd4aa3014e1bb1', 'lang': 'zh-cn', '_twitter_sess': 'BAh7CSIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCCopY%252FZmAToHaWQiJWYz%250AMTQzZTA0MGI0ZTMyNmMxNGFiZDEzMTY0NzRiNjJmOgxjc3JmX2lkIiU2N2Rk%250AYjVlNmU3MWMxNzBiNGZhZDhmZDNkMjdmOTkxYQ%253D%253D--0161f58ef902d64c45ec995038c81395abf5ddba', 'app_shell_visited': '1'}

    #
    # def start_requests(self):
    #     url = 'https://twitter.com/988aa2d2f04249c/followers'
    #     yield scrapy.Request(url,headers=self.headers,cookies=self.cookie,callback=self.parse)

    def parse(self, response):

        s_name = re.match(r"https:\/\/twitter.com\/(.*)\/followers.*", response.url)
        max_position = response.xpath(
            "//div[@class='GridTimeline']//div[@class='GridTimeline-items has-items']/@data-min-position").extract_first()
        div_list = response.xpath("//div[@class='GridTimeline']//div[@class='GridTimeline-items has-items']/div")
        for div in div_list:
            div_list_sm = div.xpath("./div")
            for div_sm in div_list_sm:
                followers_item = Followers()
                """要爬取得用户名"""
                followers_item["following"] = s_name.group(1)
                try:
                    followers_username = div_sm.xpath(
                        './/div[contains(@class, "u-textTruncate u-inlineBlock")]/a/@href').extract_first()
                    """以获得用户名"""
                    followers_item["username"] = re.match(r"\/(.*)", followers_username).group(1)
                    yield followers_item
                except Exception as e:
                    print(e)

        # yield scrapy.Request("https://twitter.com/{}/following".format(s_name.group(1)),
        #                      callback=self.parse_following)

        if max_position and s_name:
            next_url = "https://twitter.com/{0}/followers?max_position={1}".format(s_name.group(1), max_position)
            yield scrapy.Request(next_url,callback=self.parse)

        else:
            print("%s.....followers爬取完毕........followers爬取完毕........爬取完毕......" % s_name.group(1))



    def parse_following(self, response):

        ss_name = re.match(r"https:\/\/twitter.com\/(.*)\/following.*", response.url)
        maxx_position = response.xpath(
            "//div[@class='GridTimeline']//div[@class='GridTimeline-items has-items']/@data-min-position").extract_first()

        div_list = response.xpath(
            "//div[@class='GridTimeline']//div[@class='GridTimeline-items has-items']/div")
        for div in div_list:
            div_list_sm = div.xpath("./div")
            for div_sm in div_list_sm:
                following_item = Following()
                """要爬取得用户名"""
                following_item["following"] = ss_name.group(1)
                try:
                    following_username = div_sm.xpath(
                        './/div[contains(@class, "u-textTruncate u-inlineBlock")]/a/@href').extract_first()
                    following_item["username"] = re.match(r"\/(.*)", following_username).group(1)

                    yield following_item
                except Exception as e:
                    print(e)

        if maxx_position and ss_name:
            next_url = "https://twitter.com/{0}/following?max_position={1}".format(ss_name.group(1), maxx_position)
            yield scrapy.Request(next_url,
                                 callback=self.parse_following)

        else:
            print("%s.....following爬取完毕.........following爬取完毕........爬取完毕......" % ss_name.group(1))

