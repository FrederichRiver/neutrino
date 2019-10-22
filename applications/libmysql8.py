#!/usr/bin/python3
"""
This is a library dealing with mysql which is based on sqlalchemy.
Auther: Friederich River
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import CreateTable
from sqlalchemy.orm import sessionmaker
from libexception import AccountException
__version__ = '3.1.12'


class mysqlBase(object):
    def __init__(self, header):
        """
        :param header: Defines the mysql engine parameters.
        :param engine: is the object returned from create_engine.
        :param session: contains the cursor object.
        """
        mysql_url = (
            f"mysql+pymysql://{header.account}:"
            f"{header.password}"
            f"@{header.host}:{header.port}"
            f"/{header.database}")
        self.engine = create_engine(
            mysql_url,
            encoding='utf8',
            echo=False)
        db_session = sessionmaker(bind=self.engine)
        self.session = db_session()
        self.id_string = (
            f"mysql engine <{header.account}"
            f"@{header.host}>")

    def __str__(self):
        return self.id_string

    def insert(self, sql):
        self.engine.execute(sql)
        # self.engine.commit()
        return 1

    def query(self, sql):
        result = self.engine.execute(sql).fetchone()
        return result

    def drop_table(self, table_name):
        sql = f"DROP TABLE {table_name}"
        self.engine.execute(sql)

    def truncate_table(self, table_name):
        sql = f"TRUNCATE TABLE {table_name}"
        self.engine.execute(sql)


def _drop_all(base, engine):
    """
    This will drop all tables in database.
    It is a private method only for maintance.
    """
    base.metadata.drop_all(engine)


class mysqlHeader(object):
    """ Here defines the parameters passed into mysql engine.
    """

    def __init__(self, acc, pw, db,
                 host='localhost', port=3306, charset='utf8'):
        if not isinstance(acc, str):
            raise TypeError
        if not isinstance(pw, str):
            raise TypeError
        if not isinstance(db, str):
            raise TypeError
        self.account = acc
        self.password = pw
        self.database = db
        self.host = host
        self.port = port
        self.charset = 'utf8'


def create_table(table, engine):
    """
    : param table: It is form template defined in form module.
    : param engine: It is a sqlalchemy mysql engine.
    """
    table.metadata.create_all(engine)


def create_table_from_table(name, table_template, engine):
    # Base on a table, create another form which
    # is similar with the original table.
    # Only name was changed.
    # name : which is the target table name.
    # tableName : which is the original table name.
    # engine : a database engine base on MySQLBase.
    sql = "CREATE table {name} like {table_template}"
    engine.connect().execute(sql)
    engine.connect().close()


if __name__ == '__main__':
    h = mysqlHeader('root', '6414939', 'test')
    engine = mysqlBase(h)
    print(engine)
