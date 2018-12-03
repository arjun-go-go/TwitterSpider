import random
import time
from io import BytesIO
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from os import listdir
from os.path import abspath, dirname
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class TwitterCookies():
    def __init__(self, username, password,browser):
        self.url = 'https://twitter.com/login'
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--disable-gpu')
        # self.browser = webdriver.Chrome()
        self.browser = browser
        self.wait = WebDriverWait(self.browser, 10)
        self.username = username
        self.password = password
    
    def open(self):
        """
        打开网页输入用户名密码并点击
        :return: None
        """
        self.browser.delete_all_cookies()
        self.browser.get(self.url)
        time.sleep(random.randint(2, 6))
        self.browser.find_element_by_xpath(
            "//div[@class='clearfix field']/input[@name='session[username_or_email]']").send_keys(self.username)
        time.sleep(random.randint(2, 6))

        self.browser.find_element_by_xpath(
            "//div[@class='clearfix field']/input[@name='session[password]']").send_keys(self.password)
        time.sleep(random.randint(2, 5))
        self.browser.find_element_by_xpath("//div[@class='clearfix']/button[@type='submit']").click()



    def login_successfully(self):
        """
        判断是否登录成功
        :return:
        """
        try:
            return bool(
                WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'DashUserDropdown-userInfo'))))
        except TimeoutException:
            return False

    def get_cookies(self):
        """
        获取Cookies
        :return:
        """
        return self.browser.get_cookies()
    
    def main(self):
        """
        破解入口
        :return:
        """
        self.open()
        if self.login_successfully():
            cookies = self.get_cookies()
            return {
                'status': 1,
                'content': cookies
            }
        else:
            return {
                'status': 2,
                'content': '登陆出错'
            }


if __name__ == '__main__':
    result = TwitterCookies('starksaya', 'xxxxxx').main()
    print(result)
