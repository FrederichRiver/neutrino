#!/usr/bin/python3

from jupiter.database_manager import databaseBackup


def event_initial_database(header):
    from dev_global.env import GLOBAL_HEADER
    from venus.form import formTemplate, formFinanceTemplate, formInfomation
    mysql = mysqlBase(GLOBAL_HEADER)
    create_table(formTemplate, mysql.engine)
    create_table(formFinanceTemplate, mysql.engine)
    create_table(formInfomation, mysql.engine)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("maint init|backup")
        raise SystemExit(1)
    if sys.argv[1] == "init":
        try:
            # header = mysqlHeader('stock', 'stock2020', 'stock')
            header = mysqlHeader('root', '6414939', 'test')
            event_initial_database(header)
        except Exception as e:
            print(e)
    elif sys.argv[1] == "backup":
        try:
            event = databaseBackup()
            event.get_database_list()
            event.backup()
        except Exception as e:
            print(e)
    else:
        pass
