#!/usr/bin/python3
"""
Geschafen im Aug 31, 2017

Verfasst von Friederich Fluss

Lib of mysql contains methods to drive mysql db using python.
v3.0.6-alpha: change personal engine into commercial engine sqlalchemy.
v3.1.7-beta: Modified definition of mysqlBase, use strctural object to
            pass parameters.
"""

__version__ = '3.1.7-beta'
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import CreateTable
from sqlalchemy.orm import sessionmaker


class mysqlBase(object):
    def __init__(self, header):
        DB_STRING = (f"mysql+pymysql://{header.account}:"
                     f"{header.password}"
                     f"@{header.host}:{header.port}"
                     f"/{header.database}")
        self.engine = create_engine(DB_STRING,
                encoding='utf8',
                echo=False)
        DB_session = sessionmaker(bind=self.engine)
        self.session = DB_session()
        self.ident = (f"mysql engine <{header.account}"
                      f"@{header.host}>")

    def __repr__(self):
        return self.ident


def _drop_all(base, engine):
    # This will drop all tables in database.
    # It is a private method only for maintance.
    base.metadata.drop_all(engine)


class mysqlHeader(object):
    """ Here defines the parameters passed into mysql engine.
    """

    def __init__(self, acc, pw, db,
                 host='localhost', port=3306, charset='utf8'):
        self.account = acc
        self.password = pw
        self.database = db
        self.host = host
        self.port = port
        self.charset = 'utf8'


def create_table_from_table(name, tableName, engine):
    # Base on a table, create another form which
    # is similar with the original table.
    # Only name was changed.
    # name : which is the target table name.
    # tableName : which is the original table name.
    # engine : a database engine base on MySQLBase.
    Base = declarative_base()
    Base.metadata.reflect(engine)
    table = Base.metadata.tables[tableName]
    # Extract sql from the template table.
    c = str(CreateTable(table))
    c = c.replace("CREATE TABLE", "CREATE TABLE if not exists")
    sql = c.replace(tableName, name)
    # Execute the sql.
    engine.connect().execute(sql)
    engine.connect().close()
    Base.metadata.clear()


if __name__ == '__main__':
    h = mysqlHeader('root', '6414939', 'test')
    engine = mysqlBase(h)
    print(engine)
