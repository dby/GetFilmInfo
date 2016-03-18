#coding:utf-8

'''
    豆瓣网站抓取电影信息
'''

import re
import ast
import sys
import time
import random
import requests
from lxml import html

class FilmSpider:

    baseUrl = "http://movie.douban.com/"
    choseMovieUrl = "http://movie.douban.com/j/search_subjects?type=movie" 
    choseTVUrl = "http://movie.douban.com/tv/"
    rankingListUrl = "http://movie.douban.com/chart"
    bestUrl = "http://movie.douban.com/review/"

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

    '''
        爬取正在热映的电影
    '''
    def getOnShowFilms(self):
        headers = {'User-Agent': random.choice(self.user_agents)}
        onShowFilms = []
        r = requests.get(self.baseUrl)
        doc = html.document_fromstring(r.text)
        lis = doc.xpath('//li[@class="ui-slide-item"]')
        for li in lis:
            film = {}
            film["title"] = li.xpath('@data-title')
# 排除空
# title--电影名称 release--上映日期 rate--评分 star--获得星的数目 trailer--预告片的地址
# ticket--网上购票的地址 duration--电影时间 region--地区 director--导演 actors--演员
# rater--投票人数 href--详细介绍的链接 cover--电影照片
            if not len(film["title"]): continue
            film["title"] = film["title"][0]
            film["release"] = li.xpath('@data-release')[0]
            film["rate"] = li.xpath('@data-rate')[0]
            film["star"] = li.xpath('@data-star')[0]
            film["trailer"] = li.xpath('@data-trailer')[0]
            film["ticket"] =li.xpath('@data-ticket')[0]
            film["duration"] = li.xpath('@data-duration')[0]
            film["region"] = li.xpath('@data-region')[0]
            film["director"] = li.xpath('@data-director')[0]
            film["actors"] = li.xpath('@data-actors')[0]
            film["rater"] = li.xpath('@data-rater')[0]
            film["href"] = li.xpath('.//li[@class="title"]')[0].xpath('.//a')[0].xpath('@href')[0]
            a = li.xpath('.//img')[0]
            film["cover"] = a.xpath('@src')[0]
            onShowFilms.append(film)
        
        return onShowFilms

    '''
        按照类别爬取电影
    '''
    def getSpecifiedFilms(self, tag, sort,  page_limit, page_start):
# eval不支持null, true, false等，没法正确得转换为None, True, False等
# 一个解决办法就是，定义一个全局变量，再去调用eval，就可以正常使用了
        false="False"
        true="True"
        global false, true
# 设置代理
        headers = {'User-Agent': random.choice(self.user_agents)}
        url = self.choseMovieUrl + "&tag=" + (tag) + "&sort=" + (sort) + "&page_limit=" + str(page_limit) + "&page_start=" + str(page_start)
        r = requests.get(url)
        if r.status_code == requests.codes.ok:
            s = eval(r.text)
            return s["subjects"]
        else:
            return {"error":{"error_code":"1", "error_msg":str(r.status_code)}}

    '''
        按照类别电视剧
    '''
    def getSpecifiedTVs(self, type):
        onShowFilms = []
        url = self.choseTVUrl + "?type=" + str(type)
        r = requests.get(url)
        if r.status_code == requests.codes.ok:
            doc = html.document_fromstring(r.text)
            trs = doc.xpath('//tr[@class="item"]')
            for tr in trs:
                film = {}
                a1 = tr.xpath('.//a[@class="nbg"]')[0]
