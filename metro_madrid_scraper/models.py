
class Line(object):

    def __init__(self, name, metro_type, stations=[]):
        self.name = name
        self.stations = stations
        self.metro_type = metro_type

    def to_json(self):
        return {'name': self.name,
                'stations': self.stations}

    def __str__(self):
        return str(self.to_json())

    def __repr__(self):
        return str(self)


class Station(object):

    def __init__(self, name, station_rate_zone=None, services=[], correspondences=[], conections=[], coord=None):
        self.name = name
        self.station_rate_zone = station_rate_zone
        self.services = services
        self.coord = coord
        self.correspondences = correspondences
        self.conections = conections

    def to_json(self):
        return {'station_name': self.name,
                'station_rate_zone': self.station_rate_zone,
                'services': self.services,
                'coords': self.coord}

    def get_correspondences(self):
        if len(self.correspondences) == 0:
            return ''
        else:
            return ', '.join(str(e) for e in self.correspondences)

    def get_conections(self):
        if len(self.conections) == 0:
            return ''
        else:
            return ', '.join(str(e) for e in self.conections)

    def __str__(self):
        return str(self.to_json())

    def __repr__(self):
        return str(self)


class Coord(object):

    def __init__(self, lat, long):
        self.lat = lat
        self.long = long

    def to_json(self):
        return {'lat': self.lat,
                'long': self.long}

    def __str__(self):
        return str(self.to_json())

    def __repr__(self):
        return str(self)
