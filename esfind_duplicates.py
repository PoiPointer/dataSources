#!/usr/bin/python
#
# esfind_duplicates.py
#
# find duplicates in the PoiPointer data sets in ElasticSearch
#
# http://192.168.5.186:9200/poipointer/_search
#
# Copyright (C) 2014 Jeremy Tammik, Autodesk Inc.
#
from __future__ import unicode_literals
from optparse import OptionParser
import json, requests
from find_duplicates import *

_version = '1.0'

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
  "Read all PoiPointer data records from PoiPointer ElasticSearch database and list duplicates"

  print 'esfind_duplicates is obsolete now.\nUse find_duplicates.py -e instead. Bye.'
  exit(1)

  progname = 'esfind_duplicates'
  usage = 'usage: %s [options]' % progname
  parser = OptionParser( usage, version = progname + ' ' + _version )
  parser.add_option( '-?', '--question', action='store_true', dest='question', default=False, help = 'show this help message and exit' )
  parser.add_option( '-c', '--count', action='store_true', dest='count', default=False, help = 'show data set entry count' )
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

  d2 = get_poipointer_data_from_elastic_search(options)

  determine_duplicate_records(d2,options)

if __name__ == "__main__":
  main()