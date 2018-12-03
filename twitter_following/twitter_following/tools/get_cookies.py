# -*- coding: utf-8 -*-
# @Time : 2018/10/16 19:24
# @Author : Arjun
# @Site :  
# @File : get_cookies.py 
# @Software: PyCharm


class Cookie(object):

    def __init__(self,cookie):

        self.cookie = cookie

    def stringTodict(self):
        item = {}
        items = self.cookie.split(';')
        for i in items:
            key = i.split('=')[0].replace(' ','')
            value = i.split('=')[1]
            item[key] = value
        return item


if __name__ == '__main__':
    cookie = """xxxxxx"""
    trans = Cookie(cookie)
    print(trans.stringTodict())