# Shapefile

## Bibligraphy
ESRI shapefile technical description

https://github.com/harsha2010/magellan

https://github.com/Esri/geometry-api-java

https://github.com/Esri/geometry-api-java/wiki  explanations of geometry types.

https://community.hortonworks.com/articles/44319/geo-spatial-queries-with-hive-using-esri-geometry.html     How to use esri hadoop api

http://docs.oracle.com/bigdata/bda48/BDVAJ/oracle/spatial/spark/vector/class-use/SparkRecordInfoProvider.html   An interface that accept record length.


## Shapefile Description
Shapefile stores nontopological geometry and attribute information. An ESRI shapefile consists of three specific files.
- .shp , main file. Direct access, variable-record-length.
- .shx , index file. each record contains offset of the corresponding main file record from beginning.
- .dbf , dBASE table. feature attributes corresponding records in main file. one-to-one with records in main file.

### Name Criteria
Three files have same prefix, prefix are of following format

(a-Z or 0-9)(a-Z or 0-9 or _ or - )<sup>*</sup>.	Where lenth of second part is 0-7.

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
integer and double-precision integers that make up data description fields in file header and record contents are of little endian byte order. others(data make up rest fields, file management) are in big endian.

##### file header
In total 50 16-bit words. Consists of 17 fields. List important fields
**Shape Type**: All non-null shapes in this file are required to be of the same shape type. Values are binded with a specific shape type. Check it in description document.
**Bounding Box**: Actual extent of all shapes in the file. If file is empty, Xmin, Xmax, Ymax, Ymin can be unused, which assigned to 0.0 . Mmin and Mmax can contain "no data" values.

###### parse file header
Before start parsing file, we need to read and remove file header from the whole input stream. 

The endian byte orders specified in description are as follow.
- Big : File Code(4 byte int) ; 5 * Unused (4 byte int);  File Length (4 byte int)
- little : Version (4 byte int) ; shape type (4 byte int) ; 8 * boundingbox value (8 byte double)

Here is an scala example from megallen.

```scala
override def initialize(inputSplit: InputSplit, taskAttemptContext: TaskAttemptContext) {
    val split = inputSplit.asInstanceOf[FileSplit]
    val job = MapReduceUtils.getConfigurationFromContext(taskAttemptContext)
    val start = split.getStart()
    val end = start + split.getLength()
    val file = split.getPath()
    val fs = file.getFileSystem(job)
    val is = fs.open(split.getPath())
    dis = new DataInputStream(is)
    require(is.readInt() == 9994)
    // skip the next 20 bytes which should all be zero
    0 until 5 foreach {_ => require(is.readInt() == 0)}
    // file length in bits
    length = 16 * is.readInt() - 50 * 16
    remaining = length
    val version = EndianUtils.swapInteger(is.readInt())
    require(version == 1000)
    // shape type: all the shapes in a given split have the same type
    val shapeType = EndianUtils.swapInteger(is.readInt())
    key.setFileNamePrefix(split.getPath.getName.split("\\.")(0))
    value = new ShapeWritable(shapeType)
    // skip the next 64 bytes
    0 until 8 foreach {_ => is.readDouble()}
  }
```

We can find magellan check the value of file code, version, and the unused 5 integers. And ignored the 8 boundingbox values.

To get values in 16-bit words. it use length = 16 * value;




##### Record Headers
8 bytes in total, 2 fields, each 4 types. one is record number(? what the fuck is number, possibly order?), another is length of this record. 

##### Record Contents
**Null Record** is allowed. Still can't get this bullshit, but yes you can have a record of geometric information that acutally is empty. It's a place holder, waiting for some damn data populated.

Record of any Shape type has a field named Shape type, follow the same value rule as that in file header. If a file is Null, it only has Shape type field equalt to 0.

##### Parse Contents

###### Parse Record Header

The two fields are both of big endian order.

```scala
override def nextKeyValue(): Boolean = {
    if (remaining <= 0) {
      false
    } else {
    	// record header has fixed length of 8 bytes
        // byte 0 = record #, byte 4 = content length
        val recordNumber = dis.readInt()
        // record numbers begin at 1
        require(recordNumber > 0)
        val contentLength = 16 * (dis.readInt() + 4)
        value.readFields(dis)
        remaining -= contentLength
        key.setRecordIndex(key.getRecordIndex() + 1)
        true
    }
}

```
No endian order swap. Which means it set default endian order to big(does hdfs set this default or ?).
It first read the Record Number and check if it is larger than 0. Then get the content length. Use remaining to monitor the read step.

Then call readFields to read the record content.

###### Parse Record Contents

All data are supposed to be of little endian order.

**specific notes left here**


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

- [x] Fiture out the structure of shapefile.
- [x] How Endian affects the implementation of our parser.
- [ ] How to build and run projects with multiple classes on Spark. (Only know how to run single class)
- [ ] Understanding Data structures in GeoSpark. What PointRdd, RectangleRDD, what they mean.
- [ ] GeoSpark utilization. (How to wrap data we parsed from shape file into formats in GeoSpark?)

### Possible solutions

#### Magellan Library

https://github.com/harsha2010/magellan

Can be downloaded from github. Coded in scala, work on spark.

#### Esri/geometry-api-java

https://github.com/Esri/geometry-api-java

Coded in java, but only work on spark. Need transplant.