# href--链接，，title--电影名称，，cover--电影海报，，detail--电影简介
                film["href"] = a1.xpath("@href")[0]
                film["title"] = a1.xpath("@title")[0]
                img = a1.xpath('.//img')[0]
                film["cover"] = img.xpath("@src")[0]
                
                p = tr.xpath('.//p[@class="pl"]')[0]
                film["detail"] = p.text
                onShowFilms.append(film)

            return onShowFilms
    '''
        豆瓣电影排行榜
    '''
    def getRankingList(self):
        onShowFilms = []
        url = self.rankingListUrl
        r = requests.get(url)
        if r.status_code == requests.codes.ok:
            doc = html.document_fromstring(r.text)
            trs = doc.xpath('//tr[@class="item"]')
            for tr in trs:
                film = {}
                a1 = tr.xpath('.//a[@class="nbg"]')[0]
                film["href"] = a1.xpath('@href')[0]
                film["title"] = a1.xpath('@title')[0]
                img = a1.xpath('.//img')[0]
                film["cover"] = img.xpath("@src")[0]
                
                p = tr.xpath('.//p[@class="pl"]')[0]
                film["detail"] = p.text

                rating_nums = tr.xpath('.//span[@class="rating_nums"]')[0]
                film["rate"] = rating_nums.text

                onShowFilms.append(film)
            
            return onShowFilms
    
    '''
        豆瓣 获得影评
    '''
# review_title--影评标题 review_href--影评链接 film_href--电影链接 film_title--电影标题
# film_cover--电影海报 review_author_name--影评作者 review_author_profile--影评作者界面
# review_short--影评简述
    def getBestReview(self, page, _type):
        onReviews = []
        url = self.bestUrl + str(_type)  + "/?start=" + str(_type*10)
        #url = "https://movie.douban.com/review/best/"
        print url
        r = requests.get(url)
        if r.status_code == requests.codes.ok:
            doc = html.document_fromstring(r.text)
            uls = doc.xpath('//ul[@class="tlst clearfix"]')
            for ul in uls:
                review = {}
                a1 = ul.xpath('.//li[@class="nlst"]')[0].xpath('.//a')[2]
                review["review_title"] = a1.xpath('@title')[0]
                review["review_href"] = a1.xpath('@href')[0]
                a2 = ul.xpath('.//li[@class="ilst"]')[0].xpath('.//a')[0]
                review["film_href"] = a2.xpath('@href')[0]
                review["film_title"] = a2.xpath('@title')[0]
                review["film_cover"] = a2.xpath('.//img')[0].xpath('@src')[0]
                a3 = ul.xpath('.//li[@class="clst report-link"]')[0].xpath('.//a')[0]
                review["review_author_name"] = a3.text
                review["review_author_profile"] = a3.xpath("@href")[0]

                spans = ul.xpath('.//li[@class="clst report-link"]')[0].xpath('.//div[@class="review-short"]')[0].xpath('.//span')
                review_short = ""
                for i in range(len(spans)):
                    review_short += str(spans[i].text)
                review["review_short"] = review_short
                onReviews.append(review)
            
            print onReviews
            return onReviews

    def getFilmDetailMsg(self, id):
        '''获得电影的详细信息'''
        detailMsg = {}
        url = "http://movie.douban.com/subject/" + str(id) + "/?from=showing"
        r = requests.get(url)
        if r.status_code == requests.codes.ok:
            doc = html.document_fromstring(r.text)
            aPic = doc.xpath('.//div[@id="mainpic"]')[0].xpath('.//a[@class="nbgnbg"]')[0]
#海报，海报链接
            detailMsg["cover_link"] = aPic.xpath('@href')[0]
            detailMsg["cover"] = aPic.xpath('.//img')[0].xpath('@src')[0]

            info = doc.xpath('.//div[@id="info"]')[0]
#导演
            director = info.xpath('.//span[@class="attrs"]')[0].xpath('.//a')[0]
            detailMsg["director"] = director.text
#编剧
            filmWriter = info.xpath('.//span[@class="attrs"]')[1].xpath('.//a')[0]
            detailMsg["filmwriter"] = filmWriter.text
#演员
            actors = info.xpath('.//span[@class="actor"]')[0].xpath('.//span[@class="attrs"]')[0].xpath('.//a')
            actors_str = ""
            for actor in actors:
                actors_str = actor.text + "/" + actors_str
            detailMsg["actors"] = actors_str
#类型
            types = info.xpath('.//span[@property="v:genre"]')
            typeStr = ""
            for type in types:
                typeStr = type.text + "/" + typeStr
            detailMsg["type"] = typeStr

#制作国家/地区
            pat = re.compile('''\<span class\=\"pl\"\>制片国家\/地区\:\<\/span\>[^\<]+\<br''')
            res = pat.findall(r.content)[0]
            res = res[res.find("</span>")+7 : len(res)-3]
            detailMsg["region"] = res

