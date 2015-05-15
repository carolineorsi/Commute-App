import requests
import urllib
import xml.etree.ElementTree as ET
from operator import itemgetter
# import xmltodict

TOKEN = "10f777df-2175-4dfb-9b7a-69aaa066e91a"
STOPCODE_NB_22ND_ST = '70021'
# STOPCODE_NB_22ND_ST = '15203'


class Route():

    def __init__(self, name, station, to_time, travel_time, from_time, stopcode):
        self.name = name
        self.station = station
        self.to_time = to_time
        self.travel_time = travel_time
        self.from_time = from_time
        self.stopcode = stopcode


    def get_arrivals(self):
        params = urllib.urlencode({'token': TOKEN, 'stopcode': self.stopcode})
        url = "http://services.my511.org/Transit2.0/GetNextDeparturesByStopCode.aspx?%s" % params

        arrivals_xml = urllib.urlopen(url).read()
        root = ET.fromstring(arrivals_xml)

        arrivals = []
        for node in root.iter('DepartureTime'):
            arrivals.append(int(node.text))

        self.arrivals = arrivals


    def calculate_arrival(self, time_to_station):
        self.get_arrivals()

        selected_arrival = None
        for arrival in self.arrivals:
            if time_to_station + self.to_time < arrival:
                selected_arrival = arrival
                break

        if not selected_arrival:
            selected_arrival = 100

        home_time_in_mins = selected_arrival + self.travel_time + self.from_time
        return self.name, home_time_in_mins, selected_arrival
        # home_time_in_datetime = datetime.datetime.now() + home_time_in_mins #(or maybe do this elsewhere?)

        # return {
        #     'home_time': home_time_in_datetime,
        #     'arrival_time': selected_arrival
        #     }


def initiate_routes():
    routes = []
    routes.append(Route('22', '22nd', 10, 16, 10, '13342'))
    routes.append(Route('48', '22nd', 4, 25, 14, '13436'))
    routes.append(Route('N', '4th', 6, 20, 15, '15240'))
    routes.append(Route('T', '4th', 6, 20, 10, '17166'))

    return routes


def get_caltrain_arrival(stop):
    params = urllib.urlencode({
        'token': TOKEN,
        'stopcode': stop})
    url = "http://services.my511.org/Transit2.0/GetNextDeparturesByStopCode.aspx?%s" % params

    caltrain_xml = urllib.urlopen(url).read()
    root = ET.fromstring(caltrain_xml)

    departures = []
    for node in root.iter('DepartureTime'):
        departures.append(int(node.text))

    departures.sort()

    if not departures:
        departures.append(0)

    return departures[0]


def get_times():
    routes = initiate_routes()

    station_22nd = get_caltrain_arrival(STOPCODE_NB_22ND_ST)
    station_4th = station_22nd + 7 # Add seven minutes to arrival time, since can't look up 4th st departure times

    home_times = []

    for route in routes:
        if route.station == '22nd':
            home_times.append(route.calculate_arrival(station_22nd))
        else:
            home_times.append(route.calculate_arrival(station_4th))

    home_times = sorted(home_times, key=itemgetter(1))

    return home_times, station_22nd


if __name__ == '__main__':
    get_times()