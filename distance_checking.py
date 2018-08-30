import csv
import pandas as pd
import numpy as np
import logging
import sys

from baidumap import baidumap_client
from baidumap import json_parse

def setup_logging(verbose=True):
    logging.basicConfig(filename='distance_checking.log', level=logging.DEBUG, filemode='w')
    root = logging.getLogger()

    #Attach logging output to stdout
    if verbose:
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        root.addHandler(ch)

#http://api.map.baidu.com/place/v2/search?query=顶澳仔6号&region=厦门&output=json&ak=RNYTWuvcC1M8PWYPqerbbQ0V8bTX6gRY
#http://api.map.baidu.com/direction/v2/riding?origin=40.01116,116.339303&destination=39.936404,116.452562&ak=RNYTWuvcC1M8PWYPqerbbQ0V8bTX6gRY
def get_coord(client, place, region):
    action='place'
    sub_action='search'
    location_json = client.get(action=action, sub_action=sub_action, params={'query': place, 'region': region})
    (lat, lng) = json_parse.get_geocode_from_direction(location_json)
    coord = "{},{}".format(lat, lng)
    return coord

def get_distance(client, origin_coord, target_coord):
    distance_json = client.get(action='direction', sub_action='transit', params={'origin':origin_coord,'destination':target_coord})
    (distance, duration) = json_parse.get_distance_duration_from_direction(distance_json)
    return (distance, duration)

def main():
    ak = 'RNYTWuvcC1M8PWYPqerbbQ0V8bTX6gRY'
    csv_input_file = 'data/xiamen_kindergarden.csv'
    verbose = True
    setup_logging(verbose)
    logging.info("Starting read csv file process...")
    try:
        schools = pd.read_csv(csv_input_file, sep=',',header=None)
        #schools = pd.read_csv('data/kinder_school_2018.csv', sep=';', header=0)
        map_client = baidumap_client.BuiduMapClient(ak=ak)
        logging.info("Initialize the map client")
    except Exception as error:
        logger.error(error)
        raise

    schools.loc[:,'distance_daz']=np.array([100000] * len(schools))
    schools.loc[:,'distance_xdx']=np.array([100000] * len(schools))
    schools.loc[:,'distance_ave']=np.array([100000] * len(schools))

    region = '厦门'

    try:
        origin_coord_daz = get_coord(map_client, '顶澳仔6号', region)
        origin_coord_xdx = get_coord(map_client, '曾厝垵西里155号', region)
        logging.info('Coords for orginal position {} and {}'.format(origin_coord_daz, origin_coord_xdx))
    except Exception as error:
        logger.error(error)
        raise


    for index, row in schools.iterrows():
        #school = schools.at[index,'幼儿园名称']
        #place = schools.at[index,'办学地址']
        school = row[0]
        place = row[3]
        try:
            target_coord = get_coord(map_client, place, region)
            logging.info('index [{}], school [{}], at place [{}], coord: [{}]'.format(index, school, place, target_coord))
            (distance_daz, duration_daz) = get_distance(map_client, origin_coord_daz, target_coord)
            (distance_xdx, duration_xdx) = get_distance(map_client, origin_coord_xdx, target_coord)
            average_distance = ( distance_daz + distance_xdx ) / 2;
            schools.at[index, 'distance_daz'] = distance_daz
            schools.at[index, 'distance_xdx'] = distance_xdx
            schools.at[index, 'distance_ave'] = average_distance

        except Exception as error:
            logging.error(error)
            logging.info("{} can not found".format(school))

        if index > 100:
            break

    schools.to_csv("distance.csv")
    #(school, place, distance, duration)


if __name__  == '__main__':
    main()
