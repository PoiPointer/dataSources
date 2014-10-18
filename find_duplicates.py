#!/usr/bin/python
#
# find_duplicates.py
#
# find duplicates in the PoiPointer data sets in GeoJson files
#
# Copyright (C) 2014 Jeremy Tammik, Autodesk Inc.
#
from __future__ import unicode_literals
from optparse import OptionParser
import json, requests

_version = '1.0'

dataset_name_type_and_property_key = [
  ['art-heritage-of-regional-roads-fountains0', 'fountain', 'fr_name'],
  ['art-heritage-of-regional-roads-monuments', 'monument', 'fr_name'],
  ['comic-book-route', 'comic', 'character_author'],
  ['cultural-places', 'culturalplace', 'cultural_place'],
  ['museums0', 'museum', 'museum'],
  ['theatres', 'theatre', 'description'],
  ['urbis_2d_map_zipoint_zones_of_interest_cu_culture', 'urb', 'TXT_FRE']
]

def get_dataset_type( record ):
  "Extract the data set type from a record."
  i = record.index( '{' )
  j = record.index('}')
  typ = record[i+1:j]
  #print typ, record
  return typ

def get_feature_coordinates_string(feature, precision):
  coords = feature['geometry']['coordinates']
  if not coords: return '<null>'
  length = precision + 3
  sformat = '{0}.{1}'.format( length, precision)
  sformat = '{0:' + sformat + 'f} {1:' + sformat + 'f}'
  #print sformat
  return sformat.format(coords[0], coords[1])

def get_records( name_type_and_property_key, precision ):
  [name,typ,key]=name_type_and_property_key
  filename = name + '.geojson'
  #return get_records_1(filename,typ,key)
  with open(filename) as json_file:
    json_data = json.load(json_file)
  records = {}
  #print name, len(json_data['features'])
  for row in json_data['features']:
    coords = get_feature_coordinates_string(row,precision)
    if not records.has_key(coords): records[coords]=[]
    records[coords].append( "{0} {{{1}}}".format(
      row['properties'][key], typ))
  return records

def print_dict(d):
  keys = d.keys()
  keys.sort()
  count = 0
  for k in keys:
    n = len(d[k])
    if 1 == n: print k, ", ".join(d[k])
    else: print k, n, ", ".join(d[k])
    count += n
  print count, 'entries.'

def determine_duplicate_records(d2, options):
  """Determine duplicate records from dictionary of records.
  Key is a coordinate string, value is a list. Each list
  entry is a record _id with its _type in brackets."""

  nduplicate_coords = 0
  nduplicate_entries = 0
  nduplicate_entries_per_dataset = {}

  for nk in dataset_name_type_and_property_key:
    nduplicate_entries_per_dataset[nk[1]] = 0

  duplicate_records = []
  keys = d2.keys()
  keys.sort()
  for k in keys:
    vals = d2[k]
    n = len(vals)
    if 1 < n:
      nduplicate_coords += 1
      nduplicate_entries += n
      for v in vals:
        nduplicate_entries_per_dataset[
          get_dataset_type(v)] += 1
      duplicate_records.append([k,n,vals])

  print '\n{0} duplicate PoiPointer records:'.format(
    len(duplicate_records))

  for a in duplicate_records:
    s = "{0}: {1} {2}".format( a[0], a[1], ", ".join(a[2]))
    print s.encode('utf-8')

  print "\n{0} duplicate coordinates with {1} duplicate entries:".format(
    nduplicate_coords, nduplicate_entries )
  keys = nduplicate_entries_per_dataset.keys()
  keys.sort()
  for k in keys:
    print "{0:4d} duplicates in {1}".format(
      nduplicate_entries_per_dataset[k], k )
  print

  if options.url:
    d = {a[1]: [] for a in
      dataset_name_type_and_property_key}
    for a in duplicate_records:
      for val in a[2]:
        typ = get_dataset_type(val)
        rid = val.replace( '{'+typ+'}', '' )
        typ2 = typ
        if 'urb' == typ: typ2 = 'culturalplace'
        d[typ].append(
          "http://192.168.5.186:9200/poipointer/{0}/{1}".format(
            typ2, rid ))
    for v in d['urb']:
      print v.encode('utf-8')
    keys = d.keys()
    keys.sort()
    for k in keys:
      if 'urb' == k: continue
      for v in d[k]:
        print v.encode('utf-8')

def get_poipointer_data_from_geojson(options):
  "Read all PoiPointer data records from GeoJson dataset files"
  d2 = {}
  for nk in dataset_name_type_and_property_key:
    d = get_records(nk,options.precision)

    if options.list:
      print "\n{0} ({1}) has {2} entries:".format(
        nk[0], nk[1], len(d) )
      print_dict(d)

    elif options.count:
      print "{0} ({1}) has {2} entries.".format(
        nk[0], nk[1], len(d) )

    for k,vals in d.items():
      if not d2.has_key(k): d2[k] = []
      for v in vals:
        d2[k].append(v)
  return d2

def get_poipointer_data_from_elastic_search(options):
  "Read all PoiPointer data records from PoiPointer ElasticSearch database"
  d2 = {}
  r = requests.get('http://192.168.5.186:9200/poipointer/_search?size=1000')
  #print r
  j = json.loads(r.content)
  #print j
  hits = j['hits']['hits']
  print len(hits), 'entries found in ElasticSearch.'
  for h in hits:
    t = h['_type'].lower().replace('comicbookroute','comic').replace('heritage','')
    i = h['_id']
    coords = get_feature_coordinates_string(h['_source'], options.precision)
    #print coords, h['_type'], h['_id']
    if not d2.has_key(coords): d2[coords] = []
    d2[coords].append( '{0} {{{1}}}'.format( i, t ) )
  return d2

def main():
  "Read all PoiPointer data records from GeoJson files and list duplicates"

  progname = 'find_duplicates'
  usage = 'usage: %s [options]' % progname
  parser = OptionParser( usage, version = progname + ' ' + _version )
  parser.add_option( '-?', '--question', action='store_true', dest='question', default=False, help = 'show this help message and exit' )
  parser.add_option( '-c', '--count', action='store_true', dest='count', default=False, help = 'show data set entry count' )
  parser.add_option( '-e', '--elasticsearch', action='store_true', dest='elasticsearch', default=False, help = 'read data from ElasticSearch, not GeoJson' )
  parser.add_option( '-l', '--list', action='store_true', dest='list', default=False, help = 'list data set entries' )
  parser.add_option( '-p', '--precision', type='int', dest='precision', default=3, help = 'define precision, i.e. 3 or 4 digits' )
  parser.add_option( '-u', '--url', action='store_true', dest='url', default=False, help = 'generate and list URLs to delete' )
  #parser.add_option( '-q', '--quiet', action='store_true', dest='quiet', help = 'reduce verbosity' )

  (options, args) = parser.parse_args()

  #print options
  #print args

  if options.question:
    raise SystemExit(parser.print_help() or 1)

  if not options.precision in [3,4]:
    print "Sorry, I don't know what will happen if you specify a precision different from 3 or 4."
    print "Well, actually, the only thing that will happen is that you see this message..."
    raise SystemExit(parser.print_help() or 1)

  if options.elasticsearch:
    d2 = get_poipointer_data_from_elastic_search(options)
  else:
    d2 = get_poipointer_data_from_geojson(options)

  determine_duplicate_records(d2,options)

if __name__ == "__main__":
  main()