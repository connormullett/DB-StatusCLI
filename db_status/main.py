
import sys

import click
import clint
import psycopg2

from configparser import ConfigParser


@click.group()
def main():
    pass


@main.command()
@click.option('--uri', '-u', help='Database URI')
def check(uri):
    if uri is None:
        config = ConfigParser()
        config.read('config.ini')
        if not config['DatabaseURI']['uri']:
            click.echo(
                '\nNo DatabaseURI\n' \
                'use: dbstat config DATABASEURI or \n' \
                'use: dbstat check--uri DATABASEURI\n'
            )
            sys.exit(1)
        else:
            uri = config['DatabaseURI']['uri']
    click.echo('health check :: success')

@main.command()
@click.argument('uri')
def config(uri):
    click.echo('config writer :: success')

