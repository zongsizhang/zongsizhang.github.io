# MySql metadata research

reference:
[MYSQL 8.0 Reference Manual, Chapter 24, INFORMATION_SCHEMA Tables](https://dev.mysql.com/doc/refman/8.0/en/information-schema.html)

## INFORMATION_SCHEMA

This is where metadata of MySql stored.

### CHARACTER_SETS

provides *name*, *collation*, *description* and *maxlen* of all available char set in current MySql Instance

### COLLATIONS

provides information of collations, this part is important for tables with multiple languages records. **COLLATIONS** defines how strings are decoded and compared.

### COLLATION_CHARACTER_SET_APPLICABILITY

indicates what character set is applicble for what collation.

### <span style="color:blue">COLUMNS</span>

provides information about all columns in all tables in this MySql Instance

Useful Columns including: 

- *TABLE_SCHEMA*, *TABLE_NAME*, *COLUMN_NAME*, which together address a specific column
- *COLUMN_KEY*, which help check the type of index on this column. NUL(No), PRI(Primary), MUL(Index).

### COLUMN_PRIVILEGES

provides information about columnn privileges. This information comes from the *mysql.columns_priv* grant table.

To know more about privileges of mysql, head to

[Privileges provided by Mysql](https://dev.mysql.com/doc/refman/8.0/en/privileges-provided.html)

### ENGINES

provides information about storage engines.

### EVENTS

provides information about scheduled events

### FILES

provides information about InnoDB data files. In NDB Cluster this table also provides information about the files in which NDB Cluster Disk Data tables are stored.

### GLOBAL_STATUS and SESSION_STATUS

provide information about server status variables. Their contents correspond to the information produced by the *SHOW GLOBAL STATUS* and *SHOW SESSION STATUS statements*

### KEY_COLUMN_USAGE

describe which key columns have constrains

### ndb_transid_mysql_connection_map

provides a mapping between NDB transactions, NDB transaction coordinators, and MySQL Servers attached to an NDB Cluster as API nodes.

### OPTIMIZER_TRACE

provides information produced by the optimizer tracing capability

### PARAMETERS

provides information about stored procedure and function parameters, and about return values for stored functions

### PARTITIONS

provides information about table partitions.

### PLUGINS

provides information about server plugins

### PROCESSLIST

provides information about which threads are running

### PROFLING

provides statement profiling information. Its contents correspond to the information produced by the SHOW PROFILES and SHOW PROFILE statements

### REFERENTIAL_CONSTRAINTS 

provides information about foreign keys

### ROUTINES

provides information about stored routines

### SCHEMATA

provides information about databases

### SCHEMA_PRIVILEGES

provides information about schema (database) privileges

### <span style="color:blue">STATISTICS</span>

provides information about table indexes

### <span style="color:blue">TABLES</span>

table provides information about tables in databases

useful columns : *TABLE_ROWS*, *CREATE_TIME* + *UPDATE_TIME*

### TABLESPACES

provides information about active tablespaces

### TABLE_CONSTRAINTS

describes which tables have constraints

### TABLE_PRIVILEGES

provides information about table privileges

### TRIGGERS

provides information about triggers

### USER_PRIVILEGES

provides information about global privileges

### VIEWS

provides information about views in databases



