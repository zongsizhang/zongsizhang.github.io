# geospark python API notes

## usage of pyspark

pyspark has done a lot of works on optimizing communication between local python process and jvm. So we should rely on pyspark as much as possible.

pyspark use py4j to communicate python object and java object, pickle to serialize and deserialize python objects. This is a bad news, since for every piece of data pyspark will do serialization works two times to make it work in cluster.

[pyspark runtime](images/pysparkruntime.png)

With Py4j, we are able to call all functions of objects in jvm with their id. So it's possible to just add a python shell on geospark so that every time user call a function in python, we just translate commands into java codes by py4j.

Since Pickle can automatically translate Lists, Dict and prime data structures objects between java and python, as long as input and output of Methods are of these types, we don't need to deal with the double serialization problem. But we can't make such assumption because GeoSpark actually needs to deal with inputs and outputs of customized classes.

Below is an example,

```java

private static JavaPairRDD<Polygon, HashSet<Geometry>> executeSpatialJoinUsingIndex(SpatialRDD spatialRDD, SpatialRDD queryRDD, boolean considerBoundaryIntersection) throws Exception {
	//...
}

```

This method returns a pair rdd of <polygon, HashSet<Geometry>>, it's impossbile for pickle to automatically convert this type of data into a specific python rdd without any instruction. PairRDD is not a geospark defined class and it's unable to just package it with python interfaces. Even if we do so by rewriting spark codes, after returning this object we loss track of it and users may take this object to other native python logics where sparkcontext is even unaccessible.

So for all logics correlated with spark, we can do the simple package work, but for logics that will need to return objects, we will need to make a python copy of java objects that native python program and use. In reverse, if input data is of customized class, we will need to translate it into java objects.

And this serialization and deserialization demand will lead a very severe problem.

1. pyspark is actually designed to be driven by python logics, which means although python objects can be pickled into java objects and logics can be translated so that manipulation can be done in java, java executor actually doesn't understand the data structure.

Given a smple pyspark example.

```python

# myclass.py

class MyClass:
    def __init__(self, value):
        self.v = str(value)

    def addValue(self, value):
        self.v += str(value)
        return self

    def getValue(self):
        return self.v

# main.py

import sys
from pyspark import SparkContext
from myclass import MyClass

if __name__ == "__main__":
    if len(sys.argv) != 1:
        print("Usage CC")
        exit(-1)

    data = [1, 2, 3, 4, 5, 2, 5, 3, 2, 3, 7, 3, 4, 1, 4]
    sc = SparkContext(appName="WordCount")
    d = sc.parallelize(data)
    inClass = d.map(lambda input: (input, MyClass(input)))
    reduzed = inClass.reduceByKey(lambda a, b: a.addValue(b.getValue()))
    print(reduzed.collect())

```

_inClass_ is an rdd of MyClass objects, and it will be picked into java rdd, but there will be no corresponding named class in java created. Pyspark has done complex work to make sure serialized objects can be manipulated correctly, but it doesn't care about what exactly the objects it manipulates are.

Our problem is that now we have java logics, and we want to make it understood by python. This will ask objects that our logics manipulate to be all java objects. For example, even if there is a correspoding class with com.jts.geom.Coordinate in python, we will need to make a java copy for it. This will lead to 4 times serialization work and asks for complex logics to keep this two copy identical.

## Design Strategy

According to researches above, apparently there are two strategies to build our pygeospark.

1. python driven

Follow the design ideas if pyspark, rewrite logics in python.

### pros

- Easy to compat customized classes, friendly to extension.
- Leave performance problems to spark.

### cons

- Heavy code tasks, need to find python alternatives for libraries like com.jts.geom
- difficulty of maintainance

2. java driven

Only build interfaces for users to call methods. When it comes to data, make a copy.

### pros

- Can avoid some rewrite works
- Since GeoSpark handles input file, we can expect that java obejct -> python object tasks barely happens

### cons

- We also need to find alternatives for com.jts.geom in python
- not friendly to extension in python
- Overhead in serialization, really bad when update is frequent.

I personally prefer python driven solution since the second one is irresponsible and will leave a lot of problems to future developer. Also, with java driven solution we will be unable to keep up spark's trends.






