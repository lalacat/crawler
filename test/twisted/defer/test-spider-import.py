from importlib import import_module
from pkgutil import iter_modules
import sys,os

def import_spider(path):

    spiders = []

    spider = import_module(path)
    spiders.append(spider)

    if hasattr(spider,"__path__"):
        print(spider.__path__)

        for _, subpath, ispkg in iter_modules(spider.__path__):
            # 取得模块的绝对路径
            fullpath = path + "." + subpath

            # 判断是模块包还是模块
            if ispkg:
                # 是模块包的话重新调用本方法将模块包下的所以模块都导入
                spiders += import_spider(fullpath)
            else:
                # 是模块的话就直接导入到结果中
                submod = import_module(fullpath)
                spiders.append(submod)
    else:
        print("路径不对，脚本放在根目录下")
    return spiders


def find_spider_moudle(projectName):

    #获取文件当前路径
    curent_path = os.getcwd()
    # 找到项目的根目录的绝对地址，并将工作目录切换到根目录下
    root_direction = curent_path.split(projectName)[0]+projectName
    os.chdir(root_direction)
    #获取根目录下所有的子文件夹
    dirlist = os.listdir(path)

    '''
    #先判断是否有爬虫包的存在
    #存在的话就直接导入包
    #不存在的话就创建一个爬虫包
    if not dirlist.__contains__("spider"):
        os.mkdir("spider")
            
    '''



'''
find_spider = False


while not find_spider:

    find_spider = True
    try:
        s = import_spider("spider")
    except ModuleNotFoundError as e :
        print("目录路径不对，将文件放在爬虫文件同级目录下")
        find_spider = False
        os.chdir("..")
        path = os.getcwd()
        sys.path.append(path)
print(type(s))
'''

path = os.getcwd()
print(path)
root_direction = path.split("crawler")[0] + "crawler"
os.chdir(root_direction)
# 获取根目录下所有的子文件夹

list = os.listdir(root_direction)
if not list.__contains__("spider"):
    os.mkdir("spider")
print(os.getcwd())

for l in list:

    if l == 'test':
        temp = os.path.join(root_direction, l)
        os.chdir(temp)

print(temp)

flag = os.path.exists("spider")
if flag:
    sys.path.append(temp)
    s = import_spider("spider")

print(s)