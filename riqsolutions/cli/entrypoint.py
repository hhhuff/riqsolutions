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
    help="""
Specifiy subcommands when configuring:
    --api_token     API token (optional; will prompt if not provided
    --api_key       API private key (optional; will prompt if not provided
    --context       Configuration context (optional; use to activate a configuration for a given environment or project)
    --update        Set flag to update existing configfile if present
"""
)

configure.add_subparser(subparsers)
init.add_subparser(subparsers)


def main():
    args = parser.parse_args()
    if len(vars(args)) == 0:
        parser.print_help()
    else:
        args.func(args)
