import pymongo
import queue

from twisted.internet import reactor

from test.framework.setting import Setting
from test.framework.test.test_crawler.test_crawlerRunner import CrawlerRunner

# mongodb服务的地址和端口号
mongo_url = "127.0.0.1:27017"

# 连接到mongodb，如果参数不填，默认为“localhost:27017”
client = pymongo.MongoClient(mongo_url)

#连接到数据库myDatabase
DATABASE = "LianJia"
db = client[DATABASE]

#连接到集合(表):myDatabase.myCollection
COLLECTION = "XiaoQu"
db_coll = db[COLLECTION ]

projectionFields = {'_id':False}  # 用字典指定
queryArgs = {"total_zone_name":"qingpu"}

searchRes = db_coll.find(queryArgs,{'_id':False})
'''

scheduler = searchRes.next()

db_flag = True


def task_scheduke_next(searchRes):
    try:
        result = searchRes.next()
    except StopIteration:
        result = None
    return result

top_task = queue.Queue()
def load_task(searchRes,top_task):
    next_task = task_scheduke_next(searchRes)
    if next_task:
        task_name = next_task["total_zone_name"][0]
        print(task_name)
        for name,url in next_task.items():
            if name != 'total_zone_name':
                top_task.put(url)
        load_task(searchRes,top_task)
    else:
        print("任务取完")


#load_task(searchRes,top_task)
#print(top_task.qsize())
'''



s = Setting()
cr = CrawlerRunner(searchRes,s)
d = cr.start()
d.addBoth(lambda _:reactor.stop())
reactor.run()

