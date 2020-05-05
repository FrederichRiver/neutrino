#!/usr/bin/python3
from jupiter.database_manager import event_mysql_backup
__version__ = '1.0.3'


def neutrino_install():
    dest = '/opt/neutrino/'
    obj = '/root/ftp/package/'
    files = [
        'neutrino.py', 'message.py', 'manage_tool.py',
        'config/conf.json', 'config/Neutrino', 'config/task.json',
        'config/cookie.json']
    for fi in files:
        obj_fi = obj + fi
        dest_fi = dest + fi
        if os.path.isfile(obj_fi):
            # print(obj_fi)
            cmd = "cp -u -v %s %s" % (obj_fi, dest_fi)
            os.system(cmd)
        elif os.path.isdir(fi):
            solve_dir(obj_fi+'/')
        else:
            pass


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("maint init|backup")
        raise SystemExit(1)
    if sys.argv[1] == "init":
        from jupiter.database_manager import event_initial_database
        event_initial_database()
    elif sys.argv[1] == "backup":
        event_mysql_backup()
    elif sys.argv[1] == "install":
        neutrino_install()
    else:
        pass
