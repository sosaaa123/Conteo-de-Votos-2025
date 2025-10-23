import psycopg2
class Conexion:
    def __init__(self, dsn):
        self.dsn = dsn
        self.connection = psycopg2.connect(self.dsn)
        self.cursor = self.connection.cursor()

    def commit(self):
        self.connection.commit()
    def close(self):
        self.cursor.close()
        self.connection.close()

    def rollback(self):
        self.connection.rollback()