#语言
            pat = re.compile('''\<span class\=\"pl\"\>语言\:\<\/span\>[^\<]+\<br''')
            res = pat.findall(r.content)[0]
            res = res[res.find("</span>")+7 : len(res)-3]
            detailMsg["language"] = res

#上映日期
            release = info.xpath('.//span[@property="v:initialReleaseDate"]')[0]
            detailMsg["release"] = release.text

#片长
            runtime = info.xpath('.//span[@property="v:runtime"]')[0]
            detailMsg["duration"] = runtime.text

#又名
            pat = re.compile('''\<span class\=\"pl\"\>又名\:\<\/span\>[^\<]+\<br''')
            res = pat.findall(r.content)[0]
            res = res[res.find("</span>")+7 : len(res)-3]
            detailMsg["anothername"] = res
            
#评星
            interestDiv = doc.xpath('//div[@class="rating_wrap clearbox"]')[0]
            rateStrong = interestDiv.xpath('.//strong[@class="ll rating_num"]')[0]
            detailMsg["strong"] = rateStrong.text

#投票人数
            numSpan = interestDiv.xpath('.//span[@property="v:votes"]')[0]
            detailMsg["votes_num"] = numSpan.text

#五星比例
            pat = re.compile('''\<div class\=\"power\"[^\<].*\<br''')
            res = pat.findall(r.content)
            print res
            #res = res[res.find("</span>")+45 : len(res)-3].strip()
            #detailMsg["fivestar"] = res

#四星比例
            #pat = re.compile('''\<div class\=\"power\" style\=\"width:60px\"\>\<\/div\>[^\<]+\<br''')
            #res = pat.findall(r.content)[0]
            #res = res[res.find("</span>")+45 : len(res)-3].strip()
            #detailMsg["fourstar"] = res

#三星比例 有点问题
            #pat = re.compile('''\<div class\=\"power\" style\=\"width:46px\"\>\<\/div\>[^\<]+\<br''')
            #res = pat.findall(r.content)
            #res = res[res.find("</span>")+45 : len(res)-3].strip()
            #print len(res)
            #detailMsg["threestar"] = ""

#二星比例
            #pat = re.compile('''\<div class\=\"power\" style\=\"width:8px\"\>\<\/div\>[^\<]+\<br''')
            #res = pat.findall(r.content)[0]
            #res = res[res.find("</span>")+45 : len(res)-3].strip()
            #detailMsg["twostar"] = res

#一星比例
            #pat = re.compile('''\<div class\=\"power\" style\=\"width:4px\"\>\<\/div\>[^\<]+\<br''')
            #res = pat.findall(r.content)[0]
            #res = res[res.find("</span>")+45 : len(res)-3].strip()
            #detailMsg["onestar"] = res

#剧情介绍
            intro = doc.xpath('//span[@property="v:summary"]')[0]
            detailMsg["intro"] = intro.text.strip()

