from celery import task
from directions.views import *

@task()
def fetch_smrt_route():
    fetcher = MytransportSMRTBusRouteDataset()
    fetcher.fetch()

@task()
def fetch_sbs_route():
    fetcher = MytransportSBSTBusRouteDataset()
    fetcher.fetch()
