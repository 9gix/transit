from google.appengine.ext import db


class Bus(db.Model):
    """Key: <bus_no>"""
    no = db.StringProperty()
    operator = db.StringProperty()


class Stop(db.Model):
    """Key: <code>"""
    code = db.StringProperty()
    lat = db.FloatProperty()
    lng = db.FloatProperty()


class BusStop(db.Model):
    """Key: <stop__code>-<bus__no>"""
    bus = db.ReferenceProperty(Bus, collection_name='stops')
    stop = db.ReferenceProperty(Stop, collection_name='buses')
