#!/usr/bin/python
#
# find_duplicates.py
#
# find duplicates in the PoiPointer data sets
#
# Copyright (C) 2014 Jeremy Tammik, Autodesk Inc.
#
import json

dataset_name_urbis = 'urbis_2d_map_zipoint_zones_of_interest_cu_culture'

dataset_names_other = [
  'art-heritage-of-regional-roads-fountains0',
  'art-heritage-of-regional-roads-monuments',
  'comic-book-route',
  'cultural-places',
  'museums0',
  'theatres'
]

def get_urbis_records():
  filename = dataset_name_urbis + '.geojson'
  with open(filename) as json_file:
    json_data_urbis = json.load(json_file)
  rows = []
  for x in json_data_urbis['features']:
    coords = x['geometry']['coordinates']
    rows.append( [coords[0], coords[1], x['properties']['TXT_FRE']] )
  return rows

for row in get_urbis_records():
  print row

exit(1)

for n in dataset_names_other:
  with open(n + '.geojson') as json_file:
    json_data = json.load(json_file)
    print '\n' + n + ':', json_data.items()[0]
    print json_data.items()[1]

