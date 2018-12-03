# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import json
import logging
import random
import re
import time
import requests
from fake_useragent import UserAgent
from scrapy import signals
from scrapy.http import HtmlResponse

from .tools.get_cookies import Cookie


class TwitterFollowingSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class TwitterFollowingDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)



class RandomUserAgentMiddlware(object):
    #随机更换user-agent
    def __init__(self, crawler):
        super(RandomUserAgentMiddlware, self).__init__()
        self.ua = UserAgent(use_cache_server=False)
        self.ua_type = crawler.settings.get("RANDOM_UA_TYPE", "random")

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_request(self, request, spider):
        def get_ua():
            return getattr(self.ua, self.ua_type)

        request.headers.setdefault('User-Agent', get_ua())


class RandomProxyMiddleware(object):
    #动态设置ip代理
    def process_request(self, request, spider):

        spider.logger.info("subtitleSpiderMiddleware process_request: request=%s, spider=%s", request, spider)

        request.meta["proxy"] = "https://127.0.0.1:1080"

        spider.logger.info("request.meta %s", request.meta)



class CookiesMiddleware(object):

    def process_request(self, request, spider):
        print("&" * 100)
        # co = """ga=GA1.2.832194716.1542096962; _gid=GA1.2.1378979390.1542096962; lang=zh-cn; dnt=1; kdt=h5IeY8Eq2F94VkzhmCVHSKXPzJP0c0m2Uq5GxfWr; remember_checked_on=0; _twitter_sess=BAh7CiIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCIk1JAxnAToMY3NyZl9p%250AZCIlZDFkZjBjNDdlNmJkMjAxNWE5MWNiODUyYTk1ZjQ4Y2Y6B2lkIiViMDNm%250AYmQwYmMwYjA3OTIwMzFjNGRlZTdhNjZjMmMxYjoJdXNlcmwrCQDgV8j127QO--890133ba2d469dd50eac068165efcefb482ba323; csrf_same_site_set=1; csrf_same_site=1; personalization_id="v1_e2pdSoXLugATjdhNlS2DWA=="; guest_id=v1%3A154220274119362006; external_referer=padhuUp37zjgzgv1mFWxJ5Xq0CLV%2BbpWuS41v6lN3QU%3D|0|8e8t2xd8A2w%3D; ads_prefs="HBISAAA="; twid="u=1059713661013581824"; auth_token=e7f441c5fd73bd6d1fcebd0ae53c6dc48c632f05; __utma=43838368.832194716.1542096962.1542279024.1542279024.1; __utmc=43838368; __utmz=43838368.1542279024.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); ct0=177c2af792e8a2cf5bd4357992eef57a; _gat=1"""
        # cookie_dict = Cookie(co).stringTodict()
        # request.cookies = {'_ga': 'GA1.2.832194716.1542096962', '_gid': 'GA1.2.1378979390.1542096962', 'lang': 'zh-cn', 'dnt': '1', 'kdt': 'h5IeY8Eq2F94VkzhmCVHSKXPzJP0c0m2Uq5GxfWr', 'remember_checked_on': '0', '_twitter_sess': 'BAh7CiIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCIk1JAxnAToMY3NyZl9p%250AZCIlZDFkZjBjNDdlNmJkMjAxNWE5MWNiODUyYTk1ZjQ4Y2Y6B2lkIiViMDNm%250AYmQwYmMwYjA3OTIwMzFjNGRlZTdhNjZjMmMxYjoJdXNlcmwrCQDgV8j127QO--890133ba2d469dd50eac068165efcefb482ba323', 'csrf_same_site_set': '1', 'csrf_same_site': '1', 'personalization_id': '"v1_e2pdSoXLugATjdhNlS2DWA', 'guest_id': 'v1%3A154220274119362006', 'external_referer': 'padhuUp37zjgzgv1mFWxJ5Xq0CLV%2BbpWuS41v6lN3QU%3D|0|8e8t2xd8A2w%3D', 'ads_prefs': '"HBISAAA', 'twid': '"u', 'auth_token': 'e7f441c5fd73bd6d1fcebd0ae53c6dc48c632f05', '__utma': '43838368.832194716.1542096962.1542279024.1542279024.1', '__utmc': '43838368', '__utmz': '43838368.1542279024.1.1.utmcsr', 'ct0': '177c2af792e8a2cf5bd4357992eef57a', '_gat': '1'}
        # request.cookies = {'_ga': 'GA1.2.832194716.1542096962', 'dnt': '1', 'kdt': 'h5IeY8Eq2F94VkzhmCVHSKXPzJP0c0m2Uq5GxfWr', 'remember_checked_on': '0', 'csrf_same_site_set': '1', 'csrf_same_site': '1', '__utma': '43838368.832194716.1542096962.1542279024.1542279024.1', '__utmz': '43838368.1542279024.1.1.utmcsr', 'ct0': 'cf778ae932b423cc555ab70001682fe0', '_gid': 'GA1.2.306159682.1542595552', '_gat': '1', 'personalization_id': '"v1_jr7zU+rm2ke8woM/VZO46Q', 'guest_id': 'v1%3A154260658535186323', 'ads_prefs': '"HBESAAA', '_twitter_sess': 'BAh7CiIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCEYd3ClnAToMY3NyZl9p%250AZCIlMzYxZTgwNGU0OWU5ZDk4YWY2YmVkZjY1ZjRiMGI3NGU6B2lkIiUyNDZm%250ANzc0MDc2NGVhOWFlOTAxNzE4Y2Q4ZWZiNmI5NzoJdXNlcmwrCQDQlLHTTygO--0f29e4cfd3d87e7ec992f08256cec648ebc28fbe', 'twid': '"u', 'auth_token': 'cc2d0c47d028ecd1f0b2964b368886cb32e3bbe5', 'lang': 'en'}
        request.cookies = {'_ga': 'GA1.2.832194716.1542096962', 'kdt': 'h5IeY8Eq2F94VkzhmCVHSKXPzJP0c0m2Uq5GxfWr', 'remember_checked_on': '0', 'csrf_same_site_set': '1', 'csrf_same_site': '1', '__utma': '43838368.832194716.1542096962.1542279024.1542279024.1', '__utmz': '43838368.1542279024.1.1.utmcsr', '_gid': 'GA1.2.306159682.1542595552', 'personalization_id': '"v1_jr7zU+rm2ke8woM/VZO46Q', 'guest_id': 'v1%3A154260658535186323', 'ct0': 'e030d1d663f70c20181b90470e01f837', 'lang': 'zh-cn', 'external_referer': 'padhuUp37zjgzgv1mFWxJ5Xq0CLV%2BbpWuS41v6lN3QU%3D|0|8e8t2xd8A2w%3D', '_gat': '1', 'ads_prefs': '"HBERAAA', '_twitter_sess': 'BAh7CiIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCEYd3ClnAToMY3NyZl9p%250AZCIlMzYxZTgwNGU0OWU5ZDk4YWY2YmVkZjY1ZjRiMGI3NGU6B2lkIiUyNDZm%250ANzc0MDc2NGVhOWFlOTAxNzE4Y2Q4ZWZiNmI5NzoJdXNlcmwrCQPAlSGztgUM--236d2630cf8da8d0f75bcdd92043489030b1cb6a', 'twid': '"u', 'auth_token': '13adc02db0f37eb166f16f782abb973d9e0c0cd6'}


