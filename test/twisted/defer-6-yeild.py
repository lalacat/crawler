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
    d =Deferred()
    reactor.callLater(2,d.callback,request("https://www.smzdm.com/"))

    result = yield d


    print('time-wasted job '+str(job_id)+' done!')
    t2 = time.time()
    print(t2-t1)

    d1 = Deferred()
    #r_s = etree.HTML(result.text)
   # print(r_s)
    reactor.callLater(2,d1.callback,read_url(result))

    #ul = r_s.xpath("body/div[@id='content']/div/div[@id='feed-wrap']/div"
    #                  "/div[@class='feed-main-con']/ul[@id='feed-main-list']")[0].xpath('./li')
    #produce_list = ul[0].xpath
    #print(len(ul))
    t3 = time.time()
    print(t3-t2)
    try:
        result = yield d1
    except Exception as e:
        print(e)
    print(result)
    returnValue(result)
    #reactor.stop()



def all_jobs_done(_):
   # print(str(result))
    print('all jobs are done!')
    reactor.stop()


def print_result1(result):
    print("print")
    ul = result.xpath("body/div[@id='content']/div/div[@id='feed-wrap']/div"
                      "/div[@class='feed-main-con']/ul[@id='feed-main-list']")
    print(ul)
    produce_list = ul[0].xpath('./li')
    for r in produce_list:
        print(r.xpath('./h5/a/@href'))
    return

'''
def install_jobs():
    job_list = list()
    for i in range(1):
        job = time_wasted_wrapper(i)
        job_list.append(job)
    deferred_list = defer.DeferredList(job_list)
    deferred_list.addCallback(print_result1)
    deferred_list.addCallback(all_jobs_done)
'''


if __name__ == '__main__':
    #job = time_wasted_wrapper(1)
    #job.addCallback(print_result1)
    #job.addCallback(all_jobs_done)
    #reactor.callWhenRunning(time_wasted_wrapper,1)
    d = time_wasted_wrapper(2)
    d.addCallback(print_result1)
    d.addCallback(all_jobs_done)
    print('all job have started!')
    reactor.run()