import time,json,pymongo,logging
from twisted.internet import reactor

def get_smzdm_datas(web_body):
    print("get_need_datas")
    datas_list = list()
    if isinstance(web_body,bytes):
        logging.info("body got is bytes")
        web_body = json.loads(web_body)
    else:
        print("data type is json")
    if isinstance(web_body,dict):
        if web_body.__contains__("data"):
            datas = web_body['data']
    else:
        print("data type is not dict")
    for d in datas:

        result = dict()
        #Python 3.X dict里不包含 has_key() 函数，被 __contains__(key) 替代:
        #标签是：z-tag-zixun 没有article_price，article_link，top_category

        if d.__contains__("article_id"):
            result["article_id"] = d["article_id"]
            if d.__contains__("article_title"):
                result["article_title"] = d["article_title"]

            if d.__contains__("article_price"):
                result["article_price"] = d["article_price"]

            if d.__contains__("article_mall"):
                result["article_mall"] = d["article_mall"]

            if d.__contains__("article_pic"):
                result["article_pic"] = d["article_pic"]

            if d.__contains__("article_link"):
                result["article_link"] = d["article_link"]

            if d.__contains__("article_url"):
                result["article_url"] = d["article_url"]

            if d.__contains__("article_channel_class"):
                result["article_channel_class"] = d["article_channel_class"]

            if d.__contains__("top_category"):
                result["top_category"] = d["top_category"]

            datas_list.append(result)

    return datas_list


def print_smzdm_result(datas_list,url):
    print("页面 :%s 有 %d 件商品"%(url,len(datas_list)))
    for d_l in datas_list:
        for p,d in d_l.items():
            print(p,d)
            pass
    print("==============================")

def end_crawl(_, t_begin):
    t_end = time.time()
    print(t_end - t_begin)
    reactor.stop()


class MongoDb(object):

    '''
    mongo_url = "127.0.0.1:27017"

    client = pymongo.MongoClient(mongo_url)

    # 连接到数据库myDatabase
    DATABASE = "Twisted_Database"
    db = client[DATABASE]

    # 连接到集合(表):myDatabase.myCollection
    COLLECTION = "getPage_Collection"
    db_coll = db[COLLECTION]
    '''

    def __init__(self,db_url,db_name):
        # mongodb服务的地址和端口号
        self.db_url = db_url
        #数据库的名称
        self.db_name = db_name
        #表名称
        self.collection_name = None

        print('正在连接数据库')
        #连接到数据库
        try :
            self.client = pymongo.MongoClient(self.db_url)
            self.dcolls = self.client[self.db_name]
        except Exception as e :
            print(e)
    '''
    def __new__(cls, *args, **kwargs):
        #单例模式，限制对象生成的次数
        if not hasattr(cls,"instance"):
            cls.instance = super(MongoDb,cls).__new__(cls)
        return cls.instance
    '''
    def connectDb(self):
        pass

    def _getCollection(self):
        if self.dcolls != None :
            return self.dcolls[self.collection_name]

    def insert_mongoDb(self,result):
        print("开始写入到表%s"%self.collection_name)
        if isinstance(result, list):
            for post in result:
                try:
                    self.dcolls[self.collection_name].insert_one(post)
                except Exception as e:
                    print(post,e)
            print("MongoDb update Finish")
        else:
            print(type(result)+"数据类型不对，传入list类型数据")
        #return result