# Redis数据库地址
REDIS_HOST = '172.16.20.252'

# Redis端口
REDIS_PORT = 6379

# Redis密码，如无填None
REDIS_PASSWORD = None

# 产生器使用的浏览器
BROWSER_TYPE = 'Chrome'

# 产生器类，如扩展其他站点，请在此配置
GENERATOR_MAP = {
    'twitter': 'TwitterCookiesGenerator'
}

# 测试类，如扩展其他站点，请在此配置
TESTER_MAP = {
    'twitter': 'TwitterValidTester'
}

TEST_URL_MAP = {
    'twitter': 'https://twitter.com/aizong/followers'
}

# 产生器和验证器循环周期
CYCLE = 10

# API地址和端口
API_HOST = '0.0.0.0'
API_PORT = 5000

# 产生器开关，模拟登录添加Cookies
GENERATOR_PROCESS = False
# 验证器开关，循环检测数据库中Cookies是否可用，不可用删除
VALID_PROCESS = False
# API接口服务
API_PROCESS = True
