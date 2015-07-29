## film

已经部署到新浪云平台sae上，目前已经实现的功能有:  
1. 选电影
2. 电视剧(电视剧排行榜)
3. 排行榜(电影排行榜)
4. 影评(最受欢迎的影评)

## API
1. 正在上映的电影  
请求url: http://myfilms.sinaapp.com/onshowingfilms/
请求参数: 无    
返回参数:   
```python
    参数名称            类型        示例值                                                                          描述
    star                String      "00"                                                                            "星"
    title               String      "捉妖记"                                                                        "电影标题"
    region              String      "中国大陆"                                                                      "地区"
    cover               String      "http://img4.douban.com/view/movie_poster_cover/mpst/public/p2257944916.jpg"    "电影海报"
    director            String      "许诚毅"                                                                        "导演"
    duration            String      "118分钟"                                                                       "电影放映时间"
    rate                String      "7.3"                                                                           "评分"
    href                String      "http://movie.douban.com/subject/25723907/?from=showing"                        "电影详细链接"
    actors              String      "白百何 / 井柏然 / 姜武"                                                        "演员"
    rater               String      "74281"                                                                         "投票人数"
    release             String      "2015"                                                                          "上映时间"
    ticket              String      "http://movie.douban.com/subject/25723907/cinema/"                              ""
    trailer             String      "http://movie.douban.com/subject/25723907/trailer"                              "电影海报"
```
