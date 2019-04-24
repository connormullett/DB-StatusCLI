# shell.py

import sys
import os
import traceback
from .connect import Connection


def quit(*args, **kwargs):
    '''exit the terminal'''
    sys.exit(0)


def clear(*args, **kwargs):
    '''clear the terminal screen'''
    os.system('clear')


def get_uri(*args, **kwargs):
    '''returns the URI of the database
    currently connected to'''
    sys.stdout.write(f'{kwargs.get("uri")}\n')


def change_uri(*args, **kwargs):
    '''change the URI to a different database, will not write to config'''
    pass


def print_help(*args, **kwargs):
    '''print commands with descriptions to terminal'''
    sys.stdout.write(
        f' /h :: {print_help.__doc__}\n'
        f' /q :: {quit.__doc__}\n'
        f' /l :: {clear.__doc__}\n'
        f' /u :: {get_uri.__doc__}\n'
        f' /r :: {change_uri.__doc__}\n'
    )


# list of commands linked to functions
# for sql shell
_commands = {
    'h': print_help,
    'q': quit,
    'l': clear,
    'u': get_uri,
    'r': change_uri
}


def pp(rows):
    for row in rows:
        for i in row:
            sys.stdout.write(f'{i}  ')
        sys.stdout.write('\n')
    sys.stdout.write('\n')


def shell(conn: Connection):
    '''
    Creates a Read Evaluate Print
    Loop for the conn object

    commands that start with /
    are built in commands
    viewable with /h

    anything is treated as a SQL
    script, errors will trigger
    a rollback transaction
    to undo damage to DB
    '''
    # uri for /u
    uri = conn.uri
    # simplify connection object
    connection = conn.connect(conn.uri)

    cur = connection.cursor()

    while True:
        sys.stdout.write('> ')
        c = input()

        if c.startswith('/'):
            if c[1] in _commands:
                command = _commands.get(c[1], None)
                command(uri=conn.uri)
            if c[1].lower() == 'r':
                continue  # guard for this block
                # below is changing the URI in shell
                new_uri = c[3:]
                conn.uri = new_uri
                if conn.test():
                    conn.uri = uri
                else:
                    connection = conn.connect(conn.uri)

        else:
            try:
                cur.execute(c)
                connection.commit()

                if cur.description:
                    colnames = [desc[0] for desc in cur.description]
                    for column in colnames:
                        sys.stdout.write(f'{column} ')
                    sys.stdout.write('\n')

                    rows = cur.fetchall()

                    pp(rows)
            except Exception as e:
                traceback.print_tb(e.__traceback__)
                sys.stdout.write(f'{e}\n')
                connection.rollback()
