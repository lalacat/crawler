
class Spider_Out_print(object):
    def __init__(self,settings):
        self.settings = settings

    @classmethod
    def from_crawler(cls,crawler):
        return cls(crawler)

    def close_spider(self,spider):
        try:
            print("%s 理论获取小区数为%d个，实际获得小区数为%d个"
                  %(spider.name,int(spider.result["total_xiaoqu_number"][0]),spider.result_len))

            '''
            max_page = spider.total_page_number + 1
            for i in range(1, max_page):
                print("第 %d 页的房屋信息"%i)
                xiaoqu_num = len(spider.result[str(i)])
                print("本页一共 %d 个小区" % xiaoqu_num)
               

                if xiaoqu_num < 30 and i < max_page-1:
                    for community_list in spider.result[str(i)]:
                        print(community_list['community_name'])

            '''
            print(" ")

        except Exception as e :
            print("Spider_Out_print",e)

        return None
