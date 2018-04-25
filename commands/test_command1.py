from commands import BaseCommand
class Command(BaseCommand):
    def run(self,args):
        for i in args[1:]:
            print("test1："+i)
    def short_desc(self):
       return "command1"