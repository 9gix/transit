from google.appengine.ext import db

class Bus(db.Model):
    no = db.StringProperty()

class BusRoute(db.Model):
    bus = db.ReferenceProperty(Bus, collection_name='routes')
    routes = db.ListProperty(db.GeoPt)
