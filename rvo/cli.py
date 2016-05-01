#!/usr/bin/env python2.7

import sys
import os
import click
import datetime
import rvo.utils as utils
from dateutil.parser import parse
from rvo import __version__

command_folder = os.path.join(os.path.dirname(__file__), 'commands')
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

# validators
def validate_date(ctx, param, value):
    try:
        value = parse(value)
        return value
    except AttributeError:
        return value
    except ValueError:
        raise click.BadParameter('Date format \"%s\" not valid' % value)

# rvo command class
class rvoCommands(click.MultiCommand):

    def list_commands(self, ctx):
        rv = []
        for filename in os.listdir(command_folder):
            #if filename.endswith('.py'):
            if filename.endswith('.py') and not filename.startswith('__init__'):
                rv.append(filename[:-3])
        rv.sort()
        return rv

    def get_command(self, ctx, name):
        ns = {}
        fn = os.path.join(command_folder, name + '.py')
        try:
            with open(fn) as f:
                code = compile(f.read(), fn, 'exec')
                eval(code, ns, ns)
            return ns[name]
        except IOError:
            click.help_option()

# base help message
@click.command(cls=rvoCommands, context_settings=CONTEXT_SETTINGS,
help="""
Manage text data on commandline

\b
888,8, Y8b Y888P  e88 88e
888 "   Y8b Y8P  d888 888b
888      Y8b "   Y888 888P
888       Y8P     "88 88"

For the sake of your own data being managed
by you and only you!

""")
@click.version_option(version=__version__, prog_name="rvo")
def cli():
    pass

if __name__ == '__main__':
    cli()

