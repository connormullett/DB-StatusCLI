
import psycopg2
import sqlite3
import os


class ConnectionFactory:

    @staticmethod
    def create(uri):
        return Connection(uri)


class Connection:

    def __init__(self, uri):
        self.uri = uri
        # self.connect = psycopg2.connect
        if os.path.exists(self.uri):
            self.uri = sqlite3.connect
        elif self.uri.startswith('postgres'):
            self.connect = psycopg2.connect

    def test(self):
        '''
        returns None if
        connection is made
        '''
        try:
            self.connect(self.uri)
            return None
        except Exception as e:
            return e

