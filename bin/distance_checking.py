from baidumap.baidumap_client import BaiduMapClient
from baidumap import json_parse

#http://api.map.baidu.com/place/v2/search?query=顶澳仔6号&region=厦门&output=json&ak=RNYTWuvcC1M8PWYPqerbbQ0V8bTX6gRY
#http://api.map.baidu.com/direction/v2/riding?origin=40.01116,116.339303&destination=39.936404,116.452562&ak=RNYTWuvcC1M8PWYPqerbbQ0V8bTX6gRY
def main():
    map_client = BuiduMapClient()
    original_location_json = map_client.get(action='place', sub_action='search', params={'query': '顶澳仔6号', 'region': '厦门'})
    (origin_lat, origin_lng) = json_parse.get_geocode_from_direction(original_location_json)
    target_location_json = map_client.get(action='place', sub_action='search', params={'query': '曾厝安北路1号', 'region': '厦门'})
    (target_lat, target_lng) = json_parse.get_geocode_from_direction(target_location_json)
    origin_coord = "{},{}".format(origin_lat, origin_lng)
    target_coord = "{},{}".format(target_lat, target_lng)

    distance_json = map_client.get(action='direction', sub_action='riding', params={'origin':origin_coord,'destination':target_coord})
    (distance, duration) = json_parse.get_distance_duration_from_direction(distance_json)
    print (distance, duration)

if __name__  == '__main__':
    main()
