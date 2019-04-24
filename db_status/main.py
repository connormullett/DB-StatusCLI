
from configparser import ConfigParser
from .shell import shell
from .connect import ConnectionFactory
from pyfiglet import print_figlet
import clint
import click
from pathlib import Path
import sys
import os

if sys.version_info[0] < 3:
    raise Exception('DBStatus requires Python3')


APP_NAME = 'db_status'
CFG = os.path.join(click.get_app_dir(APP_NAME), 'dbstatus.ini')


@click.group()
def main():
    pass
    # colors = "51;255;255:"
    # print_figlet("DB-Status", font='slant', colors=colors)


@main.command()
def get_uri():
    '''
    returns the URI in dbstatus.ini
    '''
    config = ConfigParser()
    config.read(CFG)
    if config['DatabaseURI']['uri']:
        # returning click.echo() will make sure you dont
        # have to call sys.exit()
        return click.echo(config['DatabaseURI']['uri'])
    return click.echo('No URI set')


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
                '\nNo DatabaseURI\n'
                'use: dbstat config DATABASEURI or \n'
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
    '''
    Creates the initial Config file
    '''
    if not os.path.exists(CFG):
        Path(CFG).touch()
        with open(CFG, 'w') as f:
            f.write('[DatabaseURI]\r\nuri =')
    else:
        click.echo('config file already exists')


@main.command()
@click.argument('uri')
def set_url(uri):
    '''
    Sets a URI for permanent storage,
    useful for maintaining an existing
    connection
    '''
    config = ConfigParser()
    if not os.path.exists(CFG):
        createconf()
    config.read(CFG)
    config['DatabaseURI']['uri'] = uri
    with open(CFG, 'w') as configfile:
        config.write(configfile)


@main.command()
def clear_uri():
    '''
    Clears URI from config file
    '''
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
    '''
    Open SQL shell on URI in config file
    or URI supplied with -u/--uri flag
    '''
    if uri is None:
        config = ConfigParser()
        config.read(CFG)
        if not config['DatabaseURI']['uri']:
            click.echo(
                '\nNo DatabaseURI\n'
                'use: dbstat config DATABASEURI or \n'
                'use: dbstat check --uri/-u DATABASEURI\n'
            )
            sys.exit(1)
        else:
            uri = config['DatabaseURI']['uri']

    conn = ConnectionFactory.create(uri)
    if not conn.test():
        shell(conn)


@main.command()
@click.argument('f')
@click.option('-u', '--uri', help='Database URI to execute script on')
def script(f, uri):
    '''
    executes SQL script 'f' on database,
    where F is the path to the script
    '''
    if not uri:
        config = ConfigParser()
        config.read(CFG)
        if not config['DatabaseURI']['uri']:
            click.echo(
                'No DatabaseURI\n'
                'use: dbstat config DATABASEURI or \n'
                'use: dbstat check --uri/-u DATABASEURI\n'
            )
        uri = config['DatabaseURI']['uri']
    with open(f, 'r') as script:
        query = script.read()

    conn = ConnectionFactory.create(uri)
    connection = conn.connect(conn.uri)
    if not conn.test():
        cur = connection.cursor()
        click.echo(cur.execute(query))
        connection.commit()


@main.command()
@click.argument('query')
@click.option('-u', '--uri', help='New URI')
def query(query, uri):
    if not uri:
        config = ConfigParser()
        config.read(CFG)
        if not config['DatabaseURI']['uri']:
            click.echo(
                'No DatabaseURI\n'
                'use: dbstat config DATABASEURI or \n'
                'use: dbstat check --uri/-u DATABASEURI\n'
            )
        uri = config['DatabaseURI']['uri']
        conn = ConnectionFactory.create(uri)
        connection = conn.connect(conn.uri)
        if not conn.test():
            cur = connection.cursor()
            cur.execute(query)
            try:
                click.echo(cur.fetchone())
                # fetchone does not always return a value
            except Exception as e:
                pass
            connection.commit()
