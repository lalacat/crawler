import time
"""
动态页面中有时间戳
该测试是来检验数字怎么转化为具体时间的 

"""
now = time.time()
print(now)
web_time = 152630110926
web_time_next = 152630004007
#print("差： %f"%(web_time-now))
#print("时间戳差值：%f"%(now-web_time_next))
print(web_time-web_time_next)
test = time.asctime(time.localtime(web_time/100))
#152630018309
#print(len(str(1526301408)))
#print(len(str(152630018309)))
print(test)