#剧照
            detailMsg["covers"] = self.getFilmPhotos(id)
            return detailMsg

    def getFilmPhotos(self, id):
        '''获得电影剧照'''
        '''id--电影ID，唯一的'''
        photos = []
        url = "http://movie.douban.com/subject/" + str(id) +"/all_photos"
        r = requests.get(url)
        if r.status_code == requests.codes.ok:
            doc = html.document_fromstring(r.text)
            lis = doc.xpath('.//ul[@class="pic-col5"]')[1].xpath('.//li')
            for li in lis:
                photos.append(li.xpath('.//a')[0].xpath('.//img')[0].xpath('@src')[0])

            lis = doc.xpath('.//ul[@class="pic-col5"]')[0].xpath('.//li')
            for li in lis:
                photos.append(li.xpath('.//a')[0].xpath('.//img')[0].xpath('@src')[0])

            return photos

    def getEssay(self, id, start, limit, sort):
        '''' 获得电影的短评 '''
        ''' author_name--短评作者 essay_content--短评内容 essay_time--短评时间 essay_vote--短评票数 author_img--作者头像'''
        essay = []
        url = "http://movie.douban.com/subject/" + str(id) + "/comments?start=" + str(start) + "&limit=" + str(limit) + "&sort=" + str(sort)
        r = requests.get(url)
        if r.status_code == requests.codes.ok:
            doc = html.document_fromstring(r.text)
            divs = doc.xpath('//div[@class="comment-item"]')
            for div in divs:
                msg = {}
                aInfo = div.xpath('.//div[@class="avatar"]')[0].xpath('.//a')[0]
                msg["author_name"] = aInfo.attrib["title"]
                msg["author_img"] = aInfo.xpath('.//img')[0].attrib["src"]
                msg["essay_vote"] = div.xpath('.//span[@class="votes pr5"]')[0].text
                try:
                	time = div.xpath('.//span[@class="comment-info"]')[0].xpath('.//span')[1]
                	msg["essay_time"] = time.text.strip()
                except:
                    msg["essay_time"] = "one day"
                msg["essay_content"] = div.xpath('.//div[@class="comment"]')[0].xpath('.//p')[0].text.strip()
                essay.append(msg)

            return essay

    def getReviews(self, id, score, start, limit, sort):
        '''获得某一电影的影评'''
        '''id--电影ID score--几星影评 start--从第几个开始爬取 limit--爬取的个数 sort--排列方式'''
        reviews = []
        url = "http://movie.douban.com/subject/" +str(id) + "/reviews?sort=" + str(sort) + "&filter=&score=" + str(score) + "&limit=" + str(limit)
        r = requests.get(url)
        if r.status_code == requests.codes.ok:
            doc = html.document_fromstring(r.text)
            divs = doc.xpath('//div[@class="review"]')
            for div in divs:
                review = {}
                aInfo = div.xpath('.//div[@class="review-hd"]')[0].xpath('.//a')
#作者名
                review["author_name"] = aInfo[0].attrib["title"]
#作者头像
                review["author_img"] = aInfo[0].xpath('.//img')[0].attrib["src"]
#影评内容
                detail_url = div.xpath('.//div[@class="review-hd-expand"]')[0].xpath('.//a')[0].attrib["href"]
                review["review_content"] = self.getDetailReview(detail_url)
#影评标题
                title = div.xpath('.//div[@class="review-hd"]')[0].xpath('.//a')[3].attrib["title"]
                review["review_title"] = title
#时间 未完成
                pat = re.compile('''\<a href\=\"http\:\/\/movie\.douban\.com\/people\/35986570\/\" class\>[^\<]+\<span''')
                res = pat.findall(r.content)
                #res = res[res.find("</span>")+7 : len(res)-3]
                #detailMsg["anothername"] = res
                reviews.append(review)

            return reviews

    def getDetailReview(self, url):
        r = requests.get(url)
        if r.status_code == requests.codes.ok:
            doc = html.document_fromstring(r.text)
            div = doc.xpath('//div[@property="v:description"]')[0]
            return div.text_content()
        else:
            return ""

    def getRealTimeTickets(self):
        url = "http://www.cbooo.cn/realtime"
        headers = {'User-Agent': random.choice(self.user_agents)}
        r = requests.get(url, headers = headers)
        if r.status_code == requests.codes.ok:
            print r.text
            doc = html.document_fromstring(r.text)
            tds = doc.xpath('//td[@class="one"]')
            print len(tds)


if __name__ == '__main__':

    reload(sys)
    sys.setdefaultencoding("utf-8")

    print FilmSpider().getOnShowFilms()
    #FilmSpider().getSpecifiedFilms("热门", "time", 20, 0)
    #print FilmSpider().getSpecifiedTVs(7)
    #FilmSpider().getRankingList()
    #FilmSpider().getBestReview(1, "best")
    #FilmSpider().getFilmDetailMsg("http://movie.douban.com/subject/25895276/?from=showing")
    #FilmSpider().getFilmPhotos(25723907)
    #FilmSpider().getEssay(25723907, 0, 20, "new_score")
    #FilmSpider().getReviews(25723907, 5, 0, 20, "")
    #FilmSpider().getDetailReview("http://movie.douban.com/review/7521054/")

    #FilmSpider().getRealTimeTickets()


