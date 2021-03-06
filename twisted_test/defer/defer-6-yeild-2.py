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
    r_s = etree.HTML(request.text)
    ul = r_s.xpath("body/div[@id='content']/div/div[@id='feed-wrap']/div"
                     "/div[@class='feed-main-con']/ul[@id='feed-main-list']")[0].xpath('./li')
    return ul


@inlineCallbacks
def time_wasted_wrapper(job_id):
    import time
    t1 = time.time()
    print('begin time-wasted job '+str(job_id))
    d = Deferred()

    reactor.callWhenRunning(d.callback,request("https://www.smzdm.com/"))
    result = yield d

    print('time-wasted job '+str(job_id)+' done!')
    t2 = time.time()
    print(t2-t1)

    d1 = Deferred()
    reactor.callWhenRunning(d1.callback,read_url(result))


    t3 = time.time()
    print(t3-t2)
    try:
        result = yield d1
    except Exception as e:
        print(e)
    print(len(result))
    print(result)
    returnValue(result)
    #reactor.stop()



def all_jobs_done(_):
   # print(str(result))
    print('all jobs are done!')
    reactor.stop()


def print_result1(result):

    for r in result:
        show = r.xpath('./h5/a/@href')

        #if show is not " ":
        print(show)
    return



if __name__ == '__main__':

    #reactor.callWhenRunning(time_wasted_wrapper,1)
    d = time_wasted_wrapper(2)
    d.addCallback(print_result1)
    d.addCallback(all_jobs_done)
    print('all job have started!')

    reactor.run()


