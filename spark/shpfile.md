# Shapefile

## Bibligraphy
ESRI shapefile technical description


## Shapefile Description
Shapefile stores nontopological geometry and attribute information. An ESRI shapefile consists of three specific files.
- .shp , main file. Direct access, variable-record-length.
- .shx , index file. each record contains offset of the corresponding main file record from beginning.
- .dbf , dBASE table. feature attributes corresponding records in main file. one-to-one with records in main file.

### Name Criteria
Three files have same prefix, prefix are of following format

(a-Z | 0-9)(a-Z | 0-9 | _ | - )<sup>*</sup>.	Where lenth of second part is 0-7.

### Numerric types
- Integer: Signed 32-bit integer(4 bytes)
- Double: Signed 64-bit IEEE double-precision floating point number (8 bytes)

Floating point point numbers must be numeric values. +INF, -INF and NaN is not allowed. Any floating point number less than -10<sup>38</sup> can be seen as "no data".

### Organization of files

#### Main file .shp

##### Object Oriented Organization
- File Header
- Record Header, Reord Contents
- Record Header, Record Contents
- ..........

file header is an description of including multiple features, for example, Shape Type, Bounding Box. etc.

##### Byte Order
integer and double-precision integers that make up data description fields and record contents are of little endian byte order. others(data make up rest fields, file management) are in big endian.

##### file header
In total 50 16-bit words. Consists of 17 fields. List important fields
**Shape Type**: All non-null shapes in this file are required to be of the same shape type. Values are binded with a specific shape type. Check it in description document.
**Bounding Box**: Actual extent of all shapes in the file. If file is empty, Xmin, Xmax, Ymax, Ymin can be unused, which assigned to 0.0 . Mmin and Mmax can contain "no data" values.

##### Record Headers
8 bytes in total, 2 fields, each 4 types. one is record number(? what the fuck is number, possibly order?), another is length of this record. 

##### Record Contents
**Null Record** is allowed. Still can't get this bullshit, but yes you can have a record of geometric information that acutally is empty. It's a place holder, waiting for some damn data populated.

Record of any Shape type has a field named Shape type, follow the same value rule as that in file header. If a file is Null, it only has Shape type field equalt to 0.

Specific notes left to fill later.

#### Index File .shx

##### Object Oriented Organization
- File Header
- Record
- Record
- ..........

##### File header
File header is in the same organization as which in main file(.shp). Difference is that field "file length" store the length of index file.

##### Record
8 bytes. Actually same as Record Header in main file. Difference is that first field is offset of current record in main file. Also in **16-bit words**.

#### dBase File .dbf
dBase File can be seen as an custumized extension of shp. Features other than shape data can be added. It's formmated with standard DBF. Following 4 requiremnts below it's considered valid.
1. Must have the same prefix as .shp and .shx file.
2. Must be one-to-one corresponding to records in main file.
3. Order must be same as shape files.
4. year value in header must be the year since 1990.


## Parse Plan

### Before Start

Problems to be figured out:
- [ ] How Endian affects the implementation of our parser.(maybe should read in reverse order?)
- [ ] How to build and run projects with multiple classes on Spark. (Only know how to run single class)
- [ ] Understanding Data structures in GeoSpark. What PointRdd, RectangleRDD, what they mean.
- [ ] GeoSpark utilization. (How to wrap data we parsed from shape file into formats in GeoSpark?)



