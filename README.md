## film

已经部署到新浪云平台sae上，目前已经实现的功能有:  
1. 选电影  
2. 电视剧(电视剧排行榜)  
3. 排行榜(电影排行榜)   
4. 影评(最受欢迎的影评)  

## API
###正在上映的电影  
请求url: http://myfilms.sinaapp.com/onshowingfilms/
请求参数: 无    
返回数据类型: JSON
返回参数:   
```python
    参数名称     类型        示例值                                                                          描述
    star         String      00                                                                              星
    title        String      捉妖记                                                                          电影标题
    region       String      中国大陆                                                                        地区
    cover        String      http://img4.douban.com/view/movie_poster_cover/mpst/public/p2257944916.jpg      电影海报url
    director     String      许诚毅                                                                          导演
    duration     String      118分钟                                                                         电影放映时间
    rate         String      7.3                                                                             评分
    href         String      http://movie.douban.com/subject/25723907/?from=showing                          电影详细链接
    actors       String      白百何 / 井柏然 / 姜武                                                          演员
    rater        String      74281                                                                           投票人数
    release      String      2015                                                                            上映时间
    ticket       String      http://movie.douban.com/subject/25723907/cinema/                                ""
    trailer      String      http://movie.douban.com/subject/25723907/trailer                                电影海报
```

---


###选电影  
请求url: http://myfilms.sinaapp.com/choosefilms/  
请求参数:   
```python
    参数名称     类型        示例值                     描述
    tag          String      热门/最新/经典...          选择电影的类型
    sort         String      recommend/time/rank        排序类型 热度/时间/评价
    page_limit   Integer     20                         每次爬取的数目
    page_start   Integer     0                          从第几项开始爬
```
返回数据类型: JSON
返回参数:
```python
    参数名称    类型        示例值                                                                          描述
    rate        String      4.2                                                                             评分
    title       String      捉妖记                                                                          电影标题
    url         String      http://movie.douban.com/subject/25905746/                                       电影详细链接
    is_new      String      True                                                                            是不是最新电影
    cover       String      http://img4.douban.com/view/movie_poster_cover/lpst/public/p2256870906.jpg      电影海报url
    id          String      25905746                                                                        区分不同电影，唯一
```
示例: http://myfilms.sinaapp.com/choosefilms/?tag="热门"&sort=recommend&page_limit=20&page_start=0    
note:   
    url/cover链接需要转化一下  
    tag取值: 热门/最新/经典/可播放/豆瓣高分/冷门佳片/华语/欧美/韩国/日本/动作/喜剧/爱情/科幻/悬疑/恐怖/治愈/  


---


###电视剧  
请求url: http://myfilms.sinaapp.com/choosetvs/
请求参数:   
```python
    参数名称            类型        示例值                            描述
    type                Integer     1/2/3/4/5/6/7     全部/美剧/英剧/韩剧/大陆电视剧/港剧/日剧/动漫
```
返回数据格式: JSON  
返回参数:  
```python
    参数名称    类型        示例值                                                                          描述
    href        String      http://movie.douban.com/subject/25826612/                                       电视剧详细信息url
    cover       String      http://img3.douban.com/view/movie_poster_cover/ipst/public/p2230256732.jpg      电视剧海报url
    detail      String      2015-04-12(美国) / 艾米莉亚·克拉克 / 彼特·丁拉                                电视剧详细信息
    title       String      冰与火之歌：权力的游戏 第五季 / 王座游戏 第五季                                 电视剧名称
```
示例url: http://myfilms.sinaapp.com/choosetvs/?type=1                                                        
                                                                                                           

---


###排行榜  
请求url: http://myfilms.sinaapp.com/rankinglist/   
请求参数: 无
返回数据格式: JSON
返回参数:  
```python
    参数名称    类型        示例值                                                                          描述
    rate        String      7.9                                                                             评分
    href        String      http://img3.douban.com/view/movie_poster_cover/ipst/public/p2205014862.jpg      电影海报
    detail      String      2015-01-31(日本)...                                                             电影简介
    title       String      深夜食堂                                                                        电影名称

```
示例URL: http://myfilms.sinaapp.com/rankinglist/   


---


###最受欢迎/最近的影评  
请求url: http://myfilms.sinaapp.com/bestreview/  
请求参数:  
```python
    参数名称    类型        示例值                  描述
    page        String      0/1/2                   页数
    type        String      best/latest             最受欢迎的/最新的
```
返回数据格式: JSON  
返回参数:
```python
    参数名称                类型        示例值                                                                          描述
    film_href               String      http://movie.douban.com/subject/24879839/                                       电影链接
    film_title              String      道士下山                                                                        电影名称
    film_cover              String      http://img3.douban.com/view/movie_poster_cover/ipst/public/p2251450614.jpg      电影海报url
    review_href             String      http://movie.douban.com/review/7551733/                                         影评地址
    review_short            String      ...                                                                             简短影评(不全)
    review_title            String      请勿向西湖投掷垃圾                                                              影评名称
    review_author_profile   String      http://movie.douban.com/people/petitespot/                                      影评作者主页
    review_author_name      String      小斑                                                                            影评作者名称
```
示例URL: http://myfilms.sinaapp.com/bestreview/?type=best&page=0   


---


###某一电影具体信息   
请求url: 
请求参数:
返回数据格式:
返回参数:
示例URL:

###某一电影的短评  
请求url: 
请求参数:
返回数据格式:
返回参数:
示例URL:

###某一电影的影评  
请求url: 
请求参数:
返回数据格式:
返回参数:
示例URL:
