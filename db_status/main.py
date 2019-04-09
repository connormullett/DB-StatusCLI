
import sys, os
from pathlib import Path

import click
import clint
import psycopg2

from configparser import ConfigParser


APP_NAME = 'db_status'
CFG = os.path.join(click.get_app_dir(APP_NAME), 'dbstatus.ini')


@click.group()
def main():
    pass


@main.command()
@click.option('--uri', '-u', help='Database URI')
def check(uri):
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
    click.secho('health check :: success', fg='cyan', bold=True)


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

