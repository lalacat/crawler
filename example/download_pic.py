import os
import pymongo

pic_client = pymongo.MongoClient("localhost",27017)
pic_db = pic_client['test']
pic_connect = pic_db["smzdm_products"]

pic = pic_connect.find_one()
print(pic['picture'])
url = pic['picture']
os.execl('C:\Program Files (x86)\Thunder Network\Thunder\Program\Thunder.exe', '-StartType:DesktopIcon \"%s\"'%url)
