# Spark, read binary file

## Bibligraph

https://spark.apache.org/docs/2.0.2/api/java/org/apache/spark/SparkContext.html

## Fixed Length

**org.apache.spark.SparkContext.binaryRecords** : API for reading binary file with fixed length record into RDD.

```java
public RDD<byte[]> binaryRecords(String path, //file path
                        int recordLength, // length of all records
                        org.apache.hadoop.conf.Configuration conf) //configuration
```

## unfixed length

One possible way is to call hadoop api to process records when reading file from file system (possibley NewAPIHadoopFile). And then map records to new RDD.

andvanced solution is to read .shp and .dbf at the same time at merge them by record id. Then put them in the same record.

