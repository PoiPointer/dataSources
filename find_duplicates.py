#!/usr/bin/python
#
# find_duplicates.py
#
# find duplicates in the PoiPointer data sets
#
# Copyright (C) 2014 Jeremy Tammik, Autodesk Inc.
#
from __future__ import unicode_literals
from optparse import OptionParser
import json

_version = '1.0'

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

def print_dict(d):
  keys = d.keys()
  keys.sort()
  for k in keys:
    print k, d[k]

def main():
  "Read all PoiPointer data records and list duplicates"

  progname = 'find_duplicates'
  usage = 'usage: %s [options]' % progname
  parser = OptionParser( usage, version = progname + ' ' + _version )
  parser.add_option( '-?', '--question', action='store_true', dest='question', default=False, help = 'show this help message and exit' )
  parser.add_option( '-c', '--count', action='store_true', dest='count', default=False, help = 'show data set entry count' )
  parser.add_option( '-l', '--list', action='store_true', dest='list', default=False, help = 'list data set entries' )
  parser.add_option( '-p', '--precision', type='int', dest='precision', default=4, help = 'define precision, i.e. 3 or 4 digits' )
  #parser.add_option( '-q', '--quiet', action='store_true', dest='quiet', help = 'reduce verbosity' )

  (options, args) = parser.parse_args()

  #print options
  #print args

  if options.question:
    raise SystemExit(parser.print_help() or 1)

  d2 = {}

  for nk in dataset_name_abbreviation_and_property_key:
    d = get_records(nk)

    if options.list:
      print "\n{0} ({1}) has {2} entries:".format(
        nk[0], nk[1], len(d) )
      print_dict(d)

    elif options.count:
      print "{0} ({1}) has {2} entries.".format(
        nk[0], nk[1], len(d) )

    for k,v in d.items():
      if d2.has_key(k):
        d2[k].append(v)
      else:
        d2[k] = [v]

  print '\nDuplicate PoiPointer records:'

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