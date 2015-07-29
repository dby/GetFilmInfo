#coding: utf-8

import json
import MySQLdb
from datetime import datetime
from myfilms import app
from flask import Flask, g, request, abort, jsonify

from sae.const import (MYSQL_HOST, MYSQL_HOST_S, MYSQL_PORT, MYSQL_USER, MYSQL_PASS, MYSQL_DB)

from filmSpider import *

filmType = ["热门", "最新", "经典", "可播放", "豆瓣高分", "冷门佳片", "华语", "欧美", "韩国", "日本", "动作", "喜剧", "爱情", "科幻", "悬疑", "恐怖", "文艺"]
filmSort = ["recommend", "time", "rank"] #热度，时间，评价

tvType = {"全部":0, "美剧":1, "英剧":2, "韩剧":3, "大陆电视剧":4, "港剧":5, "日剧":6, "动漫":7}

@app.route("/")
def Hello():
    return "welcome to myfilms."

@app.route("/onshowingfilms/")
def OnShowingFilms():
    films = FilmSpider().getOnShowFilms()
    return jsonify(onshowingfilms=films)

@app.route("/choosefilms/")
def ChooseFilms():
    films = FilmSpider().getSpecifiedFilms("热门", "time", 20, 0)
    return jsonify(onshowingfilms=films)

@app.route("/choosetvs/")
def ChooseTVs():
    tvs = FilmSpider().getSpecifiedTVs(1)
    return jsonify(onshowingtvs=tvs)

@app.route("/rankinglist/")
def RankingList():
    rankingList = FilmSpider().getRankingList()
    return jsonify(rankinglist=rankingList)

@app.route("/bestreview/")
def Review():
    page = 0
    reviews = FilmSpider().getBestReview(page)
    return jsonify(review=reviews)

@app.route("/film/")
def FilmDetailMsg():
    film = FilmSpider().getFilmDetailMsg("http://movie.douban.com/subject/25723907/?from=showing")
    return jsonify(film=film)

@app.route("/essay/")
def getEssay():
    essay = FilmSpider().getEssay(25723907, 0, 20, "new_score")
    return jsonify(essay=essay)

@app.route("/review/")
def getReviews():
    essay = FilmSpider().getReviews(25723907, 5, 0, 10, "")
    return jsonify(essay=essay)
