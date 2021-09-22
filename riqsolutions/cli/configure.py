from os.path import expanduser, join, exists
import configparser
from getpass import getpass, getuser


CONFIGFILE_DEFAULT_NAME = '.riqconfig'


def add_subparser(subparsers):
    parser = subparsers.add_parser('configure')
    parser.add_argument('--api_token', 
        default=None,
        help='API token (optional; will prompt if not provided'
    )
    parser.add_argument('--api_key',
        default=None,
        help='API private key (optional; will prompt if not provided'
    )
    parser.add_argument('--proxy',
        default=None,
        help='Proxy to be used for http requests'
    )
    parser.add_argument('--context', 
        default='DEFAULT',
        help='Configuration context (optional; use to activate a configuration for a given environment or project)'
    )
    parser.add_argument('--configfile',
        help='Path to config file; defaults to {} in users home directory'.format(CONFIGFILE_DEFAULT_NAME)
    )
    parser.add_argument('--update',
        default=False,
        action='store_true',
        help='Set flag to update existing configfile if present'
    )
    parser.set_defaults(func=main)

def main(args):
    if not args.configfile:
        filepath = join(expanduser('~'), CONFIGFILE_DEFAULT_NAME)
    else:
        filepath = args.configfile
    if exists(filepath) and not args.update:
        print('ERROR: found existing config file at {} (pass --update to change file)'.format(filepath))
        return 1
    print('Writing config for context "{}" to {}'.format(args.context, filepath))
    if not args.api_token:
        api_token = getpass(' API Token: ')
    else:
        api_token = args.api_token
    if not args.api_key:
        api_key = getpass(' API Key: ')
    else:
        api_key = args.api_key
    if api_token == '' or api_key == '':
        print('ERROR: api_token and api_key are both required to complete configuration')
        return 1
    
    if not args.proxy:
        proxy = ''
    else:
        proxy = args.proxy
    
    if not args.context:
        context = 'DEFAULT'
    else:
        context = args.context

    config = configparser.ConfigParser()
    if exists(filepath) and args.update:
        config.read(filepath)
    config[args.context] = {
        'api_token': api_token,
        'api_key': api_key,
        'proxy': proxy,
        'context': context
    }
    try:
        with open(filepath, 'w') as configfile:
            config.write(configfile)
    except OSError as err:
        print('ERROR: cannot write config file - {}'.format(err))
        return 1


    
