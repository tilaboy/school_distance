import re

def get_geocode_from_direction(response):
    result_raw = response['results']
    lng = result_raw[0]['location']['lng']
    lat = result_raw[0]['location']['lat']
    #print ("lat:{}, lng:{}".format(lat, lng))
    return ( lat, lng )

def get_distance_duration_from_direction(response):
    route = response['result']['routes']
    distance = route[0]['distance']
    duration = route[0]['duration']
    #print ("distance:{}, duration:{}".format(distance, duration))
    return ( distance, duration )
