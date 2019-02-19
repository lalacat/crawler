import argparse
class BaseCommand(object):


    """
    简要对各个命令的用法进行说明的方法
    """
    def __init__(self,setting = None):
        self.setting = setting

    def short_desc(self):
        pass

    def long_desc(self):
        return "Test for Long desc"

    #给出程序版本的回调函数
    def _print_vision(self,option,opt_str,value,parser):
        print("This vision is 0.0.0")

    def add_options(self,parser):
        """
        给出基本的参数表
        """
        group = parser.add_argument_group( "Global Options")
        group.add_argument("--logfile", metavar="FILE",
                         help="log file. if omitted stderr will be used")
        group.add_argument("--nolog", action="store_true",
                         help="disable logging completely")
        group.add_argument("--profile", metavar="FILE", default=None,
                         help="write python cProfile stats to FILE")
        group.add_argument("--pidfile", metavar="FILE",
                         help="write process ID to FILE")
        group.add_argument("--version", action="version", version="version 0.0",help="command vision")
        #  处理这类参数的时候，需要使用一个方法，将-s之后的键值对处理为dict格式'-s key=value'
        group.add_argument("-s", "--set", action="append", default=[], metavar="NAME=VALUE",
            help="set/override setting (may be repeated)")
        print("global options")

    def procss_option(self, arg):

        if arg.logfile is not None:
            self.setting.set("logfile", arg.logfile, "cmdline")
            print(self.setting.attributes["logfile"].priority)

        if arg.nolog:
            self.setting.set("nolog", True, "cmdline")
        if arg.pidfile is not None:
            self.setting.set("pidfile", arg.pidfile, "cmdline")
        if arg.profile is not None:
            self.setting.set("profile", arg.profile, "cmdline")