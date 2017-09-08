# Notes on PySpark

## [PySpark Internal](https://cwiki.apache.org/confluence/display/SPARK/PySpark+Internals)

PySpark is built on top of Spark's Java API. Data is processed in Python and cached / shuffled in the JVM:

![pyspark work flow](images/pyspark.jpg)

In python driver programs, SparkContext use Py4J to launch JVM and create a JavaSparkContext. Py4J is only used on driver for local communication between the Python and Java SparkContext objects; large data transfers are performed through a different mechanism.

RDD transformations in Python are mapped to transformations on PythonRDD objects in Java. On remote worker machines, PythonRDD objects launch Python subprocesses and communicate with them using pipes, sending the user's code and the data to be processed.

#### Py4j

Py4J enables Python programs running in a Python interpreter to dynamically access Java objects in a Java Virtual Machine. Methods are called as if the Java objects resided in the Python interpreter and Java collections can be accessed through standard Python collection methods. Py4J also enables Java programs to call back Python objects.

In pyspark, Py4j is only used for local communication. When communicating large volume of data, since socket.readline() is slow, pyspark will dump data into an RDD and send via Pipes. Data and Code will be deserialized later in remote worker.

#### Daemon for launching worker processes

Many JVMs use fork/exec to launch child processes in ProcessBuilder or Runtime.exec. These child processes initially have the same memory footprint as their parent. When the Spark worker JVM has a large heap and spawns many child processes, this can cause memory exhaustion, leading to "Cannot allocate memory" errors. In Spark, this affects both pipe() and PySpark.

Other developers have run into the same problem and discovered a [variety of workarounds](https://gist.github.com/pmahoney/1970815), including adding extra swap space or telling the kernel to overcommit memory. We can't use the java_posix_spawn library to solve this problem because it's too difficult to package due to its use of platform-specific native binaries.

For PySpark, we resolved this problem by forking a daemon when the JVM heap is small and using that daemon to launch and manage a pool of Python worker processes. Since the daemon uses very little memory, it won't exhaust the memory during fork().

#### Serializing data

Data is currently serialized using the Python cPickle serializer. PySpark uses cPickle for serializing data because it's reasonably fast and supports nearly any Python data structure.

#### Why not perform more of the processing in Java

The prototype of pyspark was implemented in terms of PipedRDD. This prototype represented each python RDD as a JavaRDD[string] of based-64-encoded. This is to allow functions like join() to be implemented directly by calling java versions.

But To it's to convert java results back to back to pickled data, JavaRDD contained routines to flatten nested data structures containing pickled objects. This approach's correctness relied on serialized data equality being equivalent to Python object equality. However, there are some cases where logically identical objects can produce different pickles. This doesn't happen in most cases, but it can easily occur with dictionaries.

