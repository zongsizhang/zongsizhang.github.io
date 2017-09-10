# geospark python API notes

## usage of pyspark

pyspark has done a lot of works on optimizing communication between local python process and jvm. So we should rely on pyspark as much as possible.

pyspark use py4j to communicate python object and java object. When python program submits spark task, python data will be serialized into java objects. So we'd better keep data in java format and only deserialize into python objects when native program asks for them. 

So for most java classes in geospark, we'd better just keep the original java object and offer python interfaces for user to call. We only offer serializer and deserializer for objects that user may be able to manipulate in other places.

## important issue

convertion between python object and java object. Libraries like com.jts.geom can not be naturally understood by python. Maybe we need to offer serializer and deserializer between java and python claases. Or there are other ways to do translate work.

Below is the implementation strategy for every geospark classes.

1. org.datasyslab.geospark.enums

For all the three enum classes, we need to reimplement them in python. We keep a dictionary that map from python enum value to java enum value.

2. org.datasyslab.geospark.SpatialRDD

For all SpatialRDD classes, we offer same methods in python classes but don't rewrite any codes, we just keep a java object of SpatialRDD and call relevant functions by py4j gateway.

