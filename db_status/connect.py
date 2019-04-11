
import psycopg2


class ConnectionFactory:

    @staticmethod
    def create(uri):
        return Connection(uri)


class Connection:

    def __init__(self, uri):
        self.uri = uri
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

