from commands import BaseCommand
from conf import arglist_to_dict


class Command(BaseCommand):
    __name__ = "test_command3"

    def syntax(self):
        return "[options] <name> <domain>"

    def run(self, args):
        for i in args[1:]:
            print("test3：" + i)


    def short_desc(self):
        return "command3"

    def add_options(self, parser):
        BaseCommand.add_options(self, parser)
        parser.add_argument("-l", "--list", dest="list", action="store_true",
                          help="only list contracts, without checking them")
        parser.add_argument("-v", "--verbose", dest="verbose", default=False, action='store_true',
                          help="print contract tests for all spiders")
        parser.add_argument('-d', '--dicts', action="append", default=[], metavar='NAME=VALUE',
                          help="store dicts")

    def process_option(self, args, opts):
        BaseCommand.procss_option(args, opts)
        try:
            self.setting.setdict(arglist_to_dict(opts.dicts), priority='command')
        except ValueError:
            raise print("dicts is error")
        if opts.list:
            self.setting.setdict("list", True, priority="cmdline")
