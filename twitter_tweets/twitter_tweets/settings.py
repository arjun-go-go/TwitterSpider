# -*- coding: utf-8 -*-

# Scrapy settings for twitter_tweets project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'twitter_tweets'

SPIDER_MODULES = ['twitter_tweets.spiders']
NEWSPIDER_MODULE = 'twitter_tweets.spiders'



#srapy_redis的配置
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
SCHEDULER_PERSIST = True
# REDIS_URL = "redis://:caojun@172.16.20.216:6379"

# SCHEDULER = "scrapy_redis_bloomfilter.scheduler.Scheduler"
# DUPEFILTER_CLASS = "scrapy_redis_bloomfilter.dupefilter.RFPDupeFilter"
# SCHEDULER_PERSIST = True

# 种子队列的信息
REDIS_URL = None
REDIS_HOST = 'xxxxxxx'
REDIS_PORT = 6379
REDIS_PARAMS = {"db":8}



LOG_LEVEL = "DEBUG"



# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'twitter_tweets (+http://www.yourdomain.com)'
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'


# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 20

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 0.8
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

DEFAULT_REQUEST_HEADERS = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
  'Accept-Language': 'zh-CN,zh;q=0.9',
    "accept-encoding": "gzip, deflate, br"
}


MYEXT_ENABLED = True
IDLE_NUMBER = 720

EXTENSIONS= {
   'twitter_tweets.extensions.RedisSpiderSmartIdleClosedExensions': 500
}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'twitter_tweets.middlewares.TwitterTweetsSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    # 'twitter_tweets.middlewares.RandomUserAgentMiddlware': 1,
    'twitter_tweets.middlewares.RandomProxyMiddleware': 100,
    # 'twitter_tweets.middlewares.JavaScriptMiddleware': 200,
    # 'twitter_tweets.middlewares.JSPageMiddleware': 300,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   # 'twitter_tweets.pipelines.TwitterTweetsPipeline': 300,
   #  'twitter_tweets.pipelines.MysqlTwistedPipline': 100,
   # 'twitter_tweets.pipelines.Neo4jPipline': 100,
   'twitter_tweets.pipelines.MongoPipeline': 100,
}


import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, 'twitter_tweets'))


RANDOM_UA_TYPE = "random"



# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'



MYSQL_HOST = "xxxxxx"
MYSQL_DBNAME = "twitter"
MYSQL_USER = "xxxxxx"
MYSQL_PASSWORD = "stark"

MYSQL_HOST_1 = 'xxxxxxx'
MYSQL_DBNAME_1 = 'twitter'
MYSQL_USER_1 = 'xxxxx'
MYSQL_PASSWORD_1 = 'xxxxx'








