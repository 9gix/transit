from google.appengine.ext import db


class Bus(db.Model):
    """Key: <bus_no>"""
    no = db.StringProperty()
    operator = db.StringProperty()


class BusRoute(db.Model):
    """Key: <bus_no>-<direction>"""
    bus = db.ReferenceProperty(Bus, collection_name='routes')
    direction = db.IntegerProperty()
    routes = db.ListProperty(db.GeoPt)


class BusStop(db.Model):
    """Key: <code>"""
    code = db.StringProperty()
    coordinate = db.GeoPtProperty()


class BusRouteStop(db.Model):
    """Key: <bus_no>-<stop_sequence>"""
    bus_route = db.ReferenceProperty(BusRoute, collection_name='bus_route_stops')
    bus_stop = db.ReferenceProperty(BusStop, collection_name='bus_route_stops')
    stop_sequence = db.IntegerProperty()
    is_loop = db.BooleanProperty()
