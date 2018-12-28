# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import re
import time
from fake_useragent import UserAgent
from scrapy import signals
from collections import deque
import time
from oauthlib.oauth1 import Client as Oauth1Client
from oauthlib.oauth2 import InsecureTransportError
from oauthlib.oauth2 import WebApplicationClient as Oauth2Client
from scrapy.exceptions import NotConfigured


class TwitterTweetsSpiderMiddleware(object):
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


class TwitterTweetsDownloaderMiddleware(object):
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

    def process_request(self, request, spider):

        spider.logger.info("subtitleSpiderMiddleware process_request: request=%s, spider=%s", request, spider)

        request.meta["proxy"] = "https://127.0.0.1:1080"

        spider.logger.info("request.meta %s", request.meta)


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

"""twitter开发者Api认证中间件"""
class HttpOAuth1Middleware(object):

    @classmethod
    def from_crawler(cls, crawler):
        o = cls()
        crawler.signals.connect(o.spider_opened, signal=signals.spider_opened)
        return o

    def spider_opened(self, spider):
        tokens = getattr(spider, 'oauth_token_list', None)
        self.check_response = getattr(spider, 'oauth_check_response_func', self.default_check_response)
        self.REQUEST_WINDOW_SIZE_MINS = getattr(spider, 'oauth_request_windows_size_mins', 0)

        if tokens is None:
            raise NotConfigured
        self.tokens_live = deque()
        self.tokens_dead = deque(zip(tokens, [float('-inf')] * len(tokens)))

    def process_request(self, request, spider):
        """获取令牌"""
        token, requests_done = self._obtain_token(spider)

        if token is None:
            return request

        auth = Oauth1Client(
            client_key=token['consumer_key'],
            client_secret=token['consumer_secret'],
            resource_owner_key=token['access_token'],
            resource_owner_secret=token['access_token_secret'])

        uri, headers, body = auth.sign(request.url)
        request.headers['Authorization'] = [headers['Authorization']]

        request.meta['oauth'] = True
        request.meta['token'] = token

    def process_response(self, request, response, spider):

        oauth_used = request.meta.get('oauth', False)

        if oauth_used:
            token_dead, retry_request = self.check_response(response)

            token = request.meta['token']
            if token_dead:
                self.tokens_dead.append((token, time.time()))
            else:
                requests_succeed = request.meta['token_requests_succeed']
                requests_succeed += 1
                self.tokens_live.append((token, requests_succeed))

            if retry_request:
                del request.meta['token']
                del request.meta['oauth']
                return request
            else:
                return response

    def default_check_response(self, response):
        return True, False

    def _dead_token_time_left(self):

        if len(self.tokens_dead) > 0:
            cred, time_expired = self.tokens_dead[0]
            time_left = self.REQUEST_WINDOW_SIZE_MINS * 60 - (time.time() - time_expired)
            time_left = time_left if time_left > 0 else 0
            return time_left
        else:
            return float('inf')

    def _obtain_token(self, spider):

        if len(self.tokens_live) == 0 and self._dead_token_time_left() > 0:
            return None, None

        if len(self.tokens_live) > 0:
            token, requests_succeed = self.tokens_live.popleft()
        else:
            token, _ = self.tokens_dead.popleft()
            requests_done = 0

        return token, requests_done


