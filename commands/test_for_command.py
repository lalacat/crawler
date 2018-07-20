from importlib import import_module
from pkgutil import iter_modules
import inspect
import sys,os
from exceptions import UsageError
import optparse


def import_command(path):
    """
    导入指定目录下的包
        一般可以用于命令的导入
    对指定目录下存在多个文件的的时候回也能递归导入
    例如import_command("scrapy.commands")
    """
    commands = []
    #这条命令执行完只导入了目标文件夹中第一个*.py文件
    command = import_module(path)
    commands.append(command)

    #通过第一个.py文件获取该文件夹的绝对地址，通过文件夹的绝对地址可以通过iter_modules(path)方法获得该文件夹下所有的文件
    if hasattr(command,'__path__'):
        """
            三个参数:
            第一个通常不用
            subpath 获得的事文件或文件夹名（包名）
            ispkg 判断subpath是py文件还是文件夹（包），是包的话为true
            通过判断就可以实现指定目录下包括子目录的所有文件都能导入到执行环境中
        """
        for _,subpath,ispkg in iter_modules(command.__path__):
            #取得模块的绝对路径
            fullpath = path+"."+subpath

            #判断是模块包还是模块
            if ispkg:
                #是模块包的话重新调用本方法将模块包下的所以模块都导入
                commands += import_command(fullpath)
            else:
                #是模块的话就直接导入到结果中
                submod = import_module(fullpath)
                commands.append(submod)
    return commands


def get_command(commands):
    for c in commands:
        for obj in vars(c).values():
            """
            vars（）实现返回对象object的属性和属性值的字典对象
            要过滤出obj是类的信息，其中类的信息包括，模块导入其他模块的类的信息，模块中的父类，模块中所有定义的类
            因此，条件过滤分别是：
            1.判断obj的类型为class
            2.判断是否继承父类，因此命令包中__init__文件中定义的就是整个包中所需要的父类
            3.判断类是否为模块本身定义的类还是导入其他模块的类(感觉第二个条件包含此条件了有些多余)
            4.剔除父类
            """
            if inspect.isclass(obj) and \
                    issubclass(obj, BaseCommand) and \
                    obj.__module__ == c.__name__ and \
                    not obj == BaseCommand :
                yield obj


def get_command_dict(commands):
    dict_command = {}
    for c in get_command(commands):
        dict_command[c.__module__.split(".")[-1]]=c()

    return dict_command


def _print_commands(commands):
    """
    打印所有命令及所对应的简单用法
    """

    print("Usage:")
    print("  scrapy <command> [options] [args]\n")
    print("Available commands:")
    cmds = get_command_dict(commands)
    for cmdname, cmdclass in sorted(cmds.items()):
        print("  %-13s %s" % (cmdname, cmdclass.short_desc()))
    print()
    print('Use "scrapy <command> -h" to see more info about a command')

def _resovle_argv(argv):
    """
    将传入的参数进行解析，区分出命令和参数

    :param argv:
    :return command:
    """
    i = 1
    for arg in argv[1:]:
        if not arg.startswith("-"):
            del argv[i]
            return arg
        i += 1


def _run_print_help(parser, func, *a, **kw):
    """
    对传入的命令行参数进行处理，通过异常模块，防止程序意外中断
    :param parser: 命令行配置的实例
    :param func: 参数处理方法
    :param a: 未处理的参数
    :param kw: 已处理的参数
    :return: None
    """
    try:
        func(*a, **kw)
    except UsageError as e:
        if str(e):
            parser.error(str(e))
        if e.print_help:
            parser.print_help()
        sys.exit(2)


def run(argv):
    commands = import_command("commands")

    dict_command = get_command_dict(commands)
    parser = optparse.OptionParser(prog="Command", formatter=optparse.TitledHelpFormatter(), \
                                   conflict_handler='resolve')
    """
        for k, v in dict_command.items():
            print("%s : %s" %(k,v))
    """
    print(argv)
    cmdname = _resovle_argv(argv)

    print(argv)

    if cmdname in dict_command:
        print()
        cmd = dict_command[cmdname]
    else:
        _print_commands(commands)

    parser.description = cmd.long_desc()
    cmd.add_options(parser)
    opts,argv = parser.parse_args(argv[1:])

    print(opts)
    print(argv)
    cmd.process_option(argv, opts)

    try:
        cmd.process_option(argv,opts)
    except Exception as e:
        if str(e):
            parser.error(str(e))
            parser.print_help()




if __name__ == '__main__':
    print(os.getcwd())
    """
    项目的工作目录必须在整个项目的根目录下，才能将命令包导入
    先将目录转到上一级
    再将项目地址添加到系统环境中
    
    """
    os.chdir("..")
    path = os.getcwd()
    print(path)
    sys.path.append(path)
    from commands import BaseCommand
    run([" ","test_command3","-l"])

