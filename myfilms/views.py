#coding: utf-8

import json
import MySQLdb
from datetime import datetime
from myfilms import app
from flask import Flask, g, request, abort, jsonify

from sae.const import (MYSQL_HOST, MYSQL_HOST_S, MYSQL_PORT, MYSQL_USER, MYSQL_PASS, MYSQL_DB)

from filmSpider import *
from filmSpiderCbooo import *

import sys
reload(sys)
sys.setdefaultencoding("utf-8")


filmType = ["热门", "最新", "经典", "可播放", "豆瓣高分", "冷门佳片", "华语", "欧美", "韩国", "日本", "动作", "喜剧", "爱情", "科幻", "悬疑", "恐怖", "文艺"]
filmSort = ["recommend", "time", "rank"] #热度，时间，评价

tvType = {"全部":0, "美剧":1, "英剧":2, "韩剧":3, "大陆电视剧":4, "港剧":5, "日剧":6, "动漫":7}

@app.route("/")
def Hello():
    return "welcome to myfilms."

# 实时
@app.route("/boxofficehour/")
def BoxOfficeHour():
    return jsonify(data=FilmSpiderCbooo().getBoxOfficeHour())

# 日票房
@app.route("/boxofficeday/")
def BoxOfficeDay():
    if request.method == 'GET':
        num = request.args.get("num")
        url = "http://www.cbooo.cn/boxOffice/GetDayBoxOffice?num=" + num + "&d=1453651845015"
        return jsonify(data=FilmSpiderCbooo().getBoxOfficeDay(url))

# 周末票房
@app.route("/boxofficeweekend/")
def BoxOfficeWeekend():
    if request.method == 'GET':
        num = request.args.get("num")
        url = "http://www.cbooo.cn/boxOffice/getWeekendInfoData?selDate=2016-01-22%262016-01-24%7C2016-01-15%262016-01-17"
        return jsonify(data=FilmSpiderCbooo().getBoxOfficeWeekend(url))

# 月票房
@app.route('/boxofficemonth/')
def BoxOfficeMonth():
    if request.method == 'GET':
        sdate = request.args.get('sdate')
        url = "http://www.cbooo.cn/boxOffice/getWeekInfoData?sdate=" + sdate
        return jsonify(data=FilmSpiderCbooo().getBoxOfficeMonth(url))

# 年票房
@app.route('/boxofficeyear/')
def BoxOfficeYear():
    if request.method == 'GET':
        year = request.args.get('year')
        url = "http://www.cbooo.cn/year?year=" + year
        return jsonify(data=FilmSpiderCbooo().getBoxOfficeYear(url))

# 全球票房
@app.route('/boxofficeglobal/')
def BoxOfficeGlobal():
    if request.method == 'GET':
        weekId = request.args.get('weekId')
        url = "http://www.cbooo.cn/boxOffice/getAllInfo?weekId=" + weekId
        return jsonify(data=FilmSpiderCbooo().getBoxOfficeGlobal(url))

# 正在放映的电影
@app.route("/onshowingfilms/")
def OnShowingFilms():
    films = FilmSpider().getOnShowFilms()
    return jsonify(onshowingfilms=films)

@app.route("/choosefilms/")
def ChooseFilms():
    if request.method == 'GET':
        tag = request.args.get("tag")
        sort = request.args.get("sort")
        page_limit = request.args.get("page_limit")
        page_start = request.args.get("page_start")
        films = FilmSpider().getSpecifiedFilms(tag, sort, page_limit, page_start)
        return jsonify(onshowingfilms=films)

@app.route("/choosetvs/")
def ChooseTVs():
    if request.method == 'GET':
        type = request.args.get("type")
        tvs = FilmSpider().getSpecifiedTVs(type)
        return jsonify(onshowingtvs=tvs)

@app.route("/rankinglist/")
def RankingList():
    rankingList = FilmSpider().getRankingList()
    return jsonify(rankinglist=rankingList)

@app.route("/bestreview/")
def Review():
    if request.method == "GET":
        page = request.args.get("page")
        #_type = request.args.get("type")
        _type = "best"
        reviews = FilmSpider().getBestReview(page, _type)
        return jsonify(review=reviews)

@app.route("/film/")
def FilmDetailMsg():
    if request.method == "GET":
        id = request.args.get("id")
        film = FilmSpider().getFilmDetailMsg(id)
        return jsonify(film=film)

@app.route("/essay/")
def getEssay():
    if request.method == "GET":
        id = request.args.get("id")
        start = request.args.get("start")
        limit = request.args.get("limit")
        sort = request.args.get("sort")
        essay = FilmSpider().getEssay(id, start, limit, sort)
        return jsonify(essay=essay)

@app.route("/review/")
def getReviews():
    if request.method == "GET":
        id = request.args.get("id")
        start = request.args.get("start")
        limit = request.args.get("limit")
        sort = request.args.get("sort")
        score = request.args.get("score")
        reviews = FilmSpider().getReviews(id, score, start, limit, sort)
        return jsonify(reviews=reviews)