class RandomCookiesMiddleware(object):
    def __init__(self, cookies_url):
        self.logger = logging.getLogger(__name__)
        self.cookies_url = cookies_url

    def get_random_cookies(self):
        try:
            response = requests.get(self.cookies_url)
            if response.status_code == 200:
                cookies = json.loads(response.text)
                return cookies
        except requests.ConnectionError:
            return False

    def process_request(self, request, spider):
        self.logger.debug('正在获取Cookies')
        cookies = self.get_random_cookies()
        if cookies:
            request.cookies = cookies
            self.logger.debug('使用Cookies ' + json.dumps(cookies))

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(
            cookies_url=settings.get('COOKIES_URL')
        )



class TwitterCheckMiddleware(object):
    def process_response(self, request, response, spider):
        response_status = response.status
        response_text = response.text
        check_res = "".join(response_text.split())
        request_url = request.url
        position = re.match(r'.*data-min-position="(\d+?)">',check_res)
        if not position and response_status == 200:
            print("爬累了....累了.....累了....,休息5秒")
            clock = 0
            sleep_time = 5
            while (clock < sleep_time):
                nclock = sleep_time - clock
                print(nclock)
                time.sleep(1)
                clock += 1
            print('爬虫重新启动中')
            return request.replace(url=request_url)

        else:
            return response



"""8615510018612  qazwsx123456"""
"""starksaya  stark123456789"""
"""479510392@qq.com  13872774874twitter"""

class JSPageMiddleware(object):
    #通过chrome 动态访问
    def process_request(self,request,spider):
        if spider.name =="twe_spider_1":
            spider.browser.get(request.url)
            # for i in range(0,3):
            #     spider.browser.execute_script("var q=document.documentElement.scrollTop=10000")
            time.sleep(random.randint(3,6))
            if "login" in request.url:
                print("访问：{0}".format(request.url))
                spider.browser.find_element_by_xpath(
                    "//div[@class='clearfix field']/input[@name='session[username_or_email]']").send_keys('8615510018612')
                time.sleep(random.randint(2, 6))

                spider.browser.find_element_by_xpath(
                    "//div[@class='clearfix field']/input[@name='session[password]']").send_keys('qazwsx123456')
                time.sleep(random.randint(2, 5))
                spider.browser.find_element_by_xpath("//div[@class='clearfix']/button[@type='submit']").click()
                time.sleep(random.randint(5, 8))

                return HtmlResponse(url=spider.browser.current_url,body=spider.browser.page_source,encoding="utf-8")

            if "following" or "followers" in request.url:
                for i in range(1, 450):
                    spider.browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
                    print("访问：{0}".format(request.url))
                    time.sleep(random.randint(3, 6))
                # time.sleep(random.randint(8, 12))
                return HtmlResponse(url=spider.browser.current_url, body=spider.browser.page_source,request=request,encoding="utf-8")

            else:
                time.sleep(random.randint(6, 10))
                return HtmlResponse(url=spider.browser.current_url, body=spider.browser.page_source,request=request,encoding="utf-8")

