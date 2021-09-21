import argparse
from . import configure
from . import init

parser = argparse.ArgumentParser(
    prog='riqsolutions',
    description='RiskIQ Solutions Developer Toolkit.'
)

subparsers = parser.add_subparsers(
    title='commands', 
    description='list of valid subcommands',
    help='Specifiy a subcommand to see valid options'
)

configure.add_subparser(subparsers)
init.add_subparser(subparsers)


def main():
    args = parser.parse_args()
    if len(vars(args)) == 0:
        parser.print_help()
    else:
        args.func(args)
