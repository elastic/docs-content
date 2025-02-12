---
applies:
  stack:
  serverless:
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/maps-clean-your-data.html
---

# Clean your data [maps-clean-your-data]

Geospatial fields in {{es}} have certain restrictions that need to be addressed before upload. On this section a few recipes will be presented to help troubleshooting common issues on this type of data.


## Convert to GeoJSON or Shapefile [_convert_to_geojson_or_shapefile] 

Use [ogr2ogr](https://gdal.org/programs/ogr2ogr.md) (part of the [GDAL/OGR](https://gdal.org) suite) to convert datasets into a GeoJSON or Esri Shapefile. For example, use the following commands to convert a GPX file into JSON:

```sh
# Example GPX file from https://www.topografix.com/gpx_sample_files.asp
#
# Convert the GPX waypoints layer into a GeoJSON file
$ ogr2ogr \
  -f GeoJSON "waypoints.geo.json" \ # Output format and file name
  "fells_loop.gpx" \ # Input File Name
  "waypoints" # Input Layer (usually same as file name)

# Extract the routes layer into a GeoJSON file
$ ogr2ogr -f "GeoJSON" "routes.geo.json" "fells_loop.gpx" "routes"
```


## Convert to WGS84 Coordinate Reference System [_convert_to_wgs84_coordinate_reference_system] 

{{es}} only supports WGS84 Coordinate Reference System. Use `ogr2ogr` to convert from other coordinate systems to WGS84.

On the following example, `ogr2ogr` transforms a shapefile from [NAD83](https://epsg.org/crs_4269/NAD83.md) to [WGS84](https://epsg.org/crs_4326/WGS-84.md). The input CRS is detected automatically thanks to the `.prj` sidecar file in the source dataset.

```sh
# Example NAD83 file from https://www2.census.gov/geo/tiger/GENZ2018/shp/cb_2018_us_county_5m.zip
#
# Convert the Census Counties shapefile to WGS84 (EPSG:4326)
$ ogr2ogr -f "Esri Shapefile" \
  "cb_2018_us_county_5m.4326.shp" \ # Output file
  -t_srs "EPSG:4326" \ # EPSG:4326 is the code for WGS84
  "cb_2018_us_county_5m.shp" \ # Input file
  "cb_2018_us_county_5m" # Input layer
```


## Improve performance by breaking out complex geometries into one geometry per document [_improve_performance_by_breaking_out_complex_geometries_into_one_geometry_per_document] 

Sometimes geospatial datasets are composed by a small amount of geometries that contain a very large amount of individual part geometries. A good example of this situation is on detailed world country boundaries datasets where records for countries like Canada or Philippines have hundreds of small island geometries. Depending on the final usage of a dataset, you may want to break out this type of dataset to keep one geometry per document, considerably increasing the performance of your index.

```sh
# Example NAD83 file from www12.statcan.gc.ca/census-recensement/2011/geo/bound-limit/files-fichiers/2016/ler_000b16a_e.zip
#
# Check the number of input features
$ ogrinfo -summary ler_000b16a_e.shp ler_000b16a_e \
  | grep "Feature Count"
Feature Count: 76

# Convert to WGS84 exploding the multiple geometries
$ ogr2ogr \
  -f "Esri Shapefile" \
  "ler_000b16a_e.4326-parts.shp" \ # Output file
  -explodecollections \ # Convert multiparts into single records
  -t_srs "EPSG:4326" \ # Transform to WGS84
  "ler_000b16a_e.shp" \ # Input file
  "ler_000b16a_e" # Input layer

# Check the number of geometries in the output file
# to confirm the 76 records are exploded into 27 thousand rows
$ ogrinfo -summary ler_000b16a_e.4326-parts.shp ler_000b16a_e.4326 \
  | grep "Feature Count"
Feature Count: 27059
```

::::{warning} 
A dataset containing records with a very large amount of parts as the one from the example above may even hang in {{kib}} Maps file uploader.

::::



## Reduce the precision [_reduce_the_precision] 

Some machine generated datasets are stored with more decimals than are strictly necessary. For reference, the GeoJSON RFC 7946 [coordinate precision section](https://datatracker.ietf.org/doc/html/rfc7946#section-11.2) specifies six digits to be a common default to around 10 centimeters on the ground. The file uploader in the Maps application will automatically reduce the precision to 6 decimals but for big datasets it is better to do this before uploading.

`ogr2ogr` generates GeoJSON files with 7 decimal degrees when requesting `RFC7946` compliant files but using the `COORDINATE_PRECISION` [GeoJSON layer creation option](https://gdal.org/drivers/vector/geojson.md#layer-creation-options) it can be downsized even more if that is OK for the usage of the data.

```sh
# Example NAD83 file from https://www2.census.gov/geo/tiger/GENZ2018/shp/cb_2018_us_county_5m.zip
#
# Generate a 2008 GeoJSON file
$ ogr2ogr \
  -f GeoJSON \
  "cb_2018_us_county_5m.4326.geo.json" \ # Output file
  -t_srs "EPSG:4326" \ # Convert to WGS84
  -lco "RFC7946=NO" \ # Request a 2008 GeoJSON file
  "cb_2018_us_county_5m.shp" \
  "cb_2018_us_county_5m"

# Generate a RFC7946 GeoJSON file
$ ogr2ogr \
  -f GeoJSON \
  "cb_2018_us_county_5m.4326.RFC7946.geo.json" \ # Output file
  -t_srs "EPSG:4326" \ # Convert to WGS84
  -lco "RFC7946=YES" \ # Request a RFC7946 GeoJSON file
  "cb_2018_us_county_5m.shp" \
  "cb_2018_us_county_5m"

# Generate a RFC7946 GeoJSON file with just 5 decimal figures
$ ogr2ogr \
  -f GeoJSON \
  "cb_2018_us_county_5m.4326.RFC7946_mini.geo.json" \ # Output file
  -t_srs "EPSG:4326" \  # Convert to WGS84
  -lco "RFC7946=YES" \ # Request a RFC7946 GeoJSON file
  -lco "COORDINATE_PRECISION=5" \ # Downsize to just 5 decimal positions
  "cb_2018_us_county_5m.shp" \
  "cb_2018_us_county_5m"

# Compare the disk size of the three output files
$ du -h cb_2018_us_county_5m.4326*.geo.json
7,4M	cb_2018_us_county_5m.4326.geo.json
6,7M	cb_2018_us_county_5m.4326.RFC7946.geo.json
6,1M	cb_2018_us_county_5m.4326.RFC7946_mini.geo.json
```


## Simplifying region datasets [_simplifying_region_datasets] 

Region datasets are polygon datasets where the boundaries of the documents don’t overlap. This is common for administrative boundaries, land usage, and other continuous datasets. This type of datasets has the special feature that any geospatial operation modifying the lines of the polygons needs to be applied in the same way to the common sides of the polygons to avoid the generation of thin gap and overlap artifacts.

[`mapshaper`](https://github.com/mbloch/mapshaper) is an excellent tool to work with this type of datasets as it understands datasets of this nature and works with them accordingly.

Depending on the usage of a region dataset, different geospatial precisions may be adequate. A world countries dataset that is displayed for the entire planet does not need the same precision as a map of the countries in the South Asian continent.

`mapshaper` offers a [`simplify`](https://github.com/mbloch/mapshaper/wiki/Command-Reference#-simplify) command that accepts percentages, resolutions, and different simplification algorithms.

```sh
# Example NAD83 file from https://www2.census.gov/geo/tiger/GENZ2018/shp/cb_2018_us_county_5m.zip
#
# Generate a baseline GeoJSON file from OGR
$ ogr2ogr \
  -f GeoJSON "cb_2018_us_county_5m.ogr.geo.json" \
  -t_srs "EPSG:4326" \
  -lco RFC7946=YES \
  "cb_2018_us_county_5m.shp" \
  "cb_2018_us_county_5m"

# Simplify at different percentages with mapshaper
$ for pct in 10 50 75 99; do \
  mapshaper \
    -i "cb_2018_us_county_5m.shp" \ # Input file
    -proj "EPSG:4326" \ # Output projection
    -simplify "${pct}%" \ # Simplification
    -o cb_2018_us_county_5m.mapshaper_${pct}.geo.json; \ # Output file
  done

# Compare the size of the output files
$ du -h cb_2018_us_county_5m*.geo.json
2,0M	cb_2018_us_county_5m.mapshaper_10.geo.json
4,1M	cb_2018_us_county_5m.mapshaper_50.geo.json
5,3M	cb_2018_us_county_5m.mapshaper_75.geo.json
6,7M	cb_2018_us_county_5m.mapshaper_99.geo.json
6,7M	cb_2018_us_county_5m.ogr.geo.json
```


## Fixing incorrect geometries [_fixing_incorrect_geometries] 

The Maps application expects valid GeoJSON or Shapefile datasets. Apart from the mentioned CRS requirement, geometries need to be valid. Both `ogr2ogr` and `mapshaper` have options to try to fix invalid geometries:

* OGR [`-makevalid`](https://gdal.org/programs/ogr2ogr.md#cmdoption-ogr2ogr-makevalid) option
* Mapshaper [`-clean`](https://github.com/mbloch/mapshaper/wiki/Command-Reference#-clean) command


## And so much more [_and_so_much_more] 

`ogr2ogr` and `mapshaper` are excellent geospatial ETL (Extract Transform and Load) utilities that can do much more than viewed here. Reading the documentation in detail is worth investment to improve the quality of the datasets by removing unwanted fields, refining data types, validating value domains, etc. Finally, being command line utilities, both can be automated and added to QA pipelines.

