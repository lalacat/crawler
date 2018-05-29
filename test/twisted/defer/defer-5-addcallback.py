from twisted.internet import defer
from twisted.internet import task
from twisted.internet import reactor
import requests
from bs4 import BeautifulSoup
from lxml import etree

header = { 'User-Agent' :'MMozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0'
            ,'content-type':"application/json"}


def time_wasted_wrapper(job_id):
    def request():
        print('time-wasted job '+str(job_id)+' done!')
        result = requests.get("https://www.smzdm.com/",headers=header)
        return result
    print('begin time-wasted job '+str(job_id))
    # 返回一个deferred对象，真实情况下，这里可能是一个直接返回deferred对象的函数，也可能是一个正常阻塞函数，但是你可以用
    # deferToThread来获得一个deferred对象
    return task.deferLater(reactor, 3, request)

def read_url(request):
    #print(result.text)
    result = etree.HTML(request.text)
    return result


def find_elements(result):
    print(type(result))

    #使用xpath返回的是list类型的数据
    ul = result.xpath("body/div[@id='content']/div/div[@id='feed-wrap']/div"
                          "/div[@class='feed-main-con']/ul[@id='feed-main-list']")
    produce_list = ul[0].xpath('./li')
    return produce_list

def print_result1(result):
    print("print 1")
    for r in result:
        print(r.xpath('./h5/a/@href'))
    return

def print_result2(result):
    print("print 2")
    for r in result:
        print(r.xpath('./h5/a/@href'))
    return result

#defer的回调函数必须有参数
def all_jobs_done(_):
    print('all jobs are done!')
    reactor.stop()


jobs = list()

for i in range(1):
    job = time_wasted_wrapper(i)
    job.addCallback(read_url)
    job.addCallback(find_elements)
    job.addCallback(print_result1)
    #jobs.append(job)

defers = defer.DeferredList([job,])
defers.addCallback(all_jobs_done)

reactor.run()


