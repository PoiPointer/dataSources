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

dataset_name_abbreviation_and_property_key = [
  ['art-heritage-of-regional-roads-fountains0', 'fountain', 'fr_name'],
  ['art-heritage-of-regional-roads-monuments', 'monument', 'fr_name'],
  ['comic-book-route', 'bd', 'character_author'],
  ['cultural-places', 'cp', 'cultural_place'],
  ['museums0', 'museum', 'museum'],
  ['theatres', 'theatre', 'description'],
  ['urbis_2d_map_zipoint_zones_of_interest_cu_culture', 'urb', 'TXT_FRE']
]

def get_feature_coordinates_string(feature):
  coords = feature['geometry']['coordinates']
  return "{0:7.3f} {1:7.3f}".format(coords[0], coords[1])

#def get_records_1(filename, abbreviation, property_key):
#  with open(filename) as json_file:
#    json_data = json.load(json_file)
#  records = {}
#  for row in json_data['features']:
#    coords = get_feature_coordinates_string(row)
#    records[coords] = "%s (%s)".format(
#      row['properties'][property_key],
#      abbreviation)
#  return records

def get_records( name_abbreviation_and_property_key ):
  [name,abbr,key]=name_abbreviation_and_property_key
  filename = name + '.geojson'
  #return get_records_1(filename,abbr,key)
  with open(filename) as json_file:
    json_data = json.load(json_file)
  records = {}
  for row in json_data['features']:
    coords = get_feature_coordinates_string(row)
    records[coords] = "{0} ({1})".format(
      row['properties'][key], abbr)
  return records

#def get_urbis_records():
#  return get_records(dataset_name_and_property_key[-1])

def print_dict(d):
  keys = d.keys()
  keys.sort()
  for k in keys:
    print k, d[k]

def main():
  "Read all PoiPointer data records and list duplicates"

  d2 = {}

  for nk in dataset_name_abbreviation_and_property_key:
    d = get_records(nk)
    #print '\n\n' + nk[0] + ':'
    #print_dict(d)
    for k,v in d.items():
      if d2.has_key(k):
        d2[k].append(v)
      else:
        d2[k] = [v]

  print 'Duplicate PoiPointer records:'

  keys = d2.keys()
  keys.sort()
  for k in keys:
    vals = d2[k]
    n = len(vals)
    if 1 < n:
      s = "{0}: {1} {2}".format( k, n, ", ".join(vals))
      print s.encode('utf-8')

if __name__ == "__main__":
  main()