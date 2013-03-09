import os
import sys
from os.path import abspath, dirname, join

CURRENT_DIR = dirname(__file__)
sys.path.insert(0, abspath(join(CURRENT_DIR, '..')))
sys.path.insert(0, abspath(join(CURRENT_DIR, '../..')))
sys.path.insert(0, abspath(join(CURRENT_DIR, '../transit')))
sys.path.insert(0, abspath(join(CURRENT_DIR, '../../transit')))
from urllib import urlretrieve

from django.core.management import setup_environ
from django.contrib.gis.gdal import DataSource
import settings
setup_environ(settings)

from directions.models import Bus
from time import sleep

def main():
    for filename in sorted(os.listdir('kml')):
        ds = DataSource('kml/%s' %filename)
        print ds[0][0].geom_type.name
        break


if __name__ == '__main__':
    main()
