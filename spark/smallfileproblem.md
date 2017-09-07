# Solution to loading small shapefiles [GeoSpark]

## bibliography
[small file problems](https://blog.cloudera.com/blog/2009/02/the-small-files-problem/)

## Probem Statement

The shapefile format is a popular geospatial vector data format for geographic information system (GIS) software. Due to the huge volume of data, it's not appropriate to pack all data into one shapefile, which means it's important for shapefile loader to be able to read and parse multiple shapefiles at the same time.

A shapefile is not a singe file but a directory of files, and main contents are stored in .shp file(geo-spatial data) and .dbf file(attributes) separately. So when I first design file reader, to avoid Join operation between geographic data and attributes, I open both inputstream at the same time and read both records synchronously. Due to such strategy, every single shapefile will produce a RDD, and when reading multiple files, we can only use loop to read them one by one, which is a waste of clusters' capacity.

## Solution






