
import sys, os
from pathlib import Path

import click
import clint

from .connect import ConnectionFactory
from .shell import shell
from configparser import ConfigParser


APP_NAME = 'db_status'
CFG = os.path.join(click.get_app_dir(APP_NAME), 'dbstatus.ini')


@click.group()
def main():
    pass


@main.command()
@click.option('--uri', '-u', help='Database URI')
def check(uri):
    '''
    Checks if uri is supplied as option
    if not, opens config file and checks
    if the URI is set.
    exits if URI is not supplied and --uri/-u
    was not supplied
    returns a status (success/failed) after
    trying to connect
    '''
    if uri is None:
        config = ConfigParser()
        config.read(CFG)
        if not config['DatabaseURI']['uri']:
            click.echo(
                '\nNo DatabaseURI\n' \
                'use: dbstat config DATABASEURI or \n' \
                'use: dbstat check --uri/-u DATABASEURI\n'
            )
            sys.exit(1)
        else:
            uri = config['DatabaseURI']['uri']

    # perform connection
    con = ConnectionFactory.create(uri)
    rv = con.test()

    if not rv:
        click.secho('health check :: success', fg='cyan', bold=True)
    else:
        click.secho('health check :: failed', fg='red', bold=True)
        click.echo(rv)


@main.command()
def createconf():
    if not os.path.exists(CFG):
        Path(CFG).touch()
        with open(CFG, 'w') as f:
            f.write('[DatabaseURI]\r\nuri =')
    else:
        click.echo('config file already exists')


@main.command()
@click.argument('uri')
def set_url(uri):
    config = ConfigParser()
    if not os.path.exists(CFG):
        createconf()
    config.read(CFG)
    config['DatabaseURI']['uri'] = uri
    with open(CFG, 'w') as configfile:
        config.write(configfile)


@main.command()
def clear_url():
    config = ConfigParser()
    if not os.path.exists(CFG):
        click.echo('config file does not exist')
        sys.exit(0)
    config.read(CFG)
    config['DatabaseURI']['uri'] = ''
    with open(CFG, 'w') as f:
        config.write(f)


@main.command()
@click.option('-u', '--uri', help='Database URI to execute commands on')
def sql_shell(uri):
    if uri is None:
        config = ConfigParser()
        config.read(CFG)
        if not config['DatabaseURI']['uri']:
            click.echo(
                '\nNo DatabaseURI\n' \
                'use: dbstat config DATABASEURI or \n' \
                'use: dbstat check --uri/-u DATABASEURI\n'
            )
            sys.exit(1)
        else:
            uri = config['DatabaseURI']['uri']

    conn = ConnectionFactory.create(uri)
    if not conn.test():
        shell(conn)

