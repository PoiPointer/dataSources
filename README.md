PoiPointer Data Sources
=======================

DataSources
--
* http://opendata.brussels.be/explore/
* http://cirb.brussels/fr/nos-solutions/urbis-solutions/telechargement
* http://urbisdownload.gis.irisnet.be


Info
--
* shape -> geojson : http://ben.balter.com/2013/06/26/how-to-convert-shapefiles-to-geojson-for-use-on-github/


Accessing the UrbIS Zone of Interest Culture Data Set
--

*Manual download:*

* http://urbisdownload.gis.irisnet.be
* http://urbisdownload.gis.irisnet.be/en/dimension > 2D > Next
* http://urbisdownload.gis.irisnet.be/en/product > UrbIS-Map > Next
* http://urbisdownload.gis.irisnet.be/en/zone > Region > Next
* http://urbisdownload.gis.irisnet.be/en/format > SHP > Next
* http://urbisdownload.gis.irisnet.be/en/download > Conditions of UrbIS use read and accepted > Click on the link(s) below to download the file(s) you asked for:

Result: /Region/UrbMap_SHP.zip

*Web Service:*

    http://geoserver.gis.irisnet.be/geoserver/urbis/wfs?service=WFS&version=1.1.0&request=GetFeature&typeName=URB_M_ZIPOINT&CQL_FILTER=TYPE=%27CU%27&outputFormat=json

[Click here to test](http://geoserver.gis.irisnet.be/geoserver/urbis/wfs?service=WFS&version=1.1.0&request=GetFeature&typeName=URB_M_ZIPOINT&CQL_FILTER=TYPE=%27CU%27&outputFormat=json)

This returns the UrbIS 'Zone of Interest' layer and type CU=Culture data set in GeoJson format.



Converting UrbIS ZIPOINT CU from SHP to GeoJson
--

    ogr2ogr -where "TYPE=\"CU\"" -f GeoJSON -s_srs "EPSG:31370" -t_srs "WGS84" UrbMap_ZIPOINT_CU.geojson UrbMap_ZIPOINT.shp
