import os

file = open(os.path.join("","requset.txt"),'a+') #a+ 打开一个文件用于追加（读写），写入内容为str
fp = "https://"
file.write(fp+os.linesep)
print(os.linesep)