# Spark, read and process binary file

## Bibligraph

https://spark.apache.org/docs/2.0.2/api/java/org/apache/spark/SparkContext.html

## General Idea

### Fixed Length

**org.apache.spark.SparkContext.binaryRecords** : API for reading binary file with fixed length record into RDD.

```java
public RDD<byte[]> binaryRecords(String path, //file path
                        int recordLength, // length of all records
                        org.apache.hadoop.conf.Configuration conf) //configuration
```

### unfixed length

One possible way is to call hadoop api to process records when reading file from file system (possibley NewAPIHadoopFile). And then map records to new RDD.

andvanced solution is to read .shp and .dbf at the same time at merge them by record id. Then put them in the same record.

```java
public <K,V,F extends org.apache.hadoop.mapreduce.InputFormat<K,V>> RDD<scala.Tuple2<K,V>> newAPIHadoopFile
								   (String path,Class<F> fClass,
                                   Class<K> kClass,
                                   Class<V> vClass,
                                   org.apache.hadoop.conf.Configuration conf)

```

## Reading file from hdfs

The method I learned from Magellen project to read file is as follow:

```java
ShapeParseUtil.initializeGeometryFactory();
        FileSplit fileSplit = (FileSplit)split;
        long start = fileSplit.getStart();
        long end = start + fileSplit.getLength();
        int len = (int)fileSplit.getLength();
        Path filePath = fileSplit.getPath();
        FileSystem fileSys = filePath.getFileSystem(context.getConfiguration());
        FSDataInputStream inputStreamFS = fileSys.open(filePath);
        inputStream = new DataInputStream(inputStreamFS);
```

### Problem
This is a so called classic solution. But when applying it to shapefile that is already put to hdfs, the program crashes. According to the Exception spark reports. The input stream we get loses consistency when we read it. But if we read the file into memory at once with IOUtils.readFully(). The byte array we get is integrated with the original file. So we can eliminate the possibility that the file has already lost its consistency. So there are two possible reasons for this error.

- The file on hdfs is already cut into pieces and is held in order by some mechanism of hdfs. But the DataInputStream can't get have no interface to get such information.

- Multiple mappers get involved in this task (InputSplit is not configured correctly)

The second problem can be solved by setting the FileInputFormat as follow:

```java
public RecordReader<ShapeKey, BytesWritable> createRecordReader(InputSplit split, TaskAttemptContext context) throws IOException, InterruptedException {
        return new ShapeFileReader(split, context);
    }

    @Override
    protected boolean isSplitable(JobContext context, Path filename) {
        return false;
    }
```

According to the log, we can also ensure that only one task is registered for reading shapefile. So the only possible reason is that fileSys.open(Path) loses the track of original order of pieces.

### A unuseful but interesting solution

I tried to use InputStream utils from Java.io to replace hadoop interfaces. But it failed to read file from hdfs. The report shows that the program can't find the file by the uri we provide.

