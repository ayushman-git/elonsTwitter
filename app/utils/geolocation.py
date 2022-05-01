from cmath import asin, cos, sin, sqrt
from math import radians

def is_within_range(lat1, lon1, lat2, lon2, distance):
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371 # Radius of earth in kilometers.
    return (c * r).real <= distance

def get_coordinates(location):
    lat, lon = location.strip('"').split(',')
    return float(lat), float(lon)