#!/usr/bin/python
#
# find_duplicates.py
#
# find duplicates in the PoiPointer data sets
#
# Copyright (C) 2014 Jeremy Tammik, Autodesk Inc.
#
from __future__ import unicode_literals
import json

dataset_name_and_property_key = [
  ['art-heritage-of-regional-roads-fountains0','fr_name'],
  ['art-heritage-of-regional-roads-monuments','fr_name'],
  ['comic-book-route','character_author'],
  ['cultural-places','cultural_place'],
  ['museums0','museum'],
  ['theatres','description'],
  ['urbis_2d_map_zipoint_zones_of_interest_cu_culture','TXT_FRE']
]

def get_feature_coordinates(feature):
  return feature['geometry']['coordinates']

def get_record_string(coords,property_value):
  return "{0:6.3f} {1:6.3f} {2}".format(coords[0], coords[1], property_value)

def get_records_1(filename,property_key):
  with open(filename) as json_file:
    json_data = json.load(json_file)
  rows = []
  for row in json_data['features']:
    coords = get_feature_coordinates(row)
    #rows.append( [coords[0], coords[1], row['properties'][property_key]] )
    rows.append( get_record_string(coords,row['properties'][property_key] ))
  return rows

def get_records(name_and_property_key):
  [name,key]=name_and_property_key
  filename = name + '.geojson'
  return get_records_1(filename,key)

def get_urbis_records():
  return get_records(dataset_name_and_property_key[-1])

'''
def get_art_heritage_records(name):
  filename = name + '.geojson'
  return get_records_1(filename,'fr_name')

def get_comic_book_route_records(name):
  filename = name + '.geojson'
  return get_records_1(filename,'character_author')
'''

print '\n\nurbis:'

for row in get_urbis_records():
  print row

'''
for n in dataset_names_other[:-1]:
  if n.startswith('art-heritage'):
    rows = get_art_heritage_records(n)
  elif n.startswith('comic-book-route'):
    rows = get_comic_book_route_records(n)
  else:
    print '\n\n' + n + ':'
    with open(n + '.geojson') as json_file:
      json_data = json.load(json_file)
      rows = []
      for row in json_data['features']:
        coords = get_feature_coordinates(row)
        rows.append( [coords[0], coords[1], row['properties']['fr_name']] )
      for row in rows:
        print row
'''

for nk in dataset_name_and_property_key[:-1]:
  print '\n\n' + nk[0] + ':'
  rows = get_records(nk)
  for row in rows:
    print row
