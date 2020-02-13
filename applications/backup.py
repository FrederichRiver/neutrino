#!/usr/bin/python3
from jupiter import database_manager


def unit_test_database_manager():
    bk = database_manager.databaseBackup()
    bk.get_database_list()
    # bk.backup()
    # bk.compress()
    bk.remove_old_backup()


if __name__ == "__main__":
    bk = database_manager.databaseBackup()
    bk.get_database_list()
    bk.backup()
    bk.compress()
    bk.remove_old_backup()
