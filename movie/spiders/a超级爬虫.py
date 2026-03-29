import scrapy
import time
from movie.myLog import MyLog
from ..items import MovieItem

class A超级爬虫Spider(scrapy.Spider):
    name = "超级爬虫"
    allowed_domains = ["douban.com"]#域的范围只能在这个里面爬行
    start_urls = ["https://movie.douban.com/top250"]#要爬取的网页

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.mylog=MyLog()

    def parse(self, response):
        count=1
        for movie in response.css('ol.grid_view div.item'):
            if count <= 50:
                item=MovieItem()
                item['movieTitleCn']=movie.css('span.title::text').get('')#电影名
                item['score']=movie.css('span.rating_num::text').get('')#电影评分
                item['infro']=movie.css('div.bd p::text').get('')#简介
                item['img_url']=movie.css('div.pic img::attr(src)').get('').strip()#图片
                yield item
                count+=1
                
                for page in range(1,11):
                    next_url=response.css(f'div.paginator:nth-child({page+1}) a::attr(href)').get('')
                    if next_url:
                        yield response.follow(next_url,self.parse)
            else:
                break