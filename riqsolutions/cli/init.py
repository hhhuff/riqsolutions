__version__ = '0.5.0'


def add_subparser(subparsers):
    parser = subparsers.add_parser('init')
    parser.add_argument('--gitignore')