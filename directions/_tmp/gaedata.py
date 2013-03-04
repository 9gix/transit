"""This is an import script from google appengine data to django"""
import csv
import json
from operator import itemgetter

def get_stops_data():
    stops_data = {}
    with open('stop.csv', 'rb') as csvfile:
        stopreader = csv.reader(csvfile)
        stopreader.next()
        for i, row in enumerate(stopreader):
            lat = row[0]
            lon = row[1]
            code = row[2]
            stops_data[code] = {
                'code': code,
                'lat': lat,
                'lon': lon,
            }
    return stops_data

def get_buses_data():
    buses_data = {}
    with open('bus.csv', 'rb') as csvfile:
        busreader = csv.reader(csvfile)
        busreader.next()
        for i, row in enumerate(busreader):
            bus_no = row[2]
            direction = row[0]
            buses_data[bus_no] = {
                'no': bus_no,
                'direction': direction,
                'stops': [],
            }

    with open('bus-stop.csv', 'rb') as csvfile:
        busstopreader = csv.reader(csvfile)
        busstopreader.next()
        for i, row in enumerate(busstopreader):
            bus_no = row[0]
            stop_code = row[1]
            buses_data[bus_no]['stops'].append(stop_code)

    return buses_data

def stop_code_mapper(data):
    return stops_code_map[data]

def main():
    initial_data = []

    stops_data = get_stops_data()
    stop_mappers = {}
    for i, stop_data in enumerate(stops_data.itervalues()):
        stop = {
            'model': 'directions.stop',
            'pk': i+1,
            'fields': stop_data,
        }
        initial_data.append(stop)
        stop_mappers[stop_data['code']] = i + 1

    buses_data = get_buses_data()
    for bus_data in buses_data.itervalues():
        x = map(lambda stop: stop_mappers[stop], bus_data['stops'])
        bus_data['stops'] = x

    for i, bus_data in enumerate(buses_data.itervalues()):
        bus = {
            'model': 'directions.bus',
            'pk': i+1,
            'fields': bus_data,
        }
        initial_data.append(bus)


    with open('initial_data.json', 'w') as initial_data_file:
        json.dump(initial_data, initial_data_file, indent=4)

if __name__ == '__main__':
    main()
