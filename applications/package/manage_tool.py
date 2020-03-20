#!/usr/bin/python3
from jupiter.database_manager import event_database_backup, event_mysql_backup
__version__ = '1.0.2'


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("maint init|backup")
        raise SystemExit(1)
    if sys.argv[1] == "init":
        event_initial_database()
    elif sys.argv[1] == "backup":
        event_mysql_backup()
    else:
        pass
