#!/usr/bin/env python3
import os

def do_command(sql_query):
  base_command = 'sudo -u postgres psql nyc-taxi-data -c "%s"'  % sql_query
  os.system(base_command)

with open("table_names.txt") as f:
  for table_name in f:
    table_name = table_name.strip()

    # set GPS locations
    if('nets' in table_name):
      str_dict = {'long_min': -73.982455 ,'long_max': -73.967649, 'lat_min': 40.679035, 'lat_max': 40.687068}
    elif('yankees' in table_name):
      str_dict = {'long_min': -73.930917, 'long_max': -73.921411, 'lat_min': 40.829563, 'lat_max': 40.829679}
    elif('knicks' in table_name):
      str_dict = {'long_min': -73.998674, 'long_max': -73.986916, 'lat_min': 40.750780, 'lat_max': 40.755055}

    # determine trip direction
    if('incoming' in table_name):
      gps_tag = 'dropoff'
    elif('outgoing' in table_name):
      gps_tag = 'pickup'

    # add vars to str_dict
    str_dict['table_name'] = table_name
    str_dict['limit'] = 10
    str_dict['gps_tag'] = gps_tag
    
    sql_query = \
        '''
        SELECT * INTO %(table_name)s FROM trips WHERE
                (%(gps_tag)s_longitude between %(long_min)s and %(long_max)s) and
                (%(gps_tag)s_latitude between %(lat_min)s and %(lat_max)s)
        ''' % str_dict

    print("starting " + table_name)
    do_command(sql_query)
    print("finished " + table_name)
