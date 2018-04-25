import pymongo

test_client = pymongo.MongoClient("localhost",27017)
test_db = test_client['test']
test_collection = test_db["smzdm_products"]

temp = test_collection.find({"title":"吉得利 精选干香菇 250g *5件 *2件40元（2件8折）"})
print(temp.count())
FLAG = True

while FLAG:
    all_item = test_collection.find({})
    current_time = all_item.count()
    print(current_time)
    for one_item in all_item:
        temp_title = one_item['title']
        temp_result = test_collection.find({"title":temp_title})
        print(temp_title)
        if temp_result.count() > 1:
            test_collection.delete_one(temp_result[1])
            flag = False
            break
        flag = True
    if flag:
        FLAG = False