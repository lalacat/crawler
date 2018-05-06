from twisted.internet.defer import inlineCallbacks,Deferred,returnValue
from twisted.internet import reactor,defer,task
import requests
from lxml import etree

header = { 'User-Agent' :'MMozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0'
            ,'content-type':"application/json"}

def request(url):
    result = requests.get(url,headers=header)
    return result


def read_url(request):
    #print(result.text)
    result = etree.HTML(request.text)
    return result


@inlineCallbacks
def time_wasted_wrapper(job_id):
    import time
    t1 = time.time()
    print('begin time-wasted job '+str(job_id))
    #result = requests.get("https://www.smzdm.com/", headers=header)
    try:
      result = yield request("https://www.baidu.com/")
    except Exception as e :
        print(e)
    print('time-wasted job '+str(job_id)+' done!')
    t2 = time.time()
    print(t2-t1)
    print(result)

    r_s = etree.HTML(result.text)
    ul = r_s.xpath("body/div[@id='content']/div/div[@id='feed-wrap']/div"
                      "/div[@class='feed-main-con']/ul[@id='feed-main-list']")
    #produce_list = ul[0].xpath('./li')
    print(len(ul))
    t3 = time.time()
    print(t3-t2)

def all_jobs_done(result):
    print(str(result))
    print('all jobs are done!')
    reactor.stop()

def print_result1(result):
    print("print 1")
    for r in result:
        print(r.xpath('./h5/a/@href'))
    return

def install_jobs():
    job_list = list()
    for i in range(1):
        job = time_wasted_wrapper(i)
        job_list.append(job)
    deferred_list = defer.DeferredList(job_list)
    deferred_list.addCallback(print_result1)
    deferred_list.addCallback(all_jobs_done)

if __name__ == '__main__':
    job = time_wasted_wrapper(1)
    #job.addCallback(print_result1)
    job.__next__()
    job.addCallback(all_jobs_done)
    print('all job have started!')
    reactor.run()