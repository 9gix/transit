#!/usr/bin/env python
import os, sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gohome.settings')
sys.path.insert(0,'lib')

if __name__ == '__main__':
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
elif __name__ == 'manage':
    from django.core.handlers.wsgi import WSGIHandler
    application = WSGIHandler()


