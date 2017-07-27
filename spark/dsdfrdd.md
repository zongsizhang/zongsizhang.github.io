# RDD, Data frame and Data set. Comparison and analysis.


## Resillient Distributed Dataset (RDD)

**type-safety**. In general, RDD organize data like a Object-oriented database system. Records are referenced as objects. So it's easy to find type error when compile.

**High cost serialization**. Since RDD is type-safety. It costs a lot to communicate or do IO on data in RDD since we need to do more complex serialization and deserialization work on RDD more frequently, which will also makes overhead of GC too large.

## DataFrame

**schema**. Data are viewed as a relational table. DataFrame holds a schema to understand every row of data. So when doing serialization and deserialization, we can directly deal with data themselves and skip complex data structure.

**off-head** spark can open up memory out of jvm for DataFrame.

**catalyst** A component that support DataFrame and DataSet, which can optimize the query logic. Using rules like push conditions down in query tree to reduce data amount.

## DataSet

**Strong-typed**. Since DataSet combines characters of RDD and DataFrame. It has both objective(like RDD) and relational(like DataFrame) view of data. Because of this combination, DataSet can't allow implicit type conversion, which makes if strong-typed.

**Encoder** Encoder is the fundamental concept in the serialization and deserialization (SerDe) framework in Spark SQL 2.0. Spark SQL uses the SerDe framework for IO to make it efficient time- and space-wise. Encoder can convert objective query to binary so that spark can interact directly with binary records and deserialize data selectively.

**Higher-level** Till now, we can see DataSet as a higher level abstract as DataFrame. In spark it defines DataFrame as DataSet[row].
