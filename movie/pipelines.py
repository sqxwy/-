# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import time
import requests
from requests.exceptions import RequestException
import os
import json

headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer":"https://movie.douban.com/top250"
}
class MoviePipeline:
    def __init__(self):
        self.img_dir="douban_images"
        if not os.path.exists(self.img_dir):
             os.makedirs(self.img_dir)
        self.filename="data.json"
        self.movie_list=[]


    def process_item(self, item, spider):
            lb={"img_url" : "", "name" : "", "score" : "", "infro" : "", "img_path" : ""}
            img_url=item.get('img_url','')
            title=item.get('movieTitleCn','').strip()
            score=item.get('score','').strip()
            infro=item.get('infro','').strip()
            lb["name"]=title.replace(" ","")
            lb["infro"]=infro.replace(" ","")
            lb["score"]=score
            lb["img_url"]=img_url
            safe_title=title.replace('/','_').replace('\\','_').replace('：','_')
            img_path=os.path.join(self.img_dir,f"{safe_title}.jpg")
            max_retries=2
            if os.path.exists(img_path) and os.path.getsize(img_path) > 1024*5:
                spider.logger.info(f"图片已存在:{title}")
                lb["img_path"]=img_path
                self.movie_list.append(lb)
                return item
            for i in range(max_retries):
                try:
                    spider.logger.info(f"开始第{i+1}次下载:{title} 图片地址:{img_url}")
                    response=requests.get(img_url, headers=headers, timeout=10, stream=True)
                    response.raise_for_status()
                    with open(img_path, "wb") as f:
                         for chunk in response.iter_content(chunk_size=1024):
                              if chunk:
                                   f.write(chunk)
                    if os.path.getsize(img_path) > 5*1024:
                         spider.logger.info(f"图片下载成功:{title} 图片地址:{img_path}")
                         lb["img_path"]=img_path
                         break
                    else:
                         os.remove(img_path)
                         spider.logger.warning(f"图片下载无效,准备重试:{title}")
                except RequestException as e:
                    spider.logger.error(f"第{i+1}次下载失败:{title}")
                    if i == max_retries -1 :
                         if os.path.exists(img_path):
                              os.remove(img_path)
                              spider.logger.error(f"图片最终下载失败:{title}")
                         else:
                              time.sleep(2)
            self.movie_list.append(lb)
            return item
    def close_spider(self,spider):
         with open(self.filename,"w",encoding="utf-8") as f:
              json.dump({"movie":self.movie_list}, f , ensure_ascii=False , indent=4)
              spider.logger.info(f"所有数据成功保存到:{self.filename} 共{len(self.movie_list)}条数据")
