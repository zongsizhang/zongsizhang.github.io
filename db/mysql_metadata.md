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