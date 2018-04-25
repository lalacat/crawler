

class Test(object):

    def __init__(self):
        self.dicts = {}

    def set_value_dict(self, key, value):
        self.dicts[key] = value

    def set_dict(self, dicts):
        # 保留原有数据的基础上添加新的key:value值
        self.dicts.update(dicts)

    def get_value(self, key):
        return self[key]

    def __iter__(self):
        # 实现self本身的迭代，本质是对self.dicts属性迭代
        # if判断，for循环都是对self.__iter__进行调用
        return iter(self.dicts)

    def __getitem__(self, key, default=None):
        # 配合__iter__可以实现key直接判断是否在self中存在，直接使用self[key]取值
        if key not in self:
            return None
        return self.dicts[key]

    def get(self,key):
        if key in self:
            return self[key]
    # if判断中in的是实现就是调用这个方法
    def __contains__(self, item):
        return item in self.dicts
if __name__ == "__main__":
    test = Test()
    test.set_value_dict("a", 1)
    test.set_value_dict("b", 2)
    test.set_value_dict("c", 3)
    test.set_dict({"q": 4, "w": 5, 'e': 6})

    # 对实例本身进行迭代，实质是对test.dicts进行迭代
    for i in test:
        print(i)
    '''
    
    # 通过__getitem__实现
    print(test["a"])
    print(test["b"])
    print(test["c"])
    print(test["d"])
    '''
    print(test.get("w"))