from datetime import datetime, timedelta

import requests
# url ='http://www.cffex.com.cn/ccpm/sj/ccpm/201912/31/IF_1.csv'
from chinese_calendar import is_holiday



# 字符串转换日期格式
start = datetime.strptime('20190101','%Y%m%d').date()
end_day = datetime.strptime('20191231','%Y%m%d').date()
result = {}
number = 1

def get_tradingday(start_day,end_day):
    start_week = start_day.isoweekday()
    days = []
    end = False
    global number
    for day in range(6-start_week):
        t = start_day+timedelta(days=day)
        if t == end_day:
            end = True
            day =  6 - start_week - 1
        if t.isoweekday() < 6:
            if not is_holiday(t):
                days.append(t)
        if day == 6 - start_week - 1:
            if days:
                result[str(number)] = days
                number = number + 1
            if end:
                break
            next_weekday = t + timedelta(days=3)
            get_tradingday(next_weekday,end_day)


get_tradingday(start,end_day)
file_base_path = 'C:\\华泰\\工作\\data\\cffex\\{0}\\{1}.csv'

start_urls = [
    ]
sorts = ['IF_1','IC_1','IH_1','TS_1','TF_1','T_1']
for s in sorts:
    for i in range(1,53):
        week = result[str(i)]
        for day in week:
            day_temp = day.strftime('%Y%m%d')
            day = day.strftime('%Y%m/%d')
            url = 'http://www.cffex.com.cn/sj/ccpm/{0}/{1}.csv'.format(day,s)
            print('%s:%s 正在下载'%(s,day))
            resp = requests.get(url)
            file_name= file_base_path.format(s,day_temp)
            with open(file_name, 'wb') as output:
                output.write(resp.content)
                print('%s：已下载' %file_name)





# resp = requests.get(url)
# output = open(file_base_path, 'wb')
# output.write(resp.content)
# output.close()