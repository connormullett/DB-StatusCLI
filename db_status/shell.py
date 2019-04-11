# shell.py

import sys, os
from .connect import Connection


def print_help():
    pass


def quit():
    sys.exit(0)


def clear():
    os.system('clear')


# list of commands linked to functions
# for sql shell
_commands = {
    'h': print_help,
    'q': quit,
    'l': clear
}


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

    conn = conn.connect(conn.uri)

    cur = conn.cursor()

    while True:
        sys.stdout.write('> ')
        c = input()

        if c.startswith('/'):
            if c[1] in _commands:
                command = _commands.get(c[1], None)
                command()

        else:
            try:
                cur.execute(c)
                conn.commit()

                rows = cur.fetchall()
                for row in rows:
                    sys.stdout.write(f'{row}\n')
            except Exception as e:
                sys.stdout.write(f'{e}\n')
                conn.rollback()

