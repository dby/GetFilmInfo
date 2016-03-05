#coding:utf-8

'''
    CBO中国票房  抓取电影信息
'''

import re
import ast
import sys
import time
import random
import requests
from lxml import html

from flask import Flask, g, request, abort, jsonify

class FilmSpiderCbooo:

    baseUrl = "http://cbooo.cn/"

    user_agents = [
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
        'Opera/9.25 (Windows NT 5.1; U; en)',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
        'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
        'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
        'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
        "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
        "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 ",
    ] 
    
    def getBoxOfficeHour(self):
        url = "http://www.cbooo.cn/boxOffice/GetHourBoxOffice/"
        headers = {'User_agent': random.choice(self.user_agents)}
        r = requests.get(url)
        return r.json()

    def getBoxOfficeDay(self, url):
        headers = {'User_agent': random.choice(self.user_agents)}
        r = requests.get(url)
        return r.json()

    def getBoxOfficeWeekend(self, url):
        headers = {'User_agent': random.choice(self.user_agents)}
        r = requests.get(url)
        return r.json()

    def getBoxOfficeWeek(self, url):
        headers = {'User_agent': random.choice(self.user_agents)}
        r = requests.get(url)
        return r.json()

    def getBoxOfficeMonth(self, url):
        headers = {'User_agent': random.choice(self.user_agents)}
        r = requests.get(url)
        return r.json()

    def getBoxOfficeYear(self, url):
        headers = {'User_agent': random.choice(self.user_agents)}
        r = requests.get(url)
        return r.json()

    def getBoxOfficeGlobal(self, url):
        headers = {'User_agent': random.choice(self.user_agents)}
        r = requests.get(url)
        return r.json()

    def getBoxOfficeNorthAmerica(self, url):
        headers = {'User_agent': random.choice(self.user_agents)}
        r = requests.get(url)
        return r.json()

    def getBoxOfficeHistory(self, url):
        headers = {'User_agent': random.choice(self.user_agents)}
        r = requests.get(url)
        return r.json()


if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding("utf-8")
    FilmSpiderCbooo().getBoxOffice("Hour")
