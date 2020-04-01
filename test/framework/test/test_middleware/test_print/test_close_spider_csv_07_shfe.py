import pprint
from datetime import datetime
import pandas as pd


class Spider_Out_CSV(object):
    def __init__(self,settings):
        self.settings = settings
        self.name='shfe_海通.csv'
        self.path = 'C:\\华泰\\工作\\data\\shfe\\'+self.name
        self.frist_line = [
                            # 'date',
                            'cu',
                            'al',
                            'zn',
                            'pb',
                            'ni',
                            'sn',
                            'au',
                            'ag',
                            'rb',
                            'wr',
                            'ss',
                            'sc',
                            'hc',
                            'fu',
                            'bu',
                            'ru',
                            'nr',
                            'sp'
        ]
        self.result  = pd.DataFrame()
    @classmethod
    def from_crawler(cls,crawler):
        return cls(crawler)

    def get_volumn(self,data):
        num = 0
        for d in data:
            num += int(d.split(':')[-1])
        return num
    def defualtdictTodict(self,data):
        result = {}
        for key,value in data.items():
            result[key] = value
        return result

    def close_spider(self,spider):
        results = spider.total_result
        try:
            for index,values in results.items():
                for k in self.frist_line:
                    if values.get(k,None):
                        total_vulumn = self.get_volumn(values[k])
                        values[k] = total_vulumn
                    else:
                         values[k]= 0
                # 字符串转换日期格式
                result = pd.DataFrame(self.defualtdictTodict(values)  ,index=[index])
                if self.result.empty:
                    self.result = result
                else:
                    self.result = pd.concat([self.result,result])
                    # self.result.append(result)
            print(self.result)
            self.result.to_csv(self.path,encoding='utf-8')

        except Exception as e :
            print(e)
        return None