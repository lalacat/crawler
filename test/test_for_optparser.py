import argparse
import os,sys
os.chdir("..")
path = os.getcwd()
sys.path.append(path)
from commands import test_command3
from test.framework.setting import BaseSettings
parser = argparse.ArgumentParser(prog="Command",
                                 formatter_class=argparse.RawTextHelpFormatter,
                                 conflict_handler='resolve',
                                 )

cmd = test_command3.Command()
parser.usage = "crawler %s %s" % (cmd.__name__, cmd.syntax())
parser.description = cmd.long_desc()
cmd.add_options(parser)


args = ['--logfile=.\\test.txt', '-s name=syw', '-s age=10', '--profile=test2.txt']

arg = parser.parse_args(args)
print(arg)

cmd.setting = BaseSettings()


cmd.setting.setdict(arg.set,"cmdline")
cmd.setting.setmoduel("setting.default_setting")
print(cmd.setting.attributes)
'''
if arg.logfile is not None:
    cmd.setting.set("logfile",arg.logfile,"cmdline")
    print(cmd.setting.attributes["logfile"].priority)



if arg.nolog:
    cmd.setting.set("nolog",True,"cmdline")
if arg.pidfile is not None:
    cmd.setting.set("pidfile",arg.pidfile,"cmdline")
if arg.profile is not None:
    cmd.setting.set("profile",arg.profile,"cmdline")
'''