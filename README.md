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
返回数据类型: JSON
返回参数:   
```python
    参数名称            类型        示例值                                                                          描述
    star                String      00                                                                              星
    title               String      捉妖记                                                                          电影标题
    region              String      中国大陆                                                                        地区
    cover               String      http://img4.douban.com/view/movie_poster_cover/mpst/public/p2257944916.jpg      电影海报url
    director            String      许诚毅                                                                          导演
    duration            String      118分钟                                                                         电影放映时间
    rate                String      7.3                                                                             评分
    href                String      http://movie.douban.com/subject/25723907/?from=showing                          电影详细链接
    actors              String      白百何 / 井柏然 / 姜武                                                          演员
    rater               String      74281                                                                           投票人数
    release             String      2015                                                                            上映时间
    ticket              String      http://movie.douban.com/subject/25723907/cinema/                                ""
    trailer             String      http://movie.douban.com/subject/25723907/trailer                                电影海报
```


2. 选电影  
请求url: http://myfilms.sinaapp.com/choosefilms/  
请求参数:   
```python
    参数名称            类型        示例值                                      描述
    tag                 String      热门/最新/经典...                           选择电影的类型
    sort                String      recommend/time/rank                         排序类型 热度/时间/评价
    page_limit          Integer     20                                          每次爬取的数目
    page_start          Integer     0                                           从第几项开始爬
```
返回数据类型: JSON
返回参数:
```python
    参数名称            类型        示例值                                                                          描述
    rate                String      4.2                                                                             评分
    title               String      捉妖记                                                                          电影标题
    url                 String      http://movie.douban.com/subject/25905746/                                       电影详细链接
    is_new              String      True                                                                            是不是最新电影
    cover               String      http://img4.douban.com/view/movie_poster_cover/lpst/public/p2256870906.jpg      电影海报url
    id                  String      25905746                                                                        区分不同电影，唯一
```
示例: http://myfilms.sinaapp.com/choosefilms/?tag="热门"&sort=recommend&page_limit=20&page_start=0    
note: url/cover链接需要转化一下

3. 排行榜  


4. 最受欢迎得影评  


5. 某一电影具体信息   

6. 某一电影的短评  

7. 某一电影的影评  
