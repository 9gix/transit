import sys
from os.path import abspath, dirname, join

CURRENT_DIR = dirname(__file__)
sys.path.insert(0, abspath(join(CURRENT_DIR, '..')))
sys.path.insert(0, abspath(join(CURRENT_DIR, '../..')))
sys.path.insert(0, abspath(join(CURRENT_DIR, '../transit')))
sys.path.insert(0, abspath(join(CURRENT_DIR, '../../transit')))
from urllib import urlretrieve

from django.core.management import setup_environ
import settings
setup_environ(settings)

from directions.models import Bus
from time import sleep

BUS_ROUTE_API_URL = "http://www.publictransport.sg/kml/busroutes/"
def fetch_all_kml():
    buses = Bus.objects.all().order_by('id')
    for bus in buses:
        for direction in range(1, bus.direction + 1):
            filename = "%s-%s.kml" % (bus.no, direction)
            url = BUS_ROUTE_API_URL + filename
            print urlretrieve(url, filename)
        print bus.id
        sleep(60)

if __name__ == '__main__':
    fetch_all_kml()
